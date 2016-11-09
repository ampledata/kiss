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

from .classes import KISS, TCPKISS, SerialKISS  # NOQA
from .util import (escape_special_codes, recover_special_codes, extract_ui,  # NOQA
                   strip_df_start)

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'
