#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup



setup(
    name="thumbor-plugins-jp2",
    version="0.1.4",
    keywords="thumbor optimizers jp2",
    author="Guilherme Souza",
    author_email="guilherme@souza.tech",
    url="https://github.com/thumbor/thumbor-plugins",
    license="MIT",
    description="Thumbor optimizer to run jp2",
    long_description="""
        Available Configs:
        - JP2_QUALITY

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
        "thumbor_plugins.optimizers.jp2",
    ],
    package_dir={
        "thumbor_plugins.optimizers.jp2": ".",
    },
)
