# thumbor-plugins
[![Github Actions - tests](https://github.com/thumbor/thumbor-plugins/actions/workflows/test.yml/badge.svg)](https://github.com/thumbor/thumbor-plugins/actions)
## What are thumbor-plugins
You can add these plugins to Thumbor to get new features, like mozjpeg or gifv optimizer.

## Breaking change
This repository used to be released under a single package in previous versions, `thumbor-plugins`

We broke down into multiple packages to make it easier for developers to contribute, test, and use different versions.

For example, the mozjpeg optimizer is released on the package `thumbor-plugins-mozjpeg`, and the Gifv one on the package `thumbor-plugins-gifv`

## Install
```
pip install thumbor-plugins-mozjpeg
pip install thumbor-plugins-gifv
```

## Usage
after instaling the packages,
just add the plugins you need to the OPTIMIZERS list on your thumbor.conf
```
OPTIMIZERS = [
    'thumbor_plugins.optimizers.mozjpeg',
    'thumbor_plugins.optimizers.gifv',
]
```
