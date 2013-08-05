#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KISS Module for Python"""

__author__ = 'Greg Albrecht W2GMD <gba@onbeep.com>'
__copyright__ = 'Copyright 2013 OnBeep, Inc.'
__license__ = 'Apache License 2.0'


import logging

import serial

import constants
import util


class KISS(object):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    def __init__(self, port, speed):
        self.port = port
        self.speed = speed

    def start(self):
        self.logger.info('start()')
        self.serial_int = serial.Serial(self.port, self.speed)
        self.serial_int.timeout = 0.01  # TODO: Fix this magic number.

        # http://en.wikipedia.org/wiki/KISS_(TNC)#Command_Codes
        kiss_config = {}

        if kiss_config.get('TX_DELAY'):
            self.serial_int.write(
                constants.FEND +
                constants.TX_DELAY +
                util.escape_special_chars(kiss_config['TXD']) +
                constants.FEND
            )

        if kiss_config.get('PERSISTENCE'):
            self.serial_int.write(
                constants.FEND +
                constants.PERSISTENCE +
                util.escape_special_chars(kiss_config['PERSISTENCE']) +
                constants.FEND
            )

        if kiss_config.get('SLOT_TIME'):
            self.serial_int.write(
                constants.FEND +
                constants.SLOT_TIME +
                util.escape_special_chars(kiss_config['SLOT_TIME']) +
                constants.FEND
            )

        if kiss_config.get('TX_TAIL'):
            self.serial_int.write(
                constants.FEND +
                constants.TX_TAIL +
                util.escape_special_chars(kiss_config['TX_TAIL']) +
                constants.FEND
            )

        if kiss_config.get('FULL_DUPLEX'):
            self.serial_int.write(
                constants.FEND +
                constants.FULL_DUPLEX +
                util.escape_special_chars(kiss_config['FULL_DUPLEX']) +
                constants.FEND
            )

    def read(self):
        read_buffer = ''

        while 1:
            read_data = self.serial_int.read(1000)  # TODO: Fix this magic number.

            waiting_data = self.serial_int.inWaiting()

            if waiting_data:
                read_data = ''.join([read_data, self.serial_int.read(waiting_data)])

            if read_data:
                frames = []

                split_data = read_data.split(constants.FEND)
                len_fend = len(split_data)
                self.logger.debug('len_fend=%s', len_fend)

                # No FEND in frame
                if len_fend == 1:
                    read_buffer = ''.join([read_buffer, split_data[0]])

                # Single FEND in frame
                elif len_fend == 2:
                    # Closing FEND found
                    if split_data[0]:
                        # Partial frame continued, otherwise drop
                        frames.append(''.join([read_buffer, split_data[0]]))
                        read_buffer = ''

                    # Opening FEND found
                    else:
                        frames.append(read_buffer)
                        read_buffer = split_data[1]

                # At least one complete frame received
                elif len_fend >= 3:
                    for i in range(0, len_fend - 1):
                        st = ''.join([read_buffer, split_data[i]])

                        if st:
                            frames.append(st)
                            read_buffer = ''

                    if split_data[len_fend - 1]:
                        read_buffer = split_data[len_fend - 1]

                # Loop through received frames
                for frame in frames:
                    if len(frame) and ord(frame[0]) == 0:
                        txt = util.raw2txt(frame[1:])
                        if txt:
                            self.logger.info('txt=%s', txt)