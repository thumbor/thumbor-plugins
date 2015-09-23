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

        self.runnable = True
        self.mozjpeg_path = self.context.config.MOZJPEG_PATH
        self.mozjpeg_level = self.context.config.MOZJPEG_QUALITY or '75'

        if not (os.path.isfile(self.mozjpeg_path) and os.access(self.mozjpeg_path, os.X_OK)):
            logger.error("ERROR mozjpeg path '{0}' is not accessible".format(self.mozjpeg_path))
            self.runnable = False

    def should_run(self, image_extension, buffer):
        return ('jpg' in image_extension or 'jpeg' in image_extension) and self.runnable

    def optimize(self, buffer, input_file, output_file):
        intermediary = output_file + '-intermediate'
        Image.open(input_file).save(intermediary, 'tga')
        command = '%s -quality %s -optimize %s > %s' % (
            self.mozjpeg_path,
            self.mozjpeg_level,
            intermediary,
            output_file,
        )
        with open(os.devnull) as null:
            logger.debug("[MOZJPEG] running: " + command)
            subprocess.call(command, shell=True, stdin=null)
