# thumbor-plugins
[![Build Status](https://travis-ci.org/thumbor/thumbor-plugins.svg?branch=master)](https://travis-ci.org/thumbor/thumbor-plugins)

## Install 
```
pip install thumbor-plugins
```

## Usage
after instaling thumbor-plugins,
just add the plugins you need to the OPTIMIZERS list on your thumbor.conf
```
OPTIMIZERS = [
    'thumbor_plugins.optimizers.pngcrush'
]
```

The [wiki](https://github.com/thumbor/thumbor-plugins/wiki) has a list of the available plugins.

## Development

```
make setup
make test

# code awesome things
# PR
```
