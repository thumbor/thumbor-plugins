#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='thumbor-plugins-mozjpeg',
    version='0.0.1',
    keywords='thumbor optimizers mozjpeg',
    author='Guilherme Souza',
    author_email='guilherme@souza.tech',
    url='https://thumbor.readthedocs.io/en/latest/index.html',
    license='MIT',
    description='Thumbor optimizer to run mozjpeg',
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
    packages=[
        'thumbor_plugins.optimizers.mozjpeg',
    ],
    package_dir= {
        'thumbor_plugins.optimizers.mozjpeg': '.',
    },
)
