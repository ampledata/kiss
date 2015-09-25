#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the KISS Python Module.

Source:: https://github.com/ampledata/kiss
"""

__title__ = 'kiss'
__version__ = '3.0.0'
__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.co>'
__copyright__ = 'Copyright 2015 Orion Labs, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


import os
import sys


try:
    from setuptools import setup
except ImportError:
    # pylint: disable=F0401,E0611
    from distutils.core import setup


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist upload')
        sys.exit()


publish()


setup(
    name=__title__,
    version=__version__,
    description='KISS Python Module.',
    long_description=open('README.rst').read(),
    author='Greg Albrecht',
    author_email='gba@orionlabs.co',
    license=open('LICENSE').read(),
    url='https://github.com/ampledata/kiss',
    setup_requires=['coverage==3.7.1', 'nose==1.3.1'],
    install_requires=['pyserial==2.7'],
    package_dir={'kiss': 'kiss'},
    packages=['kiss'],
    zip_safe=False
)
