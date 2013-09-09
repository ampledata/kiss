#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the KISS Python Module.

Source:: https://github.com/ampledata/kiss
"""

__author__ = 'Greg Albrecht W2GMD <gba@onbeep.com>'
__copyright__ = 'Copyright 2013 Onbeep, Inc.'
__license__ = 'Apache License 2.0'


import os
import sys

import kiss

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def publish():
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist upload')
        sys.exit()


publish()


setup(
    name='kiss',
    version=kiss.__version__,
    description='KISS Python Module.',
    long_description=open('README.rst').read(),
    author='Greg Albrecht',
    author_email='gba@onbeep.com',
    license=open('LICENSE').read(),
    url='https://github.com/ampledata/kiss',
    setup_requires=['nose'],
    tests_require=['coverage', 'nose'],
    install_requires=['pyserial'],
    package_dir={'kiss': 'kiss'},
    zip_safe=False
)
