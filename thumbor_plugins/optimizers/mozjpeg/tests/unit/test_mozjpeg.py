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

from thumbor_plugins.optimizers.mozjpeg import Optimizer


class MozJpegOptimizerTest(TestCase):
    def setUp(self):
        self.workdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.workdir.cleanup)
        self.mozjpeg_path = self.write_file("cjpeg", b"#!/bin/sh\n")
        os.chmod(self.mozjpeg_path, stat.S_IRWXU)
        self.input_file = self.write_file("input", b"original jpeg")
        self.output_file = self.write_file("output", b"")
        self.intermediary = self.output_file + "-intermediate"

        image_open_patcher = mock.patch("PIL.Image.open")
        self.image_open = image_open_patcher.start()
        self.addCleanup(image_open_patcher.stop)
        self.image_open.return_value.save.side_effect = self.write_intermediary

    def write_intermediary(self, path, image_format):
        self.assertEqual(path, self.intermediary)
        self.assertEqual(image_format, "tga")
        self.write_file(os.path.basename(path), b"tga")

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
        conf.MOZJPEG_PATH = self.mozjpeg_path
        for key, value in overrides.items():
            setattr(conf, key, value)
        ctx = Context(config=conf)
        ctx.request = RequestParameters()

        return ctx

    def completed(self, returncode, output=b"", stderr=b""):
        def run(command, **kwargs):
            self.assertTrue(os.path.exists(self.intermediary))
            with open(command[command.index("-outfile") + 1], "wb") as f:
                f.write(output)
            return subprocess.CompletedProcess(command, returncode, stderr=stderr)

        return mock.Mock(side_effect=run)

    def optimize(self, run_mock, **overrides):
        with mock.patch("subprocess.run", run_mock):
            optimizer = Optimizer(self.get_context(**overrides))
            optimizer.optimize(None, self.input_file, self.output_file)
        return run_mock

    def test_should_not_run_if_binary_missing(self):
        optimizer = Optimizer(self.get_context(MOZJPEG_PATH="/missing/cjpeg"))
        self.assertFalse(optimizer.should_run(".jpeg", ""))

    def test_should_not_run_if_binary_not_executable(self):
        os.chmod(self.mozjpeg_path, stat.S_IRUSR | stat.S_IWUSR)
        optimizer = Optimizer(self.get_context())
        self.assertFalse(optimizer.should_run(".jpeg", ""))

    def test_should_run_only_for_jpg(self):
        optimizer = Optimizer(self.get_context())
        self.assertFalse(optimizer.should_run(".png", ""))

    def test_should_run_for_jpg(self):
        optimizer = Optimizer(self.get_context())
        self.assertTrue(optimizer.should_run(".jpg", ""))

    def test_should_run_for_jpeg(self):
        optimizer = Optimizer(self.get_context())
        self.assertTrue(optimizer.should_run(".jpeg", ""))

    def test_should_run_mozjpeg_binary_without_a_shell(self):
        run_mock = self.optimize(self.completed(0, output=b"optimized jpeg"))

        run_mock.assert_called_once()
        args, kwargs = run_mock.call_args
        self.assertEqual(
            args[0],
            [
                self.mozjpeg_path,
                "-quality",
                "75",
                "-optimize",
                "-outfile",
                self.output_file,
                self.intermediary,
            ],
        )
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        self.assertEqual(kwargs["timeout"], 30)
        self.assertNotIn("shell", kwargs)
        self.image_open.assert_called_once_with(self.input_file)
        self.assertEqual(self.read_file(self.output_file), b"optimized jpeg")
        self.assertFalse(os.path.exists(self.intermediary))

    def test_should_use_configured_quality(self):
        run_mock = self.optimize(self.completed(0, output=b"x"), MOZJPEG_QUALITY=90)
        self.assertEqual(run_mock.call_args.args[0][2], "90")

    def test_should_disable_timeout_when_zero(self):
        run_mock = self.optimize(self.completed(0, output=b"x"), MOZJPEG_TIMEOUT=0)
        self.assertIsNone(run_mock.call_args.kwargs["timeout"])

    def test_should_serve_original_when_binary_fails(self):
        self.optimize(self.completed(2, output=b"partial", stderr=b"boom"))
        self.assertEqual(self.read_file(self.output_file), b"original jpeg")
        self.assertFalse(os.path.exists(self.intermediary))

    def test_should_serve_original_when_output_is_empty(self):
        self.optimize(self.completed(0))
        self.assertEqual(self.read_file(self.output_file), b"original jpeg")

    def test_should_serve_original_on_timeout(self):
        run_mock = mock.Mock(
            side_effect=subprocess.TimeoutExpired(cmd="cjpeg", timeout=30)
        )
        self.optimize(run_mock)
        self.assertEqual(self.read_file(self.output_file), b"original jpeg")
        self.assertFalse(os.path.exists(self.intermediary))

    def test_should_accept_timeout_as_string(self):
        run_mock = self.optimize(self.completed(0, output=b"x"), MOZJPEG_TIMEOUT="30")
        self.assertEqual(run_mock.call_args.kwargs["timeout"], 30)

    def test_should_not_run_if_timeout_is_not_a_number(self):
        optimizer = Optimizer(self.get_context(MOZJPEG_TIMEOUT="soon"))
        self.assertFalse(optimizer.should_run(".jpg", ""))

    def test_should_not_run_if_timeout_is_not_finite_or_negative(self):
        for timeout in ["inf", "nan", "-1", -5]:
            optimizer = Optimizer(self.get_context(MOZJPEG_TIMEOUT=timeout))
            self.assertFalse(optimizer.should_run(".jpg", ""), timeout)
