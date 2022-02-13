from thumbor.config import Config

Config.define(
    "PNGQUANT_PATH", "/usr/bin/pngquant", "Path for the pngquant binary", "Optimizers"
)

Config.define(
    "PNGQUANT_QUALITY",
    "65-80",
    "Optimization level for pngquant ([0..100]-[0..100])",
    "Optimizers",
)

Config.define(
    "PNGQUANT_SPEED",
    "1",
    "Optimization speed for pngquant 1-11, 1 is slowest",
    "Optimizers",
)
