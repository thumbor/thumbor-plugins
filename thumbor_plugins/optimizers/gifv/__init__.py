#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

import math
import os
import re
import shutil
import subprocess
from os.path import exists

import webcolors

import thumbor_plugins.optimizers.gifv.config  # noqa

from thumbor.optimizers import BaseOptimizer
from thumbor.utils import logger

GIFV_FILTER = re.compile(r"(?:^|:)gifv(?:\(\s*(?:((?i:mp4|webm))\s*)?\))?(?:$|:)")
BACKGROUND_COLOR_FILTER = re.compile(r"(?:^|:)background_color\(([^)]*)\)")


class Optimizer(BaseOptimizer):
    def should_run(self, image_extension, image_buffer):
        if "gif" in image_extension and self.gifv_filter_argument() is not None:
            if not exists(self.context.config.FFMPEG_PATH):
                logger.warning(
                    "gifv optimizer enabled but binary FFMPEG_PATH does not exist"
                )
                return False
            try:
                self.ffmpeg_timeout()
            except (TypeError, ValueError):
                logger.warning(
                    "gifv optimizer enabled but FFMPEG_TIMEOUT "
                    "is not a finite number >= 0"
                )
                return False
            return True
        return False

    def ffmpeg_timeout(self):
        timeout = float(self.context.config.FFMPEG_TIMEOUT or 0)
        if timeout < 0 or not math.isfinite(timeout):
            raise ValueError(timeout)
        return timeout or None

    def request_filters(self):
        filters = self.context.request.filters
        if isinstance(filters, str):
            return filters
        return ":".join(filters or [])

    def gifv_filter_argument(self):
        match = GIFV_FILTER.search(self.request_filters())
        if match is None:
            return None
        return (match.group(1) or "").lower()

    def background_color(self):
        match = BACKGROUND_COLOR_FILTER.search(self.request_filters())
        if match is None:
            return None
        return self.normalize_color_to_hex(match.group(1).strip())

    def optimize(self, image_buffer, input_file, output_file):
        file_format, command_params = self.set_format()
        bg_color_hex = self.background_color()

        command = [
            self.context.config.FFMPEG_PATH,
            "-y",
            "-f",
            "gif",
            "-trans_color",
            f"0xff{(bg_color_hex[1:] if bg_color_hex else 'ffffff')}",
            "-i",
            input_file,
            "-filter_complex",
            "scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-an",
            "-movflags",
            "faststart",
            "-f",
            file_format,
            "-pix_fmt",
            "yuv420p",
        ]

        command += command_params

        command += [
            "-qmin",
            "10",
            "-qmax",
            "42",
            "-crf",
            "23",
            "-maxrate",
            "500k",
            output_file,
            "-loglevel",
            "error",
        ]

        timeout = self.ffmpeg_timeout()
        try:
            result = subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            logger.warning(
                "[GIFV] ffmpeg timed out after %ss, serving the original gif", timeout
            )
            shutil.copyfile(input_file, output_file)
            return

        if result.returncode != 0 or os.path.getsize(output_file) == 0:
            logger.warning(
                "[GIFV] ffmpeg exited with %s, serving the original gif: %s",
                result.returncode,
                result.stderr.decode("utf-8", "replace").strip(),
            )
            shutil.copyfile(input_file, output_file)
            return

        self.context.request.format = file_format

    def set_format(self):
        if self.gifv_filter_argument() == "webm":
            file_format = "webm"
            command_params = [
                "-quality",
                "good",
                "-cpu-used",
                "4",
                "-b:v",
                "500k",
            ]
        else:
            file_format = "mp4"
            command_params = ["-profile:v", "baseline", "-level", "4.0"]
        return file_format, command_params

    def normalize_color_to_hex(self, color_string):
        try:
            return webcolors.normalize_hex("#" + color_string)
        except ValueError:
            pass

        try:
            return webcolors.name_to_hex(color_string)
        except ValueError:
            pass

        try:
            return webcolors.normalize_hex(color_string)
        except ValueError:
            pass

        if color_string:
            logger.error("background_color value could not be parsed")

        return None
