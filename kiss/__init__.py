#!/usr/bin/env python
# -*- coding: utf-8 -*-

# KISS Python Module.

"""
KISS Python Module.
~~~~


:author: Greg Albrecht W2GMD <oss@undef.net>
:copyright: Copyright 2016 Orion Labs, Inc. and Contributors
:license: Apache License, Version 2.0
:source: <https://github.com/ampledata/kiss>

"""

import logging

from .classes import KISS  # NOQA
from .util import (escape_special_codes, recover_special_codes, extract_ui,  # NOQA
                   strip_df_start)

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """Default logging handler to avoid "No handler found" warnings."""
        def emit(self, record):
            """Default logging handler to avoid "No handler found" warnings."""
            pass

logging.getLogger(__name__).addHandler(NullHandler())
