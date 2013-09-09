#!/usr/bin/env python
# -*- coding: utf-8 -*-

# KISS Python Module.

"""
KISS Python Module.
~~~~


:author: Greg Albrecht W2GMD <gba@onbeep.com>
:copyright: Copyright 2013 OnBeep, Inc.
:license: Apache 2.0, see LICENSE for details.
:source: <https://github.com/ampledata/kiss>

"""

__title__ = 'kiss'
__version__ = '0.0.3'
__build__ = '0x000003'
__author__ = 'Greg Albrecht W2GMD <gba@onbeep.com>'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2013 OnBeep, Inc.'


import logging

from .classes import KISS


# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())