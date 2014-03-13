#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KISS Core Classes."""

__author__ = 'Greg Albrecht W2GMD <gba@onbeep.com>'
__copyright__ = 'Copyright 2013 OnBeep, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


import logging

import serial

import kiss.constants
import kiss.util


class KISS(object):

    """KISS Object Class."""

    logger = logging.getLogger(__name__)
    logger.setLevel(kiss.constants.LOG_LEVEL)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(kiss.constants.LOG_LEVEL)
    formatter = logging.Formatter(kiss.constants.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False

    def __init__(self, port, speed):
        self.port = port
        self.speed = speed
        self.serial_int = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.serial_int and self.serial_int.isOpen():
            self.serial_int.close()

    def __del__(self):
        if self.serial_int and self.serial_int.isOpen():
            self.serial_int.close()

    def start(self, **kwargs):
        """
        Initializes the KISS device and commits configuration.

        See http://en.wikipedia.org/wiki/KISS_(TNC)#Command_codes
        for configuration names.

        :param **kwargs: name/value pairs to use as initial config values.
        """
        self.logger.debug("kwargs=%s", kwargs)
        self.serial_int = serial.Serial(self.port, self.speed)
        self.serial_int.timeout = kiss.constants.SERIAL_TIMEOUT

        # If no settings specified, default to config values similar
        # to those that ship with xastir.
        if not kwargs:
            kwargs = kiss.constants.DEFAULT_KISS_CONFIG_VALUES

        for name, value in kwargs.items():
            self.write_setting(name, value)

    def write_setting(self, name, value):
        """
        Writes KISS Command Codes to attached device.

        http://en.wikipedia.org/wiki/KISS_(TNC)#Command_Codes

        :param name: KISS Command Code Name as a string.
        :param value: KISS Command Code Value to write.
        """
        self.logger.debug('Configuring %s = %s', name, repr(value))

        # Do the reasonable thing if a user passes an int
        if type(value) == int:
            value = chr(value)

        return self.serial_int.write(
            kiss.constants.FEND +
            getattr(kiss.constants, name.upper()) +
            kiss.util.escape_special_codes(value) +
            kiss.constants.FEND
        )

    def read(self, callback=None):
        """
        Reads data from KISS device.

        :param callback: Callback to call with decoded data.
        """
        self.logger.debug('callback=%s', callback)
        read_buffer = ''

        while 1:
            read_data = self.serial_int.read(kiss.constants.READ_BYTES)

            waiting_data = self.serial_int.inWaiting()

            if waiting_data:
                read_data = ''.join([
                    read_data, self.serial_int.read(waiting_data)])

            if read_data:
                frames = []

                split_data = read_data.split(kiss.constants.FEND)
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
                        _str = ''.join([read_buffer, split_data[i]])
                        if _str:
                            frames.append(_str)
                            read_buffer = ''
                    if split_data[len_fend - 1]:
                        read_buffer = split_data[len_fend - 1]

                # Loop through received frames
                for frame in frames:
                    if len(frame) and ord(frame[0]) == 0:
                        self.logger.debug('frame=%s', frame)
                        if callback:
                            callback(frame)

    def write(self, frame):
        """
        Writes frame to KISS device.

        :param frame: Frame to write.
        """
        return self.serial_int.write(''.join([
            kiss.constants.FEND,
            kiss.constants.DATA_FRAME,
            kiss.util.escape_special_codes(frame),
            kiss.constants.FEND
        ]))
