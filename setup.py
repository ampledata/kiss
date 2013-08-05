#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for kiss.

Source:: https://github.com/ampledata/kiss
"""

__author__ = 'Greg Albrecht W2GMD <gba@onbeep.com>'
__copyright__ = 'Copyright 2013 Onbeep, Inc.'
__license__ = 'Apache License 2.0'


import setuptools


def read_readme():
    """Reads in README file for use in setuptools."""
    with open('README.rst') as rmf:
        rmf.read()


setuptools.setup(
    name='kiss',
    version='0.0.1',
    description='KISS is a protocol for communicating with a ' +
                'serial TNC device used for Amateur Radio.',
    author='Greg Albrecht',
    author_email='gba@onbeep.com',
    long_description='A Python implementation of the KISS Protocol ' +
                     'for communicating with serial TNC devices for ' +
                     'use with Amateur Radio.',
    license='Apache License 2.0',
    copyright='Copyright 2013 OnBeep, Inc.',
    url='https://github.com/ampledata/kiss',
    setup_requires=['nose'],
    tests_require=['coverage', 'nose'],
    install_requires=['pyserial']
)
