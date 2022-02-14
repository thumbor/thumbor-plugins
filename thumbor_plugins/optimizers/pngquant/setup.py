#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup



setup(
    name="thumbor-plugins-pngquant",
    version="0.1.1",
    keywords="thumbor optimizers pngquant",
    author="Guilherme Souza",
    author_email="guilherme@souza.tech",
    url="https://thumbor.readthedocs.io/en/latest/index.html",
    license="MIT",
    description="Thumbor optimizer to run pngquant",
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
        "thumbor_plugins.optimizers.pngquant",
    ],
    package_dir={
        "thumbor_plugins.optimizers.pngquant": ".",
    },
)
