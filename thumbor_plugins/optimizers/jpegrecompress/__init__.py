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

import thumbor_plugins.optimizers.jpegrecompress.config  # noqa

from thumbor.optimizers import BaseOptimizer
from thumbor.utils import logger


class Optimizer(BaseOptimizer):
    def __init__(self, context):
        super(Optimizer, self).__init__(context)

        self.runnable = True
        self.jpegrecompress_path = self.context.config.JPEGRECOMPRESS_PATH
        try:
            timeout = float(self.context.config.JPEGRECOMPRESS_TIMEOUT or 0)
            if timeout < 0 or not math.isfinite(timeout):
                raise ValueError(timeout)
            self.jpegrecompress_timeout = timeout or None
        except (TypeError, ValueError):
            logger.error(
                "ERROR jpegrecompress timeout '{0}' is not a finite number >= 0".format(
                    self.context.config.JPEGRECOMPRESS_TIMEOUT
                )
            )
            self.runnable = False

        if not (
            os.path.isfile(self.jpegrecompress_path)
            and os.access(self.jpegrecompress_path, os.X_OK)
        ):
            logger.error(
                "ERROR jpeg-recompress path '{0}' is not accessible".format(
                    self.jpegrecompress_path
                )
            )
            self.runnable = False

    def should_run(self, image_extension, buffer):
        return ("jpg" in image_extension or "jpeg" in image_extension) and self.runnable

    def optimize(self, buffer, input_file, output_file):
        command = [
            self.jpegrecompress_path,
            "--quiet",
            "--strip",
            "--accurate",
            "--loops",
            "10",
            input_file,
            output_file,
        ]
        logger.debug("[JPEG-RECOMPRESS] running: %s", " ".join(command))
        try:
            result = subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=self.jpegrecompress_timeout,
            )
        except subprocess.TimeoutExpired:
            logger.warning(
                "[JPEG-RECOMPRESS] timed out after %ss, serving the unoptimized image",
                self.jpegrecompress_timeout,
            )
            shutil.copyfile(input_file, output_file)
            return

        if result.returncode != 0 or os.path.getsize(output_file) == 0:
            logger.warning(
                "[JPEG-RECOMPRESS] exited with %s, serving the unoptimized image: %s",
                result.returncode,
                result.stderr.decode("utf-8", "replace").strip(),
            )
            shutil.copyfile(input_file, output_file)
