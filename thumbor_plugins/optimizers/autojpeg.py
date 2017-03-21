#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license


import os
import subprocess

from thumbor.optimizers import BaseOptimizer
from thumbor.utils import logger
from PIL import Image
from io import BytesIO

class Optimizer(BaseOptimizer):
    def __init__(self, context):
        super(Optimizer, self).__init__(context)

        self.autojpeg_quality = int(self.context.config.AUTOJPEG_QUALITY)
        self.autojpeg_subsampling = int(self.context.config.AUTOJPEG_SUBSAMPLING)

    def should_run(self, image_extension, buffer):
        if not 'png' in image_extension:
            return False;

        input_image = Image.open(BytesIO(buffer))
        extrema = input_image.getextrema()
        has_alpha = (len(extrema) > 3) and (extrema[3][0] < 255)
        if input_image.mode == 'P' or has_alpha:
            return False;

        return True;

    def optimize(self, buffer, input_file, output_file):
        return Image.open(input_file).save(output_file, 'JPEG', quality=self.autojpeg_quality, optimize=True, subsampling=self.autojpeg_subsampling)
