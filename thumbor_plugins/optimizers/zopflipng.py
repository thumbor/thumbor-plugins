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
        self.zopflipng_path = self.context.config.ZOPFLIPNG_PATH

        if not (os.path.isfile(self.zopflipng_path) and os.access(self.zopflipng_path, os.X_OK)):
            logger.error("ERROR zopflipng path '{0}' is not accessible".format(self.zopflipng_path))
            self.runnable = False

    def should_run(self, image_extension, buffer):
        return 'png' in image_extension and self.runnable

    def optimize(self, buffer, input_file, output_file):
        command = [
            self.zopflipng_path,
            '-y',
        ]

        if self.context.config.ZOPFLIPNG_COMPRESS_MORE:
            command += [
                '-m'
            ]

        if self.context.config.ZOPFLIPNG_LOSSY_TRANSPARENT:
            command += [
                '--lossy_transparent'
            ]

        if self.context.config.ZOPFLIPNG_LOSSY_8BIT:
            command += [
                '--lossy_8bit'
            ]

        command += [
            input_file,
            output_file
        ]

        with open(os.devnull) as null:
            logger.debug("[ZOPFLIPNG] running: %s" % " ".join(command))
            subprocess.call(command, stdin=null, stdout=null)
