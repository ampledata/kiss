#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities for the KISS Python Module."""

__author__ = 'Greg Albrecht W2GMD <gba@onbeep.com>'
__copyright__ = 'Copyright 2013 OnBeep, Inc.'
__license__ = 'Apache 2.0'


import logging

import kiss.constants


logger = logging.getLogger(__name__)
logger.setLevel(kiss.constants.LOG_LEVEL)
console_handler = logging.StreamHandler()
console_handler.setLevel(kiss.constants.LOG_LEVEL)
formatter = logging.Formatter(kiss.constants.LOG_FORMAT)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.propagate = False


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
