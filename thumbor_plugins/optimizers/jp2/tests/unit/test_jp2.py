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

from thumbor_plugins.optimizers.jp2 import Optimizer


class Jp2OptimizerTest(TestCase):
    def get_context(self):
        conf = Config()
        conf.JP2_QUALITY = "80"
        ctx = Context(config=conf)
        ctx.request = RequestParameters()
        ctx.request.filters.append("jp2")

        return ctx

    @mock.patch("thumbor_plugins.optimizers.jp2.Image")
    def test_should_convert_image_as_rgb(self, pil_image_mock):
        image_opened_mock = mock.Mock()
        image_converted_mock = mock.Mock()
        image_opened_mock.convert.return_value = image_converted_mock
        pil_image_mock.open.return_value = image_opened_mock

        image_opened_mock.mode = "1"

        optimizer = Optimizer(self.get_context())
        optimizer.optimize(None, "input_file", "output_file")

        image_opened_mock.convert.assert_called_with(mode="RGB")
        image_converted_mock.save.assert_called_with(
            "output_file", "JPEG2000", quality_mode="dB", quality_layers=[80]
        )
