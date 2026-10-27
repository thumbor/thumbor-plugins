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

import thumbor_plugins.optimizers.optipng.config  # noqa

from thumbor.optimizers import BaseOptimizer
from thumbor.utils import logger


class Optimizer(BaseOptimizer):
    def __init__(self, context):
        super(Optimizer, self).__init__(context)

        self.runnable = True
        self.optipng_path = self.context.config.OPTIPNG_PATH
        try:
            timeout = float(self.context.config.OPTIPNG_TIMEOUT or 0)
            if timeout < 0 or not math.isfinite(timeout):
                raise ValueError(timeout)
            self.optipng_timeout = timeout or None
        except (TypeError, ValueError):
            logger.error(
                "ERROR optipng timeout '{0}' is not a finite number >= 0".format(
                    self.context.config.OPTIPNG_TIMEOUT
                )
            )
            self.runnable = False

        if not (
            os.path.isfile(self.optipng_path) and os.access(self.optipng_path, os.X_OK)
        ):
            logger.error(
                "ERROR optipng path '{0}' is not accessible".format(self.optipng_path)
            )
            self.runnable = False

        try:
            # optipng treats any level above 7 like -o7, and -o0 with -force exits 1
            # with "IDAT recoding is necessary, but is disabled by the user"
            self.optipng_level = min(int(self.context.config.OPTIPNG_LEVEL), 7)
            if self.optipng_level < 1:
                raise ValueError(self.optipng_level)
        except (TypeError, ValueError):
            logger.error(
                "ERROR optipng level '{0}' is not an integer of 1 or more".format(
                    self.context.config.OPTIPNG_LEVEL
                )
            )
            self.runnable = False

    def should_run(self, image_extension, buffer):
        return "png" in image_extension and self.runnable

    def optimize(self, buffer, input_file, output_file):
        command = [
            self.optipng_path,
            "-fix",
            "-preserve",
            "-force",
            "-keep",
            "-o%d" % self.optipng_level,
            "-out",
            output_file,
            "--",
            input_file,
        ]
        logger.debug("[OPTIPNG] running: %s", " ".join(command))
        try:
            result = subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=self.optipng_timeout,
            )
        except subprocess.TimeoutExpired:
            logger.warning(
                "[OPTIPNG] timed out after %ss, serving the unoptimized image",
                self.optipng_timeout,
            )
            shutil.copyfile(input_file, output_file)
            return
        finally:
            # optipng refuses to overwrite the output file thumbor pre-created
            # unless -keep is given, which renames it to <output>.bak and never
            # deletes that copy
            try:
                os.remove(output_file + ".bak")
            except FileNotFoundError:
                pass

        if result.returncode != 0 or os.path.getsize(output_file) == 0:
            logger.warning(
                "[OPTIPNG] exited with %s, serving the unoptimized image: %s",
                result.returncode,
                result.stderr.decode("utf-8", "replace").strip(),
            )
            shutil.copyfile(input_file, output_file)
