#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from setuptools import setup
from thumbor_png_optimizers import __version__


setup(
    name='thumbor-png-optimizers',
    version=__version__,
    keywords='imaging face detection feature thumbnail imagemagick pil opencv',
    author='globo.com',
    author_email='timehome@corp.globo.com',
    url='https://github.com/globocom/thumbor/wiki',
    license='MIT',
    description='Contributed extensions for Thumbor',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics :: Presentation'
    ],
    packages=['thumbor_png_optimizers'],
    package_dir={"thumbor_png_optimizers": "thumbor_png_optimizers"},
    install_requires=[
        'thumbor',
    ],
    extras_require={
        'tests': [
            'pyvows',
            'mock',
            'colorama',
        ]
    }
)
