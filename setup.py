#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

import sys
from setuptools import setup
from thumbor_plugins import __version__

extras_require={
    'tests': [
        'tornado-pyvows>=0.6.0',
        'coverage',
        'mock',
        'colorama',
        # https://github.com/python-pillow/Pillow/issues/2609
        'pillow<4.2.0',
        'nose'
    ]
}

# https://pypi.org/project/gevent/
if sys.version_info == (2,5):
    extras_require['tests'].insert(0, 'gevent>=1.0,<1.1')
elif sys.version_info == (2,6):
    extras_require['tests'].insert(0, 'gevent>=1.1,<1.2')
elif sys.version_info <= (2, 7, 8):
    extras_require['tests'].insert(0, 'gevent>=1.2,<1.3')
elif sys.version_info <= (3,4) and sys.version_info >= (3,3):
    extras_require['tests'].insert(0, 'gevent==1.2')
else:
    extras_require['tests'].insert(0, 'gevent')

setup(
    name='thumbor-plugins',
    version=__version__,
    keywords='imaging face detection feature thumbnail imagemagick pil opencv',
    author='globo.com',
    author_email='timehome@corp.globo.com',
    url='https://github.com/globocom/thumbor/wiki',
    license='MIT',
    description='Optimizers and filters contributed by the Thumbor community',
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
    packages=['thumbor_plugins', 'thumbor_plugins.optimizers'],
    package_dir={"thumbor_plugins": "thumbor_plugins"},
    install_requires=[
        'thumbor',
    ],
    extras_require=extras_require
)
