#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from shutil import which
from unittest import TestCase, mock

from thumbor.config import Config
from thumbor.context import Context, RequestParameters
from thumbor.utils import EXTENSION

from thumbor_plugins.optimizers.jpegrecompress import Optimizer


class MozJpegOptimizerTest(TestCase):
    def setUp(self):
        self.os_path_isfile_patcher = mock.patch("os.path.isfile")
        self.os_access_patcher = mock.patch("os.access")
        self.mock_os_path_isfile = self.os_path_isfile_patcher.start()
        self.mock_os_access = self.os_access_patcher.start()

    def tearDown(self):
        self.os_path_isfile_patcher.stop()
        self.mock_os_access.stop()

    def get_context(self):
        conf = Config()
        conf.JPEGRECOMPRESS_PATH = "/usr/bin/jpeg-recompress"
        ctx = Context(config=conf)
        ctx.request = RequestParameters()

        return ctx

    def test_should_not_run_if_binary_missing(self):
        self.mock_os_path_isfile.return_value = False
        optimizer = Optimizer(self.get_context())
        self.assertFalse(optimizer.should_run(".jpeg", ""))

    def test_should_not_run_if_binary_not_executable(self):
        self.mock_os_access.return_value = False
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

    @mock.patch("subprocess.call")
    @mock.patch("PIL.Image.open")
    def test_should_run_mozjpeg_binary(self, pil_image_mock, subprocess_call_mock):
        optimizer = Optimizer(self.get_context())
        optimizer.optimize(None, "input_file", "output_file")
        subprocess_call_mock.assert_called_with(
            "/usr/bin/jpeg-recompress --strip --accurate --loops 10 input_file output_file",
            shell=True,
            stdin=mock.ANY,
        )
