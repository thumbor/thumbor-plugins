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

from thumbor_plugins.optimizers.pngquant import Optimizer


class PNGQuantOptimizerTest(TestCase):
    def setUp(self):
        self.workdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.workdir.cleanup)
        self.pngquant_path = self.write_file("pngquant", b"#!/bin/sh\n")
        os.chmod(self.pngquant_path, stat.S_IRWXU)
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
        conf.PNGQUANT_PATH = self.pngquant_path
        conf.PNGQUANT_QUALITY = "65-80"
        conf.PNGQUANT_SPEED = "1"
        for key, value in overrides.items():
            setattr(conf, key, value)
        ctx = Context(config=conf)
        ctx.request = RequestParameters()

        return ctx

    def completed(self, returncode, stdout=b"", stderr=b""):
        def run(command, **kwargs):
            kwargs["stdout"].write(stdout)
            return subprocess.CompletedProcess(command, returncode, stderr=stderr)

        return mock.Mock(side_effect=run)

    def optimize(self, run_mock, **overrides):
        with mock.patch("subprocess.run", run_mock):
            optimizer = Optimizer(self.get_context(**overrides))
            optimizer.optimize(None, self.input_file, self.output_file)
        return run_mock

    def test_should_not_run_if_binary_missing(self):
        optimizer = Optimizer(self.get_context(PNGQUANT_PATH="/missing/pngquant"))
        self.assertFalse(optimizer.should_run(".png", ""))

    def test_should_not_run_if_binary_not_executable(self):
        os.chmod(self.pngquant_path, stat.S_IRUSR | stat.S_IWUSR)
        optimizer = Optimizer(self.get_context())
        self.assertFalse(optimizer.should_run(".png", ""))

    def test_should_run_only_for_png(self):
        optimizer = Optimizer(self.get_context())
        self.assertFalse(optimizer.should_run(".jpg", ""))

    def test_should_run_for_png(self):
        optimizer = Optimizer(self.get_context())
        self.assertTrue(optimizer.should_run(".png", ""))

    def test_should_run_pngquant_binary_without_a_shell(self):
        run_mock = self.optimize(self.completed(0, stdout=b"optimized png"))

        run_mock.assert_called_once()
        args, kwargs = run_mock.call_args
        self.assertEqual(
            args[0],
            [self.pngquant_path, "--speed", "1", "--quality=65-80", "-"],
        )
        self.assertEqual(kwargs["stdin"].name, self.input_file)
        self.assertEqual(kwargs["stdout"].name, self.output_file)
        self.assertEqual(kwargs["timeout"], 30)
        self.assertNotIn("shell", kwargs)
        self.assertEqual(self.read_file(self.output_file), b"optimized png")

    def test_should_disable_timeout_when_zero(self):
        run_mock = self.optimize(self.completed(0, stdout=b"x"), PNGQUANT_TIMEOUT=0)
        self.assertIsNone(run_mock.call_args.kwargs["timeout"])

    def test_should_serve_original_when_binary_fails(self):
        self.optimize(self.completed(1, stdout=b"partial", stderr=b"boom"))
        self.assertEqual(self.read_file(self.output_file), b"original png")

    def test_should_serve_original_when_output_is_empty(self):
        self.optimize(self.completed(0))
        self.assertEqual(self.read_file(self.output_file), b"original png")

    def test_should_serve_original_when_quality_target_not_met(self):
        with self.assertLogs("thumbor", level="DEBUG") as logs:
            self.optimize(self.completed(99, stdout=b"24-bit original"))
        self.assertEqual(self.read_file(self.output_file), b"original png")
        self.assertIn(
            "DEBUG:thumbor:[PNGQUANT] quality target not met, serving the original",
            logs.output,
        )
        self.assertNotIn("WARNING", [record.levelname for record in logs.records])

    def test_should_serve_original_on_timeout(self):
        run_mock = mock.Mock(
            side_effect=subprocess.TimeoutExpired(cmd="pngquant", timeout=30)
        )
        self.optimize(run_mock)
        self.assertEqual(self.read_file(self.output_file), b"original png")

    def test_should_accept_timeout_as_string(self):
        run_mock = self.optimize(self.completed(0, stdout=b"x"), PNGQUANT_TIMEOUT="30")
        self.assertEqual(run_mock.call_args.kwargs["timeout"], 30)

    def test_should_not_run_if_timeout_is_not_a_number(self):
        optimizer = Optimizer(self.get_context(PNGQUANT_TIMEOUT="soon"))
        self.assertFalse(optimizer.should_run(".png", ""))

    def test_should_not_run_if_timeout_is_not_finite_or_negative(self):
        for timeout in ["inf", "nan", "-1", -5]:
            optimizer = Optimizer(self.get_context(PNGQUANT_TIMEOUT=timeout))
            self.assertFalse(optimizer.should_run(".png", ""), timeout)

    def test_should_accept_quality_as_a_value_or_a_range(self):
        for quality in ["80", "65-80", "0-100", "-80", "65-", 80]:
            optimizer = Optimizer(self.get_context(PNGQUANT_QUALITY=quality))
            self.assertTrue(optimizer.should_run(".png", ""), quality)

    def test_should_not_run_if_quality_is_invalid(self):
        for quality in ["101", "80-65", "abc", "-", "65-101"]:
            optimizer = Optimizer(self.get_context(PNGQUANT_QUALITY=quality))
            self.assertFalse(optimizer.should_run(".png", ""), quality)

    def test_should_not_run_if_speed_is_invalid(self):
        for speed in ["0", "12", "fast", 12]:
            optimizer = Optimizer(self.get_context(PNGQUANT_SPEED=speed))
            self.assertFalse(optimizer.should_run(".png", ""), speed)

    def test_should_pass_speed_without_leading_zeros(self):
        run_mock = self.optimize(self.completed(0, stdout=b"x"), PNGQUANT_SPEED="03")
        self.assertEqual(run_mock.call_args.args[0][1:3], ["--speed", "3"])
