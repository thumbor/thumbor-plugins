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


class Optimizer(BaseOptimizer):
    def __init__(self, context):
        super(Optimizer, self).__init__(context)

        self.runnable = True
        self.pngquant_path = self.context.config.PNGQUANT_PATH
        self.pngquant_quality = self.context.config.PNGQUANT_QUALITY or '65-80'
        self.pngquant_speed = self.context.config.PNGQUANT_SPEED or '3'

        if not (os.path.isfile(self.pngquant_path) and os.access(self.pngquant_path, os.X_OK)):
            logger.error("ERROR pnqquant path '{0}' is not accessible".format(self.pngquant_path))
            self.runnable = False

    def should_run(self, image_extension, buffer):
        return 'png' in image_extension and self.runnable

    def optimize(self, buffer, input_file, output_file):
        command = 'cat %s | %s --speed %s --quality=%s - > %s' % (
            input_file,
            self.pngquant_path,
            self.pngquant_speed,
            self.pngquant_quality,
            output_file,
        )
        with open(os.devnull) as null:
            logger.debug("[PNGQUANT] running: " + command)
            subprocess.call(command, shell=True, stdin=null)
