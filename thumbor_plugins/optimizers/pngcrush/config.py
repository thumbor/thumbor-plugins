from thumbor.config import Config

Config.define(
    "PNGCRUSH_PATH", "/usr/bin/pngcrush", "Path for the pngcrush binary", "Optimizers"
)

Config.define(
    "PNGCRUSH_TIMEOUT",
    30,
    "Seconds to wait for pngcrush before serving the unoptimized image (0 disables)",
    "Optimizers",
)
