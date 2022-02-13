from thumbor.config import Config

Config.define(
    "JPEGRECOMPRESS_PATH",
    "/usr/bin/jpeg-recompress",
    "Path for the jpeg-recompress binary",
    "Optimizers",
)
