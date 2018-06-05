#!/usr/bin/python
# -*- coding: utf-8 -*-

from thumbor.filters import BaseFilter, filter_method
from thumbor.utils import logger


def is_webp(context):
    return (context.config.AUTO_WEBP and
            context.request.accepts_webp and
            not context.request.engine.is_multiple() and
            context.request.engine.can_convert_to_webp())


class Filter(BaseFilter):
    @filter_method()
    def format_auto(self):
        if is_webp(self.context):
            self.context.request.format = 'webp'
            logger.debug('Webp is supported, using webp')
        elif not self.context.request.engine.is_multiple():
            self.context.request.format = 'jpg'
            logger.debug('Webp is not supported, using jpg')
