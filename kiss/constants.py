#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Constants for KISS Python Module."""

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.co>'
__copyright__ = 'Copyright 2015 Orion Labs, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


import logging


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = ('%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d'
              ' - %(message)s')

SERIAL_TIMEOUT = 0.01
READ_BYTES = 1000

# KISS Special Characters
# http://en.wikipedia.org/wiki/KISS_(TNC)#Special_Characters
FEND = chr(0xC0)
FESC = chr(0xDB)
TFEND = chr(0xDC)
TFESC = chr(0xDD)

# "FEND is sent as FESC, TFEND"
FESC_TFEND = ''.join([FESC, TFEND])

# "FESC is sent as FESC, TFESC"
FESC_TFESC = ''.join([FESC, TFESC])

# KISS Command Codes
# http://en.wikipedia.org/wiki/KISS_(TNC)#Command_Codes
DATA_FRAME = chr(0x00)
TX_DELAY = chr(0x01)
PERSISTENCE = chr(0x02)
SLOT_TIME = chr(0x03)
TX_TAIL = chr(0x04)
FULL_DUPLEX = chr(0x05)
SET_HARDWARE = chr(0x06)
RETURN = chr(0xFF)

# Alternate convenience spellings for Command Codes
# (these more closely match the names in the spec)
DATAFRAME = DATA_FRAME
TXDELAY = TX_DELAY
P = PERSISTENCE
SLOTTIME = SLOT_TIME
TXTAIL = TX_TAIL
FULLDUPLEX = FULL_DUPLEX
SETHARDWARE = SET_HARDWARE

DEFAULT_KISS_CONFIG_VALUES = {
    'TX_DELAY': 40,
    'PERSISTENCE': 63,
    'SLOT_TIME': 20,
    'TX_TAIL': 30,
    'FULL_DUPLEX': 0,
    }
