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
        self.path = self.context.config.JPEGRECOMPRESS_PATH
        self.method = self.context.config.JPEGRECOMPRESS_METHOD
        self.quality_preset = self.context.config.JPEGRECOMPRESS_QUALITY_PRESET
        self.quality_min = self.context.config.JPEGRECOMPRESS_QUALITY_MIN
        self.quality_max = self.context.config.JPEGRECOMPRESS_QUALITY_MAX
        self.loops = self.context.config.JPEGRECOMPRESS_LOOPS
        self.accurate = self.context.config.JPEGRECOMPRESS_ACCURATE
        self.subsample = self.context.config.JPEGRECOMPRESS_SUBSAMPLE

        if not (os.path.isfile(self.path) and os.access(self.path, os.X_OK)):
            logger.error("ERROR jpeg-recompress path '{0}' is not accessible".format(self.path))
            self.runnable = False

        if self.method not in ['mpe', 'ssim', 'ms-ssim', 'smallfry']:
            self.method = 'ssim'

        if self.quality_preset and self.quality_preset not in ['low', 'medium', 'high', 'veryhigh']:
            self.quality_preset = 'medium'

    def should_run(self, image_extension, buffer):
        return ('jpg' in image_extension or 'jpeg' in image_extension) and self.runnable

    def optimize(self, buffer, input_file, output_file):
        command = '%s --method %s %s %s %s --strip %s --subsample %s --loops %s %s %s ' % (
            self.path,
            self.method,
            '--quality ' + self.quality_preset if self.quality_preset else '',
            '--min ' + str(self.quality_min) if self.quality_min else '',
            '--max ' + str(self.quality_max) if self.quality_max else '',
            '--accurate' if self.accurate else '',
            'default' if self.subsample else 'disable',
            self.loops,
            input_file,
            output_file,
        )
        with open(os.devnull) as null:
            logger.debug("[JPEG-RECOMPRESS] running: " + command)
            subprocess.call(command, shell=True, stdin=null)
