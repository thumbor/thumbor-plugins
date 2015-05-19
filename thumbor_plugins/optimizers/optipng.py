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
        self.optipng_path = self.context.config.OPTIPNG_PATH
        self.optipng_level = self.context.config.OPTIPNG_LEVEL

        if not (os.path.isfile(self.optipng_path) and os.access(self.optipng_path, os.X_OK)):
            logger.error("ERROR optipng path '{0}' is not accessible".format(self.optipng_path))
            self.runnable = False

    def should_run(self, image_extension, buffer):
        return 'png' in image_extension and self.runnable

    def optimize(self, buffer, input_file, output_file):
        command = '%s -quiet -preserve -force -keep -o%d -out %s -- %s ' % (
            self.optipng_path,
            self.optipng_level,
            output_file,
            input_file,
        )
        with open(os.devnull) as null:
            logger.debug("[OPTIPNG] running: " + command)
            subprocess.call(command, shell=True, stdin=null)
