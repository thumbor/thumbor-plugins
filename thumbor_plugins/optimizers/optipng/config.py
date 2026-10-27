from thumbor.config import Config

Config.define(
    "OPTIPNG_PATH", "/usr/bin/optipng", "Path for the optipng binary", "Optimizers"
)

Config.define("OPTIPNG_LEVEL", 5, "Optimization level for optipng (1-7)", "Optimizers")

Config.define(
    "OPTIPNG_TIMEOUT",
    30,
    "Seconds to wait for optipng before serving the unoptimized image (0 disables)",
    "Optimizers",
)
