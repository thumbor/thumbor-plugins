#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

import os
import stat
import subprocess
import tempfile
from unittest import TestCase, mock

from thumbor.config import Config
from thumbor.context import Context, RequestParameters

from thumbor_plugins.optimizers.optipng import Optimizer


class OptiPNGOptimizerTest(TestCase):
    def setUp(self):
        self.workdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.workdir.cleanup)
        self.optipng_path = self.write_file("optipng", b"#!/bin/sh\n")
        os.chmod(self.optipng_path, stat.S_IRWXU)
        self.input_file = self.write_file("input", b"original png")
        self.output_file = self.write_file("output", b"")

    def write_file(self, name, content):
        path = os.path.join(self.workdir.name, name)
        with open(path, "wb") as f:
            f.write(content)
        return path

    def read_file(self, path):
        with open(path, "rb") as f:
            return f.read()

    def get_context(self, **overrides):
        conf = Config()
        conf.OPTIPNG_PATH = self.optipng_path
        for key, value in overrides.items():
            setattr(conf, key, value)
        ctx = Context(config=conf)
        ctx.request = RequestParameters()

        return ctx

    def completed(self, returncode, output=b"", stderr=b""):
        def run(command, **kwargs):
            output_file = command[command.index("-out") + 1]
            with open(output_file + ".bak", "wb"):
                pass
            with open(output_file, "wb") as f:
                f.write(output)
            return subprocess.CompletedProcess(command, returncode, stderr=stderr)

        return mock.Mock(side_effect=run)

    def optimize(self, run_mock, **overrides):
        with mock.patch("subprocess.run", run_mock):
            optimizer = Optimizer(self.get_context(**overrides))
            optimizer.optimize(None, self.input_file, self.output_file)
        return run_mock

    def test_should_not_run_if_binary_missing(self):
        optimizer = Optimizer(self.get_context(OPTIPNG_PATH="/missing/optipng"))
        self.assertFalse(optimizer.should_run(".png", ""))

    def test_should_not_run_if_binary_not_executable(self):
        os.chmod(self.optipng_path, stat.S_IRUSR | stat.S_IWUSR)
        optimizer = Optimizer(self.get_context())
        self.assertFalse(optimizer.should_run(".png", ""))

    def test_should_not_run_if_level_is_not_an_integer(self):
        optimizer = Optimizer(self.get_context(OPTIPNG_LEVEL="fast"))
        self.assertFalse(optimizer.should_run(".png", ""))

    def test_should_run_only_for_png(self):
        optimizer = Optimizer(self.get_context())
        self.assertFalse(optimizer.should_run(".jpg", ""))

    def test_should_run_for_png(self):
        optimizer = Optimizer(self.get_context())
        self.assertTrue(optimizer.should_run(".png", ""))

    def test_should_run_optipng_binary_without_a_shell(self):
        run_mock = self.optimize(self.completed(0, output=b"optimized png"))

        run_mock.assert_called_once()
        args, kwargs = run_mock.call_args
        self.assertEqual(
            args[0],
            [
                self.optipng_path,
                "-fix",
                "-preserve",
                "-force",
                "-keep",
                "-o5",
                "-out",
                self.output_file,
                "--",
                self.input_file,
            ],
        )
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        self.assertEqual(kwargs["timeout"], 30)
        self.assertNotIn("shell", kwargs)
        self.assertEqual(self.read_file(self.output_file), b"optimized png")

    def test_should_accept_level_as_string(self):
        run_mock = self.optimize(self.completed(0, output=b"x"), OPTIPNG_LEVEL="2")
        self.assertIn("-o2", run_mock.call_args.args[0])

    def test_should_disable_timeout_when_zero(self):
        run_mock = self.optimize(self.completed(0, output=b"x"), OPTIPNG_TIMEOUT=0)
        self.assertIsNone(run_mock.call_args.kwargs["timeout"])

    def test_should_serve_original_when_binary_fails(self):
        self.optimize(self.completed(1, output=b"partial", stderr=b"boom"))
        self.assertEqual(self.read_file(self.output_file), b"original png")

    def test_should_serve_original_when_output_is_empty(self):
        self.optimize(self.completed(0))
        self.assertEqual(self.read_file(self.output_file), b"original png")

    def test_should_serve_original_on_timeout(self):
        run_mock = mock.Mock(
            side_effect=subprocess.TimeoutExpired(cmd="optipng", timeout=30)
        )
        self.optimize(run_mock)
        self.assertEqual(self.read_file(self.output_file), b"original png")

    def test_should_not_run_if_level_is_below_one(self):
        for level in [-1, 0, "0"]:
            optimizer = Optimizer(self.get_context(OPTIPNG_LEVEL=level))
            self.assertFalse(optimizer.should_run(".png", ""), level)

    def test_should_cap_level_at_seven(self):
        for level in [8, "99"]:
            run_mock = self.optimize(
                self.completed(0, output=b"x"), OPTIPNG_LEVEL=level
            )
            self.assertIn("-o7", run_mock.call_args.args[0], level)

    def test_should_accept_timeout_as_string(self):
        run_mock = self.optimize(self.completed(0, output=b"x"), OPTIPNG_TIMEOUT="30")
        self.assertEqual(run_mock.call_args.kwargs["timeout"], 30)

    def test_should_not_run_if_timeout_is_not_a_number(self):
        optimizer = Optimizer(self.get_context(OPTIPNG_TIMEOUT="soon"))
        self.assertFalse(optimizer.should_run(".png", ""))

    def test_should_not_run_if_timeout_is_not_finite_or_negative(self):
        for timeout in ["inf", "nan", "-1", -5]:
            optimizer = Optimizer(self.get_context(OPTIPNG_TIMEOUT=timeout))
            self.assertFalse(optimizer.should_run(".png", ""), timeout)

    def test_should_remove_the_backup_optipng_leaves_behind(self):
        self.optimize(self.completed(0, output=b"x"))
        self.assertFalse(os.path.exists(self.output_file + ".bak"))

    def test_should_remove_the_backup_when_binary_fails(self):
        self.optimize(self.completed(1, output=b"partial"))
        self.assertFalse(os.path.exists(self.output_file + ".bak"))
