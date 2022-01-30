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

Config.define(
    'PNGQUANT_PATH',
    '/usr/local/bin/pngquant',
    'Path for the pngquant binary',
    'Optimizers'
)

Config.define(
    'PNGQUANT_QUALITY',
    '65-80',
    'Optimization level for pngquant ([0..100]-[0..100])',
    'Optimizers'
)

Config.define(
    'PNGQUANT_SPEED',
    '1',
    'Optimization speed for pngquant 1-11, 1 is slowest',
    'Optimizers'
)

Config.define(
    'IMGMIN_PATH',
    '/usr/local/bin/imgmin',
    'Path for the imgmin binary',
    'Optimizers'
)
