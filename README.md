# thumbor-plugins
[![Github Actions - tests](https://github.com/thumbor/thumbor-plugins/actions/workflows/test.yml/badge.svg)](https://github.com/thumbor/thumbor-plugins/actions)
## What are thumbor-plugins
This monorepo contains multiple plugins that can be used on Thumbor, to add new capabilities, like GifV or mozjpeg compression.
Each of the optimizers are released, and can be installed separately.
The plugins can be found in: https://pypi.org/search/?q=%22thumbor-plugins%22&o=-created

## ⚙️ Installation
```
pip install thumbor-plugins-mozjpeg
pip install thumbor-plugins-gifv
```

## 🎯 Usage
after instaling the packages,
just add the plugins you need to the OPTIMIZERS list on your thumbor.conf
```
OPTIMIZERS = [
    'thumbor_plugins.optimizers.mozjpeg',
    'thumbor_plugins.optimizers.gifv',
]
```
Each optimizer contains parameters that can be used to configure how it runs.

## 👍 Contribute

thumbor-plugins is an open-source project with many contributors. Join them
[contributing code](https://github.com/thumbor/thumbor-plugins/blob/master/CONTRIBUTING.md).


## Breaking change
This repository used to be released under a single package in previous versions, `thumbor-plugins`

We broke down into multiple packages to make it easier for developers to contribute, test, and use different versions.

For example, the mozjpeg optimizer is released on the package `thumbor-plugins-mozjpeg`, and the Gifv one on the package `thumbor-plugins-gifv`

