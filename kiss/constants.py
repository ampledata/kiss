#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python KISS Module Constants."""

import logging

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = logging.Formatter(
    '%(asctime)s kiss %(levelname)s %(name)s.%(funcName)s:%(lineno)d'
    ' - %(message)s')

SERIAL_TIMEOUT = 0.01
READ_BYTES = 1000

# KISS Special Characters
# http://en.wikipedia.org/wiki/KISS_(TNC)#Special_Characters
# http://k4kpk.com/content/notes-aprs-kiss-and-setting-tnc-x-igate-and-digipeater
# Frames begin and end with a FEND/Frame End/0xC0 byte
FEND = chr(0xC0)  # Marks START and END of a Frame
FESC = chr(0xDB)  # Escapes FEND and FESC bytes within a frame

# Transpose Bytes: Used within a frame-
# "Transpose FEND": An FEND after an FESC (within a frame)-
# Sent as FESC TFEND
TFEND = chr(0xDC)
# "Transpose FESC": An FESC after an FESC (within a frame)-
# Sent as FESC TFESC
TFESC = chr(0xDD)

# "FEND is sent as FESC, TFEND"
# 0xC0 is sent as 0xDB 0xDC
FESC_TFEND = ''.join([FESC, TFEND])

# "FESC is sent as FESC, TFESC"
# 0xDB is sent as 0xDB 0xDD
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

KISS_ON = 'KISS $0B'
KISS_OFF = ''.join([FEND, chr(0xFF), FEND, FEND])

NMEA_HEADER = ''.join([FEND, chr(0xF0), '$'])
