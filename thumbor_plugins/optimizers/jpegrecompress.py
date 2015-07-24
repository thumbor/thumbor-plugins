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
        self.jpegrecompress_path = self.context.config.JPEGRECOMPRESS_PATH

        if not (os.path.isfile(self.jpegrecompress_path) and os.access(self.jpegrecompress_path, os.X_OK)):
            logger.error("ERROR jpeg-recompress path '{0}' is not accessible".format(self.jpegrecompress_path))
            self.runnable = False

    def should_run(self, image_extension, buffer):
        return ('jpg' in image_extension or 'jpeg' in image_extension) and self.runnable

    def optimize(self, buffer, input_file, output_file):
        command = '%s --strip --accurate --loops 10 %s %s ' % (
            self.jpegrecompress_path,
            input_file,
            output_file,
        )
        with open(os.devnull) as null:
            logger.debug("[JPEG-RECOMPRESS] running: " + command)
            subprocess.call(command, shell=True, stdin=null)
