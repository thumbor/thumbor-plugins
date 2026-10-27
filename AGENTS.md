# AGENTS.md

thumbor-plugins is a monorepo of optimizers for
[thumbor](https://github.com/thumbor/thumbor), the smart imaging HTTP service.
An optimizer post-processes the image thumbor is about to serve, usually by
running an external binary such as `pngquant` or `ffmpeg` on it. Each
directory under `thumbor_plugins/optimizers/` is its own PyPI package
(`thumbor-plugins-<name>`) with its own `setup.py`, `CHANGELOG.md`, tests, and
release cycle. There is no root package to install.

## Dev Environment Setup

- **Prerequisites:** Python 3 and Docker. Docker is all you need for the full
  per-package test suite; CI builds one image per optimizer from
  `thumbor_plugins/optimizers/<plugin>/tests/docker/Dockerfile`
  (`python:3.12-slim` plus the binary that optimizer wraps).
- `make setup` installs the shared test requirements (`thumbor==7.*`,
  `pytest`, `pytest-cov`) and the lint tooling (`ruff`) on the host. To
  iterate on one optimizer, also install its package in editable mode:

  ```
  make setup
  pip install -e thumbor_plugins/optimizers/pngquant
  ```

  Integration tests also need the optimizer's binary on the host (`ffmpeg`
  and `gifsicle` for `gifv`, `cjpeg` for `mozjpeg`, `jpeg-recompress`,
  `optipng`, `pngcrush`, `pngquant`). `jp2` needs Pillow built with OpenJPEG
  support instead of a binary.

## Running tests

- One optimizer, the way CI runs it (builds the Docker image, installs the
  package, runs unit and integration tests with coverage):

  ```
  make test_<plugin>        # e.g. make test_pngquant, make test_gifv
  ```

- Every unit test, directly on the host:

  ```
  make test_unit
  ```

- A single package on the host:

  ```
  pytest thumbor_plugins/optimizers/pngquant/tests/unit
  pytest thumbor_plugins/optimizers/pngquant/tests/integration
  ```

- Unit tests mock `os.path.isfile`, `os.access`, and `subprocess.call`, so
  they run without the binary and assert the exact command line. Integration
  tests subclass `thumbor_plugins.test_helpers.engine.EngineCase`, which boots
  a real thumbor app (file loader, PIL engine, no storage) with the class
  attribute `optimizer` as the only entry in `OPTIMIZERS` and `fixtures_path`
  pointing at `tests/integration/imgs/`, then assert that the optimized
  response is smaller than the fixture (`gifv` asserts the video
  `Content-Type` instead).
- CI (`.github/workflows/test.yml`) builds its matrix by finding every
  `Dockerfile` under `thumbor_plugins/`, runs each package's tests in its own
  image, and uploads coverage to Coveralls. The release workflow does not
  look at Dockerfiles: it only releases the paths listed in
  `release-please-config.json`.

## Code style

- `ruff` is the formatter and linter, configured in `ruff.toml` (88 columns,
  black-compatible style, `E`/`F`/`W` rules). `make lint` runs `ruff check`
  and `ruff format --check`; `make format` rewrites files. The Lint workflow
  runs the same two commands on pushes to `master` and on every pull request.
- Each `__init__.py` imports its own `config` module for the side effect of
  registering the package's settings:

  ```
  import thumbor_plugins.optimizers.<plugin>.config  # noqa
  ```

## Project structure

