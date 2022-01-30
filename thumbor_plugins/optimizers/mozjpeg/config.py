from thumbor.config import Config

Config.define(
    'MOZJPEG_PATH',
    '/opt/mozjpeg/bin/cjpeg',
    'Path for the mozjpeg binary',
    'Optimizers'
)

Config.define(
    'MOZJPEG_QUALITY',
    '75',
    'Optimization level for mozjpeg (0-100)',
    'Optimizers'
)
