from thumbor.config import Config

Config.define(
    "JPEGRECOMPRESS_PATH",
    "/usr/bin/jpeg-recompress",
    "Path for the jpeg-recompress binary",
    "Optimizers",
)

Config.define(
    "JPEGRECOMPRESS_TIMEOUT",
    30,
    "Seconds to wait for jpeg-recompress before serving the unoptimized image "
    "(0 disables)",
    "Optimizers",
)
