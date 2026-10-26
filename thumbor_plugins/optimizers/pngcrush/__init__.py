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

import thumbor_plugins.optimizers.pngcrush.config  # noqa

from thumbor.optimizers import BaseOptimizer
from thumbor.utils import logger


class Optimizer(BaseOptimizer):
    def __init__(self, context):
        super(Optimizer, self).__init__(context)

        self.runnable = True
        self.pngcrush_path = self.context.config.PNGCRUSH_PATH
        try:
            timeout = float(self.context.config.PNGCRUSH_TIMEOUT or 0)
            if timeout < 0 or not math.isfinite(timeout):
                raise ValueError(timeout)
            self.pngcrush_timeout = timeout or None
        except (TypeError, ValueError):
            logger.error(
                "ERROR pngcrush timeout '{0}' is not a finite number >= 0".format(
                    self.context.config.PNGCRUSH_TIMEOUT
                )
            )
            self.runnable = False

        if not (
            os.path.isfile(self.pngcrush_path)
            and os.access(self.pngcrush_path, os.X_OK)
        ):
            logger.error(
                "ERROR pngcrush path '{0}' is not accessible".format(self.pngcrush_path)
            )
            self.runnable = False

    def should_run(self, image_extension, buffer):
        return "png" in image_extension and self.runnable

    def optimize(self, buffer, input_file, output_file):
        command = [self.pngcrush_path, "-reduce", "-q", input_file, output_file]
        logger.debug("[PNGCRUSH] running: %s", " ".join(command))
        try:
            result = subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=self.pngcrush_timeout,
            )
        except subprocess.TimeoutExpired:
            logger.warning(
                "[PNGCRUSH] timed out after %ss, serving the unoptimized image",
                self.pngcrush_timeout,
            )
            shutil.copyfile(input_file, output_file)
            return

        if result.returncode != 0:
            logger.warning(
                "[PNGCRUSH] exited with %s, serving the unoptimized image: %s",
                result.returncode,
                result.stderr.decode("utf-8", "replace").strip(),
            )
            shutil.copyfile(input_file, output_file)
        elif os.path.getsize(output_file) == 0:
            logger.warning(
                "[PNGCRUSH] produced no output, serving the unoptimized image: %s",
                result.stderr.decode("utf-8", "replace").strip(),
            )
            shutil.copyfile(input_file, output_file)
