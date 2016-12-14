#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python KISS Module.

"""
Python KISS Module.
~~~~


:author: Greg Albrecht W2GMD <oss@undef.net>
:copyright: Copyright 2016 Orion Labs, Inc. and Contributors
:license: Apache License, Version 2.0
:source: <https://github.com/ampledata/kiss>

"""

from .constants import (LOG_FORMAT, LOG_LEVEL, SERIAL_TIMEOUT, READ_BYTES,  # NOQA
                        FEND, FESC, TFEND, TFESC, FESC_TFEND, FESC_TFESC,
                        DATA_FRAME, TX_DELAY, PERSISTENCE, SLOT_TIME, TX_TAIL,
                        FULL_DUPLEX, SET_HARDWARE, RETURN, DATAFRAME, TXDELAY,
                        P, SLOTTIME, TXTAIL, FULLDUPLEX, SETHARDWARE,
                        DEFAULT_KISS_CONFIG_VALUES, KISS_ON, KISS_OFF,
                        NMEA_HEADER)

from .exceptions import SocketClosetError  # NOQA

from .util import (escape_special_codes, recover_special_codes, extract_ui,  # NOQA
                   strip_df_start, strip_nmea)

from .classes import KISS, TCPKISS, SerialKISS  # NOQA


__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'
