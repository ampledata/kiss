#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python KISS Module Utility Functions Definitions."""

import kiss

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Greg Albrecht and Contributors'  # NOQA pylint: disable=R0801
__license__ = 'Apache License, Version 2.0'  # NOQA pylint: disable=R0801


def escape_special_codes(raw_codes):
    """
    Escape special codes, per KISS spec.

    "If the FEND or FESC codes appear in the data to be transferred, they
    need to be escaped. The FEND code is then sent as FESC, TFEND and the
    FESC is then sent as FESC, TFESC."
    - http://en.wikipedia.org/wiki/KISS_(TNC)#Description
    """
    return raw_codes.replace(
        kiss.FESC,
        kiss.FESC_TFESC
    ).replace(
        kiss.FEND,
        kiss.FESC_TFEND
    )


def recover_special_codes(escaped_codes):
    """
    Recover special codes, per KISS spec.

    "If the FESC_TFESC or FESC_TFEND escaped codes appear in the data received,
    they need to be recovered to the original codes. The FESC_TFESC code is
    replaced by FESC code and FESC_TFEND is replaced by FEND code."
    - http://en.wikipedia.org/wiki/KISS_(TNC)#Description
    """
    out = bytearray()
    i = 0
    while i < len(escaped_codes):
        if escaped_codes[i] == kiss.FESC[0] and i + 1 < len(escaped_codes):
            if escaped_codes[i + 1] == kiss.TFESC[0]:
                out.append(kiss.FESC[0])
                i += 1 #Skips over the next byte, which would be the TFESC
            elif escaped_codes[i + 1] == kiss.TFEND[0]:
                out.append(kiss.FEND[0])
                i += 1
            else:
                out.append(escaped_codes[i])
        else:
            out.append(escaped_codes[i])
        i += 1

    return out

def extract_ui(frame):
    """
    Extracts the UI component of an individual frame.

    :param frame: APRS/AX.25 frame.
    :type frame: str
    :returns: UI component of frame.
    :rtype: str
    """
    start_ui = frame.split(
        b''.join([kiss.FEND, kiss.DATA_FRAME]))
    end_ui = start_ui[0].split(b''.join([kiss.SLOT_TIME, kiss.UI_PROTOCOL_ID]))
    return ''.join([chr(x >> 1) for x in end_ui[0]])


def strip_df_start(frame):
    """
    Strips KISS DATA_FRAME start (0x00) and newline from frame.

    :param frame: APRS/AX.25 frame.
    :type frame: str
    :returns: APRS/AX.25 frame sans DATA_FRAME start (0x00).
    :rtype: str
    """
    return frame.lstrip(kiss.DATA_FRAME).strip()


def strip_nmea(frame):
    """
    Extracts NMEA header from T3-Micro or NMEA encoded KISS frames.
    """
    if len(frame) > 0:
        if frame[0] == 240:
            return frame[1:].rstrip()
    return frame
