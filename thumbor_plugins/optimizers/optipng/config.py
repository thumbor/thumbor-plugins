from thumbor.config import Config

Config.define(
    "OPTIPNG_PATH", "/usr/bin/optipng", "Path for the optipng binary", "Optimizers"
)

Config.define("OPTIPNG_LEVEL", 5, "Optimization level for optipng (0-7)", "Optimizers")
