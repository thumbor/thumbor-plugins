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

from thumbor_plugins.optimizers.pngcrush import Optimizer


class PNGCrushOptimizerTest(TestCase):
    def setUp(self):
        self.workdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.workdir.cleanup)
        self.pngcrush_path = self.write_file("pngcrush", b"#!/bin/sh\n")
        os.chmod(self.pngcrush_path, stat.S_IRWXU)
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
        conf.PNGCRUSH_PATH = self.pngcrush_path
        for key, value in overrides.items():
            setattr(conf, key, value)
        ctx = Context(config=conf)
        ctx.request = RequestParameters()

        return ctx

    def completed(self, returncode, output=b"", stderr=b""):
        def run(command, **kwargs):
            with open(command[-1], "wb") as f:
                f.write(output)
            return subprocess.CompletedProcess(command, returncode, stderr=stderr)

        return mock.Mock(side_effect=run)

    def optimize(self, run_mock, **overrides):
        with mock.patch("subprocess.run", run_mock):
            optimizer = Optimizer(self.get_context(**overrides))
            optimizer.optimize(None, self.input_file, self.output_file)
        return run_mock

    def test_should_not_run_if_binary_missing(self):
        optimizer = Optimizer(self.get_context(PNGCRUSH_PATH="/missing/pngcrush"))
        self.assertFalse(optimizer.should_run(".png", ""))

    def test_should_not_run_if_binary_not_executable(self):
        os.chmod(self.pngcrush_path, stat.S_IRUSR | stat.S_IWUSR)
        optimizer = Optimizer(self.get_context())
        self.assertFalse(optimizer.should_run(".png", ""))

    def test_should_run_only_for_png(self):
        optimizer = Optimizer(self.get_context())
        self.assertFalse(optimizer.should_run(".jpg", ""))

    def test_should_run_for_png(self):
        optimizer = Optimizer(self.get_context())
        self.assertTrue(optimizer.should_run(".png", ""))

    def test_should_run_pngcrush_binary_without_a_shell(self):
        run_mock = self.optimize(self.completed(0, output=b"optimized png"))

        run_mock.assert_called_once()
        args, kwargs = run_mock.call_args
        self.assertEqual(
            args[0],
            [self.pngcrush_path, "-reduce", "-q", self.input_file, self.output_file],
        )
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        self.assertEqual(kwargs["timeout"], 30)
        self.assertNotIn("shell", kwargs)
        self.assertEqual(self.read_file(self.output_file), b"optimized png")

    def test_should_disable_timeout_when_zero(self):
        run_mock = self.optimize(self.completed(0, output=b"x"), PNGCRUSH_TIMEOUT=0)
        self.assertIsNone(run_mock.call_args.kwargs["timeout"])

    def test_should_serve_original_when_binary_fails(self):
        self.optimize(self.completed(1, output=b"partial", stderr=b"boom"))
        self.assertEqual(self.read_file(self.output_file), b"original png")

    def test_should_serve_original_when_output_is_empty(self):
        self.optimize(self.completed(0))
        self.assertEqual(self.read_file(self.output_file), b"original png")

    def test_should_serve_original_on_timeout(self):
        run_mock = mock.Mock(
            side_effect=subprocess.TimeoutExpired(cmd="pngcrush", timeout=30)
        )
        self.optimize(run_mock)
        self.assertEqual(self.read_file(self.output_file), b"original png")

    def test_should_accept_timeout_as_string(self):
        run_mock = self.optimize(self.completed(0, output=b"x"), PNGCRUSH_TIMEOUT="30")
        self.assertEqual(run_mock.call_args.kwargs["timeout"], 30)

    def test_should_not_run_if_timeout_is_not_a_number(self):
        optimizer = Optimizer(self.get_context(PNGCRUSH_TIMEOUT="soon"))
        self.assertFalse(optimizer.should_run(".png", ""))

    def test_should_not_run_if_timeout_is_not_finite_or_negative(self):
        for timeout in ["inf", "nan", "-1", -5]:
            optimizer = Optimizer(self.get_context(PNGCRUSH_TIMEOUT=timeout))
            self.assertFalse(optimizer.should_run(".png", ""), timeout)
