#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup



setup(
    name="thumbor-plugins-optipng",
    version="0.1.5",
    keywords="thumbor optimizers optipng",
    author="Guilherme Souza",
    author_email="guilherme@souza.tech",
    url="https://github.com/thumbor/thumbor-plugins",
    license="MIT",
    description="Thumbor optimizer to run optipng",
    long_description="""
        Available Configs:
        - OPTIPNG_PATH
        - OPTIPNG_LEVEL

        This package is part of the thumbor-plugins repository.
        For more information, visit: https://github.com/thumbor/thumbor-plugins
    """,
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
    packages=[
        "thumbor_plugins.optimizers.optipng",
    ],
    package_dir={
        "thumbor_plugins.optimizers.optipng": ".",
    },
)
