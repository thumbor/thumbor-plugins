# Security Policy

## Reporting a Vulnerability

The thumbor team takes security vulnerabilities seriously. If you discover a
security issue in any of the `thumbor-plugins-*` packages, please report it
responsibly.

Please **DO NOT open a public GitHub issue** for security vulnerabilities.

Instead, please report the vulnerability privately using GitHub's
**Private Vulnerability Reporting** feature:

- Go to the repository's **Security** tab
- Click **Report a vulnerability**
- Submit the details through the GitHub Security Advisory form

Include as much information as possible to help us reproduce the issue:

- Description of the vulnerability
- The affected optimizer package and its version
- Steps to reproduce
- Potential impact
- A proof of concept (PoC), if available
- Your environment (thumbor version, the wrapped binary and its version,
  configuration, deployment model)

We will acknowledge receipt of your report as soon as possible and work with
you to understand and resolve the issue.

Issues in thumbor itself belong to the
[thumbor security policy](https://github.com/thumbor/thumbor/security/policy),
and issues in the tools these optimizers wrap (`ffmpeg`, MozJPEG,
`jpeg-recompress`, `optipng`, `pngcrush`, `pngquant`) belong to their upstream
projects. If you are unsure where a problem lives, report it here and we will
help route it.

## Responsible Disclosure

We ask that you follow responsible disclosure practices:

- Do not publicly disclose the vulnerability before it has been addressed.
- Allow the maintainers reasonable time to investigate and fix the issue.
- Coordinate with us before publishing advisories, blog posts, or CVEs.

Once the issue is fixed, we will publicly acknowledge your contribution unless
you prefer to remain anonymous.

## Supported Versions

Each optimizer in this repository is versioned and released independently.
Security fixes are provided for the latest release of each
`thumbor-plugins-*` package.

| Version                        | Supported |
| ------------------------------ | --------- |
| Latest release of each package | ✅        |
| Older releases                 | ❌        |

Users are strongly encouraged to keep their thumbor-plugins packages, thumbor
itself, and the underlying optimizer binaries up to date.

## Security Considerations When Running thumbor-plugins

These optimizers run an external program on every image they process, with
the same privileges as the thumbor process. When deploying them in production,
please consider the following:

- Point each `*_PATH` setting (`FFMPEG_PATH`, `MOZJPEG_PATH`,
  `JPEGRECOMPRESS_PATH`, `OPTIPNG_PATH`, `PNGCRUSH_PATH`, `PNGQUANT_PATH`) at
  a trusted binary and keep that binary patched. A vulnerability in the
  underlying tool is reachable through any image thumbor is asked to optimize.
- Treat optimizer settings as trusted operator configuration. Paths and
  quality or speed values are passed to the binaries through a shell, so never
  populate them from untrusted input.
- Follow thumbor's own hardening guidance: use a strong `SECURITY_KEY`, set
  `ALLOW_UNSAFE_URL = False`, restrict `ALLOWED_SOURCES`, and place thumbor
  behind a reverse proxy or CDN with rate limiting. Optimizers only run on
  requests thumbor has already accepted, so URL signing is the first line of
  defense.
- Enable only the optimizers you need. Each one adds a process execution per
  matching request.

## Acknowledgements

We appreciate the efforts of security researchers and the open-source community
in responsibly reporting vulnerabilities and helping improve the security of
thumbor-plugins.
