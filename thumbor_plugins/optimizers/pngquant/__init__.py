#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license


import math
import os
import re
import shutil
import subprocess

import thumbor_plugins.optimizers.pngquant.config  # noqa

from thumbor.optimizers import BaseOptimizer
from thumbor.utils import logger

QUALITY_TOO_LOW = 99
QUALITY = re.compile(r"^(\d{1,3})?(?:-(\d{1,3})?)?$")


class Optimizer(BaseOptimizer):
    def __init__(self, context):
        super(Optimizer, self).__init__(context)

        self.runnable = True
        self.pngquant_path = self.context.config.PNGQUANT_PATH
        self.pngquant_quality = str(self.context.config.PNGQUANT_QUALITY or "65-80")
        try:
            timeout = float(self.context.config.PNGQUANT_TIMEOUT or 0)
            if timeout < 0 or not math.isfinite(timeout):
                raise ValueError(timeout)
            self.pngquant_timeout = timeout or None
        except (TypeError, ValueError):
            logger.error(
                "ERROR pngquant timeout '{0}' is not a finite number >= 0".format(
                    self.context.config.PNGQUANT_TIMEOUT
                )
            )
            self.runnable = False

        if not (
            os.path.isfile(self.pngquant_path)
            and os.access(self.pngquant_path, os.X_OK)
        ):
            logger.error(
                "ERROR pngquant path '{0}' is not accessible".format(self.pngquant_path)
            )
            self.runnable = False

        if not self.valid_quality(self.pngquant_quality):
            logger.error(
                "ERROR pngquant quality '{0}' is not min-max within 0-100".format(
                    self.pngquant_quality
                )
            )
            self.runnable = False

        try:
            self.pngquant_speed = int(self.context.config.PNGQUANT_SPEED or 3)
            if not 1 <= self.pngquant_speed <= 11:
                raise ValueError(self.pngquant_speed)
        except (TypeError, ValueError):
            logger.error(
                "ERROR pngquant speed '{0}' is not an integer between 1 and 11".format(
                    self.context.config.PNGQUANT_SPEED
                )
            )
            self.runnable = False

    @staticmethod
    def valid_quality(quality):
        match = QUALITY.match(quality)
        if match is None:
            return False
        values = [int(value) for value in match.groups() if value is not None]
        return bool(values) and max(values) <= 100 and values == sorted(values)

    def should_run(self, image_extension, buffer):
        return "png" in image_extension and self.runnable

    def optimize(self, buffer, input_file, output_file):
        command = [
            self.pngquant_path,
            "--speed",
            str(self.pngquant_speed),
            "--quality=%s" % self.pngquant_quality,
            "-",
        ]
        logger.debug("[PNGQUANT] running: %s", " ".join(command))
        try:
            with open(input_file, "rb") as stdin, open(output_file, "wb") as stdout:
                result = subprocess.run(
                    command,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=subprocess.PIPE,
                    timeout=self.pngquant_timeout,
                )
        except subprocess.TimeoutExpired:
            logger.warning(
                "[PNGQUANT] timed out after %ss, serving the unoptimized image",
                self.pngquant_timeout,
            )
            shutil.copyfile(input_file, output_file)
            return

        if result.returncode == QUALITY_TOO_LOW:
            logger.debug("[PNGQUANT] quality target not met, serving the original")
            shutil.copyfile(input_file, output_file)
        elif result.returncode != 0 or os.path.getsize(output_file) == 0:
            logger.warning(
                "[PNGQUANT] exited with %s, serving the unoptimized image: %s",
                result.returncode,
                result.stderr.decode("utf-8", "replace").strip(),
            )
            shutil.copyfile(input_file, output_file)
