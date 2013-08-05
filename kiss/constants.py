#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Constants for KISS Module."""

__author__ = 'Greg Albrecht W2GMD <gba@onbeep.com>'
__copyright__ = 'Copyright 2013 OnBeep, Inc.'
__license__ = 'Apache License 2.0'


# KISS Special Characters
# http://en.wikipedia.org/wiki/KISS_(TNC)#Special_Characters
FEND = chr(0xC0)
FESC = chr(0xDB)
TFEND = chr(0xDC)
TFESC = chr(0xDD)


# "FEND is sent as FESC, TFEND"
FEND_TFEND = ''.join([FEND, TFEND])

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