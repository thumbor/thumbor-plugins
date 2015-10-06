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
from PIL import Image, ImageStat

class Optimizer(BaseOptimizer):
    def __init__(self, context):
        super(Optimizer, self).__init__(context)

        self.runnable = True
        self.imgmin_path = self.context.config.IMGMIN_PATH

        if not ( os.path.isfile(self.imgmin_path) ):
            logger.error("ERROR path '{0}' or '{1}' is not accessible".format(self.imgmin_path))
            self.runnable = False

    def should_run(self, image_extension, buffer):
        return self.runnable and 'auto' in self.context.request.filters and ('png' in image_extension or 'jpg' in image_extension or 'jpeg' in image_extension)

    def optimize(self, buffer, input_file, output_file):
        input_image = Image.open(input_file)
        stats = ImageStat.Stat(input_image).extrema
        has_alpha = False
        if len(stats) > 3 and (stats[3][0] < 255):
            has_alpha = True

        if has_alpha == False:
            intermediary = output_file + '-intermediate'
            input_image.save(intermediary, 'JPEG')
            input_file = intermediary

        command = '%s %s %s > /dev/null 2>&1' % (
            self.imgmin_path,
            input_file,
            output_file,
        )
        with open(os.devnull) as null:
            logger.debug("[AUTO IMGMIN] running: " + command)
            subprocess.call(command, shell=True, stdin=null)