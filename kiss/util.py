#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities for the KISS Python Module."""

__author__ = 'Greg Albrecht W2GMD <gba@onbeep.com>'
__copyright__ = 'Copyright 2013 OnBeep, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


import kiss.constants


def escape_special_codes(raw_codes):
    """
    Escape special codes, per KISS spec.

    "If the FEND or FESC codes appear in the data to be transferred, they
    need to be escaped. The FEND code is then sent as FESC, TFEND and the
    FESC is then sent as FESC, TFESC."
    - http://en.wikipedia.org/wiki/KISS_(TNC)#Description
    """
    return raw_codes.replace(
        kiss.constants.FESC,
        kiss.constants.FESC_TFESC
    ).replace(
        kiss.constants.FEND,
        kiss.constants.FESC_TFEND
    )
