#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

__version__ = "0.1.0"

from thumbor.config import Config

Config.define(
    'PNGCRUSH_PATH',
    '/usr/local/bin/pngcrush',
    'Path for the pngcrush binary',
    'Optimizers'
)

Config.define(
    'OPTIPNG_PATH',
    '/usr/bin/optipng',
    'Path for the optipng binary',
    'Optimizers'
)

Config.define(
    'OPTIPNG_LEVEL',
    5,
    'Optimization level for optipng (0-7)',
    'Optimizers'
)
