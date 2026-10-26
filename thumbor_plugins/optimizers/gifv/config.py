from thumbor.config import Config

Config.define(
    "FFMPEG_PATH",
    "/usr/local/bin/ffmpeg",
    "Path for the ffmpeg binary used to generate gifv(h.264)",
    "Optimizers",
)

Config.define(
    "FFMPEG_TIMEOUT",
    60,
    "Seconds to wait for ffmpeg before serving the original gif (0 disables)",
    "Optimizers",
)
