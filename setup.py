#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from setuptools import setup


setup(
    name="thumbor-plugins",
    version="0.1.0",
    keywords="imaging face detection feature thumbnail imagemagick pil opencv",
    author="globo.com",
    author_email="timehome@corp.globo.com",
    url="https://github.com/globocom/thumbor/wiki",
    license="MIT",
    description="Optimizers and filters contributed by the Thumbor community",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Graphics :: Presentation",
    ],
    packages=["thumbor_plugins", "thumbor_plugins.optimizers"],
    package_dir={"thumbor_plugins": "thumbor_plugins"},
    install_requires=[],
    extras_require={
        "tests": [
            "pytest>=6.2.5",
            "thumbor==7.*,>=7.0.6",
        ]
    },
)
