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

Config.define(
    'AUTOJPEG_QUALITY',
    '90',
    'Quality level for autojpeg optimizer. Possible values: 0-100',
    'Optmizers'
)

Config.define(
    'AUTOJPEG_SUBSAMPLING',
    '0',
    'Quality level for autojpeg optimizer. Possible values: -1, 0, 1, 2. Keep original = -1, 4:4:4 = 0, 4:2:2 = 1, 4:1:1 = 2',
    'Optmizers'
)
