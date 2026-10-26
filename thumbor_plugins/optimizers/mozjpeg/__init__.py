#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license


import math
import os
import shutil
import subprocess

import thumbor_plugins.optimizers.mozjpeg.config  # noqa

from thumbor.optimizers import BaseOptimizer
from thumbor.utils import logger
from PIL import Image


class Optimizer(BaseOptimizer):
    def __init__(self, context):
        super(Optimizer, self).__init__(context)

        self.runnable = True
        self.mozjpeg_path = self.context.config.MOZJPEG_PATH
        self.mozjpeg_level = self.context.config.MOZJPEG_QUALITY or "75"
        try:
            timeout = float(self.context.config.MOZJPEG_TIMEOUT or 0)
            if timeout < 0 or not math.isfinite(timeout):
                raise ValueError(timeout)
            self.mozjpeg_timeout = timeout or None
        except (TypeError, ValueError):
            logger.error(
                "ERROR mozjpeg timeout '{0}' is not a finite number >= 0".format(
                    self.context.config.MOZJPEG_TIMEOUT
                )
            )
            self.runnable = False

        if not (
            os.path.isfile(self.mozjpeg_path) and os.access(self.mozjpeg_path, os.X_OK)
        ):
            logger.error(
                "ERROR mozjpeg path '{0}' is not accessible".format(self.mozjpeg_path)
            )
            self.runnable = False

    def should_run(self, image_extension, buffer):
        return ("jpg" in image_extension or "jpeg" in image_extension) and self.runnable

    def optimize(self, buffer, input_file, output_file):
        intermediary = output_file + "-intermediate"
        Image.open(input_file).save(intermediary, "tga")
        command = [
            self.mozjpeg_path,
            "-quality",
            str(self.mozjpeg_level),
            "-optimize",
            "-outfile",
            output_file,
            intermediary,
        ]
        logger.debug("[MOZJPEG] running: %s", " ".join(command))
        try:
            result = subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=self.mozjpeg_timeout,
            )
        except subprocess.TimeoutExpired:
            logger.warning(
                "[MOZJPEG] timed out after %ss, serving the unoptimized image",
                self.mozjpeg_timeout,
            )
            shutil.copyfile(input_file, output_file)
            return
        finally:
            if os.path.exists(intermediary):
                os.unlink(intermediary)

        if result.returncode != 0 or os.path.getsize(output_file) == 0:
            logger.warning(
                "[MOZJPEG] exited with %s, serving the unoptimized image: %s",
                result.returncode,
                result.stderr.decode("utf-8", "replace").strip(),
            )
            shutil.copyfile(input_file, output_file)
