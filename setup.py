#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the Python KISS Module.

Source:: https://github.com/ampledata/kiss
"""

import os
import setuptools
import sys

__title__ = 'kiss'
__version__ = '7.0.0b1'
__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Greg Albrecht and Contributors'  # NOQA pylint: disable=R0801
__license__ = 'Apache License, Version 2.0'  # NOQA pylint: disable=R0801


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist')
        os.system('twine upload dist/*')
        sys.exit()


publish()


setuptools.setup(
    name=__title__,
    version=__version__,
    description='Python KISS Module.',
    author='Greg Albrecht',
    author_email='oss@undef.net',
    packages=['kiss'],
    package_data={'': ['LICENSE']},
    package_dir={'kiss': 'kiss'},
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    url='https://github.com/ampledata/kiss',
    zip_safe=False,
    setup_requires=[
        'coverage >= 4.4.1',
        'nose >= 1.3.7',
        'dummyserial >= 1.0.0',
        'aprs > 6.9',
        'mocket >= 1.8.2'
    ],
    install_requires=['pyserial >= 3.4'],
    classifiers=[
        'Topic :: Communications :: Ham Radio',
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License'
    ],
    keywords=[
        'Ham Radio', 'APRS', 'KISS'
    ]
)
