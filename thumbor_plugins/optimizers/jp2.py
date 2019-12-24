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

class Optimizer(BaseOptimizer):
    def __init__(self, context):
        super(Optimizer, self).__init__(context)

        self.jp2_quality = 80
        if self.context.config.JP2_QUALITY:
            if isinstance(self.context.config.JP2_QUALITY, str):
                self.jp2_quality = int(self.context.config.JP2_QUALITY)
            else:
                self.jp2_quality = self.context.config.JP2_QUALITY

    def should_run(self, image_extension, buffer):
        return 'jp2' in self.context.request.filters

    def optimize(self, buffer, input_file, output_file):
        im = Image.open(input_file)
        if im.mode in ['1', 'P']:
            if im.mode == '1':
                target_mode = 'RGB'
            else:
                # convert() figures out RGB or RGBA based on palette used
                target_mode = None
            im = im.convert(mode=target_mode)

        return im.save(output_file, 'JPEG2000', quality_mode='dB', quality_layers=[self.jp2_quality])