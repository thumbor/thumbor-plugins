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

Config.define(
    'JP2_QUALITY',
    '41',
    'Optimization level for jp2 optimizer',
    'Optimizers'
)

Config.define(
    'MOZJPEG_PATH',
    '/usr/local/bin/cjpeg',
    'Path for the mozjpeg binary',
    'Optimizers'
)

Config.define(
    'MOZJPEG_QUALITY',
    '75',
    'Optimization level for mozjpeg (0-100)',
    'Optimizers'
)