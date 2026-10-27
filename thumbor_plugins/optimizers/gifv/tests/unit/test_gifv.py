#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

import os
import subprocess
import tempfile
from unittest import TestCase, mock

from thumbor.config import Config
from thumbor.context import Context, RequestParameters

from thumbor_plugins.optimizers.gifv import Optimizer

FFMPEG_PATH = "/usr/bin/ffmpeg"


class GifvOptimizerTest(TestCase):
    def setUp(self):
        exists_patcher = mock.patch("thumbor_plugins.optimizers.gifv.exists")
        self.mock_exists = exists_patcher.start()
        self.addCleanup(exists_patcher.stop)

        self.workdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.workdir.cleanup)
        self.input_file = self.write_file("input", b"original gif")
        self.output_file = self.write_file("output", b"")

    def write_file(self, name, content):
        path = os.path.join(self.workdir.name, name)
        with open(path, "wb") as f:
            f.write(content)
        return path

    def read_file(self, path):
        with open(path, "rb") as f:
            return f.read()

    def get_context(self, filters="gifv()", **overrides):
        conf = Config()
        conf.FFMPEG_PATH = FFMPEG_PATH
        for key, value in overrides.items():
            setattr(conf, key, value)
        ctx = Context(config=conf)
        ctx.request = RequestParameters(filters=filters)

        return ctx

    def get_optimizer(self, filters="gifv()", **overrides):
        return Optimizer(self.get_context(filters, **overrides))

    def completed(self, returncode, output=b"", stderr=b""):
        def run(command, **kwargs):
            with open(command[command.index("-loglevel") - 1], "wb") as f:
                f.write(output)
            return subprocess.CompletedProcess(command, returncode, stderr=stderr)

        return mock.Mock(side_effect=run)

    def optimize(self, run_mock, filters="gifv()", **overrides):
        optimizer = self.get_optimizer(filters, **overrides)
        with mock.patch("subprocess.run", run_mock):
            optimizer.optimize(None, self.input_file, self.output_file)
        return optimizer, run_mock

    def test_should_run_for_gif_with_gifv_filter(self):
        for filters in ["gifv()", "gifv(webm)", "gifv", "quality(80):gifv():fill(f00)"]:
            self.assertTrue(self.get_optimizer(filters).should_run(".gif", ""), filters)

    def test_should_not_run_without_gifv_filter(self):
        for filters in ["", "quality(80)", "watermark(gifv.png,0,0)", "gifvx()", []]:
            self.assertFalse(
                self.get_optimizer(filters).should_run(".gif", ""), repr(filters)
            )

    def test_should_not_run_for_not_gif(self):
        for extension in [".jpg", ".jpeg", ".png", ".webp", ".mp4"]:
            self.assertFalse(self.get_optimizer().should_run(extension, ""), extension)

    def test_should_not_run_if_binary_ffmpeg_path_does_not_exist(self):
        self.mock_exists.return_value = False
        self.assertFalse(self.get_optimizer().should_run(".gif", ""))

    def test_should_default_to_mp4(self):
        for filters in [
            "gifv()",
            "gifv",
            "gifv(mp4)",
            "gifv():watermark(webm.png,0,0)",
        ]:
            file_format, params = self.get_optimizer(filters).set_format()
            self.assertEqual(file_format, "mp4", filters)
            self.assertEqual(params, ["-profile:v", "baseline", "-level", "4.0"])

    def test_should_use_webm_when_requested(self):
        for filters in [
            "gifv(webm)",
            "gifv( WEBM )",
            "gifv(\twebm)",
            "fill(f00):gifv(webm)",
        ]:
            file_format, params = self.get_optimizer(filters).set_format()
            self.assertEqual(file_format, "webm", filters)
            self.assertEqual(params[:2], ["-quality", "good"])

    def test_should_parse_background_color_filter(self):
        cases = {
            "gifv():background_color(ff00ff)": "#ff00ff",
            "background_color(magenta):gifv()": "#ff00ff",
            "gifv():background_color( f0f )": "#ff00ff",
            "gifv():background_color(nope)": None,
            "background_color:gifv()": None,
            "gifv():watermark(background_color(1).png,0,0)": None,
            "gifv()": None,
        }
        for filters, expected in cases.items():
            self.assertEqual(
                self.get_optimizer(filters).background_color(), expected, filters
            )

    def test_should_parse_background_color_with_valid_value(self):
        optimizer = self.get_optimizer()
        magenta_unicode_hex = "#ff00ff"
        self.assertEqual(
            optimizer.normalize_color_to_hex("ff00ff"), magenta_unicode_hex
        )
        self.assertEqual(
            optimizer.normalize_color_to_hex("#ff00ff"), magenta_unicode_hex
        )
        self.assertEqual(optimizer.normalize_color_to_hex("f0f"), magenta_unicode_hex)
        self.assertEqual(optimizer.normalize_color_to_hex("#f0f"), magenta_unicode_hex)
        self.assertEqual(
            optimizer.normalize_color_to_hex("magenta"), magenta_unicode_hex
        )

    def test_should_not_parse_background_color_with_invalid_value(self):
        optimizer = self.get_optimizer()
        self.assertEqual(optimizer.normalize_color_to_hex("asdfasdfasfd"), None)

    def test_should_run_ffmpeg_without_a_shell(self):
        optimizer, run_mock = self.optimize(
            self.completed(0, output=b"mp4 video"), "gifv():background_color(ff00ff)"
        )

        run_mock.assert_called_once()
        args, kwargs = run_mock.call_args
        command = args[0]
        self.assertEqual(command[0], FFMPEG_PATH)
        self.assertEqual(command[2:4], ["-f", "gif"])
        self.assertEqual(command[4:6], ["-trans_color", "0xffff00ff"])
        self.assertEqual(command[6:8], ["-i", self.input_file])
        self.assertIn("mp4", command)
        self.assertEqual(command[-3:], [self.output_file, "-loglevel", "error"])
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        self.assertEqual(kwargs["timeout"], 60)
        self.assertNotIn("shell", kwargs)
        self.assertEqual(self.read_file(self.output_file), b"mp4 video")
        self.assertEqual(optimizer.context.request.format, "mp4")

    def test_should_default_background_to_white(self):
        _, run_mock = self.optimize(self.completed(0, output=b"x"))
        self.assertEqual(
            run_mock.call_args.args[0][4:6], ["-trans_color", "0xffffffff"]
        )

    def test_should_encode_webm(self):
        optimizer, run_mock = self.optimize(
            self.completed(0, output=b"x"), "gifv(webm)"
        )
        self.assertIn("webm", run_mock.call_args.args[0])
        self.assertEqual(optimizer.context.request.format, "webm")

    def test_should_disable_timeout_when_zero(self):
        _, run_mock = self.optimize(self.completed(0, output=b"x"), FFMPEG_TIMEOUT=0)
        self.assertIsNone(run_mock.call_args.kwargs["timeout"])

    def test_should_serve_original_gif_when_ffmpeg_fails(self):
        optimizer, _ = self.optimize(self.completed(1, output=b"partial", stderr=b"x"))
        self.assertEqual(self.read_file(self.output_file), b"original gif")
        self.assertIsNone(optimizer.context.request.format)

    def test_should_serve_original_gif_when_output_is_empty(self):
        optimizer, _ = self.optimize(self.completed(0))
        self.assertEqual(self.read_file(self.output_file), b"original gif")
        self.assertIsNone(optimizer.context.request.format)

    def test_should_serve_original_gif_on_timeout(self):
        run_mock = mock.Mock(
            side_effect=subprocess.TimeoutExpired(cmd="ffmpeg", timeout=60)
        )
        optimizer, _ = self.optimize(run_mock)
        self.assertEqual(self.read_file(self.output_file), b"original gif")
        self.assertIsNone(optimizer.context.request.format)

    def test_should_not_run_for_unknown_gifv_argument(self):
        for filters in ["gifv(foo)", "gifv(a:b)", "gifv(webmx)", "gifv(mp4 webm)"]:
            optimizer = self.get_optimizer(filters)
            self.assertIsNone(optimizer.gifv_filter_argument(), filters)
            self.assertFalse(optimizer.should_run(".gif", ""), filters)

    def test_should_accept_timeout_as_string(self):
        _, run_mock = self.optimize(self.completed(0, output=b"x"), FFMPEG_TIMEOUT="60")
        self.assertEqual(run_mock.call_args.kwargs["timeout"], 60)

    def test_should_not_run_if_timeout_is_not_a_number(self):
        self.assertFalse(
            self.get_optimizer(FFMPEG_TIMEOUT="soon").should_run(".gif", "")
        )

    def test_should_not_run_if_timeout_is_not_finite_or_negative(self):
        for timeout in ["inf", "nan", "-1", -5]:
            optimizer = self.get_optimizer(FFMPEG_TIMEOUT=timeout)
            self.assertFalse(optimizer.should_run(".gif", ""), timeout)
