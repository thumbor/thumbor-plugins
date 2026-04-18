# thumbor-plugins

[![GitHub Actions - tests](https://github.com/thumbor/thumbor-plugins/actions/workflows/test.yml/badge.svg)](https://github.com/thumbor/thumbor-plugins/actions/workflows/test.yml)

`thumbor-plugins` is a monorepo of independently released
[Thumbor](https://github.com/thumbor/thumbor) optimizers. Each directory under
`thumbor_plugins/optimizers/` is its own Python package, with its own
changelog, tests, and release cycle.

The repository focuses on small, composable integrations that add image or
media optimization steps to a Thumbor deployment without forcing you to install
a single umbrella package. There is no all-in-one `thumbor-plugins`
distribution for runtime use; install the optimizer packages you actually want
to enable.

## What's in this repository

| Optimizer       | PyPI package                     | Thumbor module                              | What it does                           | Trigger                                     | Runtime dependency                           | Config                                                |
| --------------- | -------------------------------- | ------------------------------------------- | -------------------------------------- | ------------------------------------------- | -------------------------------------------- | ----------------------------------------------------- |
| GifV            | `thumbor-plugins-gifv`           | `thumbor_plugins.optimizers.gifv`           | Converts GIF requests into MP4 or WebM | Requests whose filter chain contains `gifv` | `ffmpeg`                                     | `FFMPEG_PATH`                                         |
| JP2             | `thumbor-plugins-jp2`            | `thumbor_plugins.optimizers.jp2`            | Writes JPEG 2000 output through Pillow | Requests whose filter chain contains `jp2`  | Pillow built with JPEG 2000/OpenJPEG support | `JP2_QUALITY`                                         |
| JPEG Recompress | `thumbor-plugins-jpegrecompress` | `thumbor_plugins.optimizers.jpegrecompress` | Runs `jpeg-recompress` for JPEGs       | Automatic for `.jpg` / `.jpeg`              | `jpeg-recompress`                            | `JPEGRECOMPRESS_PATH`                                 |
| MozJPEG         | `thumbor-plugins-mozjpeg`        | `thumbor_plugins.optimizers.mozjpeg`        | Runs `cjpeg` from MozJPEG for JPEGs    | Automatic for `.jpg` / `.jpeg`              | `cjpeg` from MozJPEG                         | `MOZJPEG_PATH`, `MOZJPEG_QUALITY`                     |
| OptiPNG         | `thumbor-plugins-optipng`        | `thumbor_plugins.optimizers.optipng`        | Runs `optipng` for PNGs                | Automatic for `.png`                        | `optipng`                                    | `OPTIPNG_PATH`, `OPTIPNG_LEVEL`                       |
| PNGCrush        | `thumbor-plugins-pngcrush`       | `thumbor_plugins.optimizers.pngcrush`       | Runs `pngcrush -reduce` for PNGs       | Automatic for `.png`                        | `pngcrush`                                   | `PNGCRUSH_PATH`                                       |
| PNGQuant        | `thumbor-plugins-pngquant`       | `thumbor_plugins.optimizers.pngquant`       | Runs `pngquant` for PNGs               | Automatic for `.png`                        | `pngquant`                                   | `PNGQUANT_PATH`, `PNGQUANT_QUALITY`, `PNGQUANT_SPEED` |

## Installation

Install only the packages you need:

```bash
pip install thumbor-plugins-mozjpeg
pip install thumbor-plugins-pngquant
pip install thumbor-plugins-gifv
```

Most optimizers are thin wrappers around native binaries, so `pip install` is
only part of the setup. Your Thumbor runtime image or host must also provide
the matching executable, such as `ffmpeg`, `pngquant`, `optipng`, `pngcrush`,
`jpeg-recompress`, or MozJPEG's `cjpeg`.

## Usage in Thumbor

After installing a package, add its module to the `OPTIMIZERS` list in
`thumbor.conf`:

```python
OPTIMIZERS = [
    "thumbor_plugins.optimizers.mozjpeg",
    "thumbor_plugins.optimizers.pngquant",
    "thumbor_plugins.optimizers.gifv",
]

MOZJPEG_PATH = "/opt/mozjpeg/bin/cjpeg"
MOZJPEG_QUALITY = "75"

PNGQUANT_PATH = "/usr/bin/pngquant"
PNGQUANT_QUALITY = "65-80"
PNGQUANT_SPEED = "1"

FFMPEG_PATH = "/usr/bin/ffmpeg"
```

How each optimizer behaves:

- `mozjpeg` and `jpegrecompress` run for JPEG requests.
- `pngquant`, `pngcrush`, and `optipng` run for PNG requests.
- `gifv` runs only when the request filter chain contains `gifv`.
- `jp2` runs when the request filter chain contains `jp2`.

### GifV examples

Convert a GIF into MP4:

```text
/unsafe/filters:gifv()/animated.gif
```

Convert a GIF into WebM:

```text
/unsafe/filters:gifv(webm)/animated.gif
```

Set a background color for transparent GIF frames:

```text
/unsafe/filters:gifv(mp4):background_color(ff00ff)/animated.gif
```

`background_color(...)` accepts normalized hex values, short hex values, or CSS
color names.

## Repository layout

```text
thumbor_plugins/
  optimizers/
    <plugin>/
      __init__.py
      config.py
      setup.py
      CHANGELOG.md
      tests/
  test_helpers/
```

Each optimizer directory is a standalone distributable package.
That split is intentional: you can ship only the plugins you need, version them
independently, and keep tests isolated per optimizer.

## Development

### Requirements

- Docker for integration tests
- Python 3

The test suite installs `thumbor==7.*` from `test_requirements.txt`.

### Running tests

Run integration and unit tests for a specific optimizer with:

```bash
make test_mozjpeg
make test_pngquant
make test_gifv
```

Run all unit tests with:

```bash
make test_unit
```

To iterate locally on a single optimizer package:

```bash
pip install -r test_requirements.txt
pip install -e thumbor_plugins/optimizers/pngquant
pytest thumbor_plugins/optimizers/pngquant/tests/unit
```

Each optimizer ships its own Dockerfile under
`thumbor_plugins/optimizers/<plugin>/tests/docker/`, and CI uses those
Dockerfiles to build the test matrix.

## Releasing

This repository uses
[release-please](https://github.com/googleapis/release-please) and expects
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Because
each optimizer is versioned independently, changes should stay scoped to the
package you are modifying whenever possible.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community guidelines.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

## Third-party assets

Integration tests use `bug.png` by [Marcelo Jorge Vieira](https://www.flickr.com/photos/marcelometal/540719764/),
licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
