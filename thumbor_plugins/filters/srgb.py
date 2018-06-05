#!/usr/bin/python
# -*- coding: utf-8 -*-


import thumbor.filters
from thumbor.filters import BaseFilter, filter_method
from thumbor.utils import logger
from thumbor.engines.pil import Engine as PILEngine

from io import BytesIO

try:
    from PIL import ImageCms
except:
    ImageCms = None

# See http://pippin.gimp.org/sRGBz/
tiny_srgb = bytearray([0, 0, 1, 235, 98, 97, 98, 108, 2, 32, 0, 4, 109, 110, 116, 114, 82, 71, 66, 32, 88, 89, 90, 32,
                       7, 225, 0, 9, 0, 20, 0, 0, 0, 0, 0, 0, 97, 99, 115, 112, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 246, 214, 0, 1, 0, 0, 0, 0, 211, 45, 98, 97,
                       98, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 119, 116, 112, 116, 0, 0, 0, 240, 0, 0,
                       0, 20, 114, 88, 89, 90, 0, 0, 1, 4, 0, 0, 0, 20, 103, 88, 89, 90, 0, 0, 1, 24, 0, 0, 0, 20, 98,
                       88, 89, 90, 0, 0, 1, 44, 0, 0, 0, 20, 114, 84, 82, 67, 0, 0, 1, 64, 0, 0, 0, 64, 103, 84, 82, 67,
                       0, 0, 1, 64, 0, 0, 0, 64, 98, 84, 82, 67, 0, 0, 1, 64, 0, 0, 0, 64, 99, 112, 114, 116, 0, 0, 1,
                       128, 0, 0, 0, 12, 100, 101, 115, 99, 0, 0, 1, 140, 0, 0, 0, 95, 88, 89, 90, 32, 0, 0, 0, 0, 0, 0,
                       243, 81, 0, 1, 0, 0, 0, 1, 22, 204, 88, 89, 90, 32, 0, 0, 0, 0, 0, 0, 111, 161, 0, 0, 56, 246, 0,
                       0, 3, 145, 88, 89, 90, 32, 0, 0, 0, 0, 0, 0, 98, 151, 0, 0, 183, 135, 0, 0, 24, 218, 88, 89, 90,
                       32, 0, 0, 0, 0, 0, 0, 36, 158, 0, 0, 15, 131, 0, 0, 182, 194, 99, 117, 114, 118, 0, 0, 0, 0, 0,
                       0, 0, 26, 0, 0, 0, 202, 1, 199, 3, 96, 5, 143, 8, 106, 11, 244, 16, 60, 21, 78, 27, 48, 33, 241,
                       41, 141, 50, 21, 59, 143, 70, 0, 81, 119, 93, 234, 107, 109, 122, 1, 137, 175, 154, 125, 172,
                       100, 191, 122, 211, 192, 233, 47, 255, 255, 116, 101, 120, 116, 0, 0, 0, 0, 67, 67, 48, 0, 100,
                       101, 115, 99, 0, 0, 0, 0, 0, 0, 0, 6, 115, 82, 71, 66, 122, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, ])


class Filter(BaseFilter):
    phase = thumbor.filters.PHASE_AFTER_LOAD

    @filter_method()
    def srgb(self):
        try:
            if not isinstance(self.engine, PILEngine):
                logger.warn('Could not perform profileToProfile conversion: engine is not PIL engine')
                return

            if (ImageCms is None):
                logger.warn('ImageCms is not installed. Could not perform profileToProfile conversion')
                return

            image = self.engine.image

            embedded_profile = image.info.get('icc_profile')

            if not embedded_profile:
                logger.debug('Image does not have embedded profile. Assuming already in sRGB')
                return

            embedded_profile = BytesIO(embedded_profile)
            srgb_profile = BytesIO(tiny_srgb)

            output_mode = 'RGBA' if 'A' in image.mode else 'RGB'
            image = ImageCms.profileToProfile(image, embedded_profile, srgb_profile, renderingIntent=0,
                                              outputMode=output_mode)

            self.engine.image = image
            self.engine.icc_profile = image.info.get('icc_profile')
        except Exception as err:
            logger.exception(err)

