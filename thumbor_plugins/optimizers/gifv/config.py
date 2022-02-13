from thumbor.config import Config

Config.define(
    "FFMPEG_PATH",
    "/usr/local/bin/ffmpeg",
    "Path for the ffmpeg binary used to generate gifv(h.264)",
    "Optimizers",
)
