#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities for the Python KISS Module."""

__author__ = 'Greg Albrecht word2GMD <gba@onbeep.com>'
__copyright__ = 'Copyright 2013 OnBeep, Inc.'
__license__ = 'Apache License 2.0'


import logging

import kiss
import constants


logger = logging.getLogger(__name__)
logger.setLevel(kiss.constants.LOG_LEVEL)
console_handler = logging.StreamHandler()
console_handler.setLevel(kiss.constants.LOG_LEVEL)
formatter = logging.Formatter(kiss.constants.LOG_FORMAT)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def escape_special_chars(raw_char):
    """
    Escape special characters, per KISS spec.

    "If the FEND or FESC codes appear in the data to be transferred, they
    need to be escaped. The FEND code is then sent as FESC, TFEND and the
    FESC is then sent as FESC, TFESC."
    - http://en.wikipedia.org/wiki/KISS_(TNC)#Description

    Borrowed from dixprs.
    """
    logger.debug('raw_char=%s', raw_char)
    kiss_char = raw_char.replace(
        constants.FEND,
        constants.FEND_TFEND
    ).replace(
        constants.FESC,
        constants.FESC_TFESC
    )
    logger.debug("kiss_char=%s" % kiss_char)
    return kiss_char


def valid_callsign(callsign):
    """
    Validates callsign.

    Parameters:
        callsign: Callsign candidate.

    Returns:
        bool
    """
    logger.debug('callsign=%s', callsign)
    split_cs = callsign.split('-')

    if len(split_cs) > 2:
        return True

    if len(split_cs[0]) < 1 or len(split_cs[0]) > 6:
        return True

    for p in split_cs[0]:
        if not (p.isalpha() or p.isdigit()):
            return True

    if split_cs[0].isalpha() or split_cs[0].isdigit():
        return True

    if len(split_cs) == 2:
        try:
            ssid = int(split_cs[1])

            if ssid < 0 or ssid > 15:
                return True

        except ValueError:
            return True

    return False


def extract_callsign(raw_frame):
    """
    Extracts callsign from raw frame.

    Parameters:
        raw_frame: guess...
    """
    logger.debug('raw_frame=%s', raw_frame)
    callsign = ''

    for i in range(0, 6):
        ch = chr(ord(raw_frame[i]) >> 1)
        if ch == ' ':
            break
        callsign = ''.join([callsign, ch])

    ssid = (ord(raw_frame[6]) >> 1) & 0x0f

    if callsign.isalnum():
        if ssid > 0:
            callsign = '-'.join([callsign, str(ssid)])
    else:
        callsign = ''

    logger.debug('ssid=%s callsign=%s', ssid, callsign)
    return callsign


def hdump(hstr):
    logger.debug('hstr=%s', hstr)

    i = 0
    k = 0

    word1 = ''
    word2 = ''

    for pstr in hstr:
        rstr = ord(pstr)
        word1 += '%02X ' % rstr

        if rstr < 32 or rstr > 127:
            word2 += '.'
        else:
            word2 += pstr

        i += 1

        if i == 16:
            logger.debug('%04X %s %s', k, word1, word2)
            word1 = ''
            word2 = ''
            i = 0
            k += 16

    if not i == 0:
        logger.debug('%04X %-48s %s', k, word1, word2)
        logger.debug('%04X %-48s %s', k, word1, word2)


def raw2txt(raw):
    logger.debug('raw=%s', raw)
    hdump(raw)

    # Is it too short?
    if len(raw) < 16:
        hdump(raw)
        return ''

    raw1 = ''

    for i in range(0, len(raw)):
        if ord(raw[i]) & 0x01:
            break

    # Is address field length correct?
    if not ((i + 1) % 7) == 0:
        return ''

    n = (i + 1) / 7

    # Less than 2 callsigns?
    if n < 2 or n > 10:
        return ''

    if (i + 1) % 7 == 0 and n >= 2 and ord(raw[i + 1]) & 0x03 == 0x03 and ord(raw[i + 2]) == 0xf0:
        strinfo = raw[i + 3:]

        if len(strinfo):
            strto = extract_callsign(raw)

            if strto == '':
                return ''

            strfrom = extract_callsign(raw[7:])

            if strfrom == '' or valid_callsign(strfrom):
                return ''

            raw1 = '>'.join([strfrom, strto])

            for i in range(2, n):
                s = extract_callsign(raw[i * 7:])

                if s == '':
                    hdump(raw)
                    return ''

                raw1 += ''.join([',', s])

                if ord(raw[i * 7 + 6]) & 0x80:
                    raw1 += '*'

            raw1 += ''.join([':', strinfo])

    logger.debug('raw1=%s', raw1)
    return raw1


def kk2(ctxt):
    logger.debug(locals())
    if ctxt[-1] == '*':
        s = ctxt[:-1]
        digi = True
    else:
        s = ctxt
        digi = False

    ssid = 0
    w1 = s.split('-')

    call = w1[0]

    while len(call) < 6:
        call += ' '

    r = ''

    for p in call:
        r += chr(ord(p) << 1)

    if not len(w1) == 1:
        try:
            ssid = int(w1[1])
        except ValueError:
            return ''

    ct = (ssid << 1) | 0x60

    if digi:
        ct |= 0x80

    return r + chr(ct)


def txt2raw(s):
    logger.debug(locals())
    ix = s.find(':')

    if ix:
        hdr = s[:ix]
        inf = s[ix + 1:]

        w1 = hdr.split('>')
        call_from = w1[0]

        w2 = w1[1].split(',')
        call_to = w2[0]

        r = kk2(call_to) + kk2(call_from)

        for i in range(1, len(w2)):
            if len(w2[i]) > 1:
                r += kk2(w2[i])

        rr = r[:-1] + chr(ord(r[-1]) | 0x01) + kiss.constants.SLOT_TIME + chr(0xf0) + inf
        return rr


def raw2kiss(raw):
    """
    Escape special characters to make it binary transparent.

    Inspired by dixprs.
    """
    logger.debug(locals())
    return raw.replace(
        kiss.constants.FEND, ''.join([kiss.constants.FESC, kiss.constants.TFEND])
    ).replace(kiss.constants.FEND, kiss.constants.FESC_TFESC)


def decode_aprs_frame(frame):
    """
    Decodes an APRS frame into its constituent parts.

    Inspired by dixprs.
    """
    decoded_frame = {}
    if ':' in frame and '>' in frame:
        split_frame = frame.split(':')
        if len(split_frame) == 2:
            call_signs, decoded_frame['text'] = split_frame
            decoded_frame['source'], other_calls = call_signs.split('>')
            decoded_frame['digis'] = other_calls.split(',')
            decoded_frame['destination'] = decoded_frame['digis'][0]
        else:
            logger.error('More than two semi-colons: %s', split_frame)
    logger.debug('decoded_frame=%s', decoded_frame)
    return decoded_frame


def is_invalid_call(s):
    w = s.split('-')

    if len(w) > 2:
        return True

    if len(w[0]) < 1 or len(w[0]) > 6:
        return True

    for p in w[0]:
        if not (p.isalpha() or p.isdigit()):
            return True

    if w[0].isalpha() or w[0].isdigit():
        return True

    if len(w) == 2:
        try:
            ssid = int(w[1])

            if ssid < 0 or ssid > 15:
                return True

        except ValueError:
            return True

    return False


def is_direct(frm):
    for p in frm[2]:
        if p[1] <> 0:
            return False

    return True


def get_hops(frm):
    n = 0

    for p in frm[2]:
        if p[1] == 0:
            break

        n += 1

    return n