```
thumbor_plugins/
  optimizers/
    <plugin>/
      __init__.py       ← Optimizer(BaseOptimizer) with should_run and optimize
      config.py         ← Config.define(...) for every <PLUGIN>_* setting
      setup.py          ← package metadata; release-please bumps version
      CHANGELOG.md      ← written by release-please, do not edit by hand
      tests/
        unit/           ← mocks the binary, runs anywhere
        integration/    ← runs thumbor against imgs/ fixtures, needs binary
        docker/         ← Dockerfile used by make test_<plugin> and by CI
  test_helpers/
    engine.py           ← EngineCase, the base class for integration tests
test_requirements.txt   ← thumbor, pytest, pytest-cov pins for every package
lint_requirements.txt   ← ruff pin used by make lint and the Lint workflow
ruff.toml               ← lint and format configuration
Makefile                ← make setup, lint, format, test_<plugin>, test_unit
.release-please-manifest.json ← current released version of each package
.github/workflows/      ← tests, release-please + PyPI publish (CodeQL
                           and stale exist but are disabled)
```

## How an optimizer works

- thumbor imports every module listed in `OPTIMIZERS` and instantiates its
  `Optimizer` class with the context. Before serving an image,
  `BaseOptimizer.run_optimizer` calls `should_run(image_extension,
  image_buffer)`; when it returns true, thumbor writes the image to a temp
  file, calls `optimize(image_buffer, input_file, output_file)`, and serves
  whatever was written to `output_file`.
- `should_run` is where format gating lives. `mozjpeg`, `jpegrecompress`,
  `optipng`, `pngcrush`, and `pngquant` match on the extension; `gifv`
  requires both the `.gif` extension and the `gifv` filter in
  `context.request.filters`; `jp2` checks only for the `jp2` filter (a
  substring match on the filter string) and runs for any output format.
- Optimizers that wrap a binary check the configured path (in `__init__`, or
  in `should_run` for `gifv`) and disable themselves with a logged error when
  it is missing or not executable (`gifv` only checks that the path exists
  and logs a warning), instead of failing the request.
- Settings are registered in `config.py` with
  `Config.define(name, default, description, "Optimizers")` and read from
  `self.context.config`.

## Contribution guidelines

- Commits must follow Conventional Commits; release-please reads them to open
  a release PR per package and to write that package's `CHANGELOG.md`. Scope
  each change to one package (`fix(pngquant): ...`) whenever possible, since
  release-please only looks at the commits that touch that package's
  directory.
- Never hand-edit a `CHANGELOG.md`, the `version` in a `setup.py`, or
  `.release-please-manifest.json`; the release PR changes all three. The
  only exception is adding a new package to the manifest.
- Every change must include tests. Run `make lint` and `make test_<plugin>`
  for the package you touched before opening a PR.
- To add an optimizer, copy an existing directory, rename the package in
  `setup.py`, `config.py` and the `config` import, give it a Dockerfile that
  installs its binary, register it in `release-please-config.json` and
  `.release-please-manifest.json`, and add it to the README table.
- Dependabot opens daily PRs for `test_requirements.txt`. A stale workflow
  is checked in, but GitHub disabled it for inactivity in June 2022, so it
  closes nothing.

## Security considerations

- Every optimizer except `jp2` executes an external program with thumbor's
  privileges on each matching request. All of them except `gifv` build the
  command as a string and run it through `subprocess.call(..., shell=True)`,
  interpolating the `*_PATH`, quality and speed settings plus the temp file
  paths. Those settings come from the operator's `thumbor.conf`; never let
  request data reach a shell string. `gifv` is the model for request-derived
  input: it parses `background_color` from the filters and passes it as a
  list argument with no shell.
- Optimizers run after thumbor has validated the URL signature and loaded the
  source image, so thumbor's own hardening (`SECURITY_KEY`,
  `ALLOW_UNSAFE_URL = False`, `ALLOWED_SOURCES`, `MAX_PIXELS`) decides which
  images ever reach a binary. The test helper deliberately uses
  `SECURITY_KEY="ACME-SEC"` and `/unsafe/` URLs.
- A CodeQL workflow is checked in, but GitHub disabled it for inactivity in
  June 2022 and it still pins `codeql-action@v1`; no code scanning runs
  today.
- Report vulnerabilities privately through GitHub's Private Vulnerability
  Reporting (the repository's Security tab), never in a public issue.
