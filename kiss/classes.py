#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KISS Core Classes."""

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.co>'
__copyright__ = 'Copyright 2015 Orion Labs, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


import logging

import serial
import socket

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

    def __init__(self, port=None, speed=None, host=None, tcp_port=None,
                 strip_df_start=False):
        self.port = port
        self.speed = speed
        self.host = host
        self.tcp_port = tcp_port
        self.interface = None
        self.interface_mode = None
        self.strip_df_start = strip_df_start

        if self.port is not None and self.speed is not None:
            self.interface_mode = 'serial'
        elif self.host is not None and self.tcp_port is not None:
            self.interface_mode = 'tcp'
        if self.interface_mode is None:
            raise Exception('Must set port/speed or host/tcp_port.')

        self.logger.info('Using interface_mode=%s', self.interface_mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if 'tcp' in self.interface_mode:
            self.interface.shutdown()
        elif self.interface and self.interface.isOpen():
            self.interface.close()

    def __del__(self):
        if self.interface and self.interface.isOpen():
            self.interface.close()

    def start(self, **kwargs):
        """
        Initializes the KISS device and commits configuration.

        See http://en.wikipedia.org/wiki/KISS_(TNC)#Command_codes
        for configuration names.

        :param **kwargs: name/value pairs to use as initial config values.
        """
        self.logger.debug("kwargs=%s", kwargs)

        if 'tcp' in self.interface_mode:
            address = (self.host, self.tcp_port)
            self.interface = socket.create_connection(address)
        elif 'serial' in self.interface_mode:
            self.interface = serial.Serial(self.port, self.speed)
            self.interface.timeout = kiss.constants.SERIAL_TIMEOUT

        # Previous verious defaulted to Xastir-friendly configs. Unfortunately
        # those don't work with Bluetooth TNCs, so we're reverting to None.
        if 'serial' in self.interface_mode and kwargs:
            for name, value in kwargs.items():
                self.write_setting(name, value)

        # If no settings specified, default to config values similar
        # to those that ship with Xastir.
        #if not kwargs:
        #    kwargs = kiss.constants.DEFAULT_KISS_CONFIG_VALUES


    def write_setting(self, name, value):
        """
        Writes KISS Command Codes to attached device.

        http://en.wikipedia.org/wiki/KISS_(TNC)#Command_Codes

        :param name: KISS Command Code Name as a string.
        :param value: KISS Command Code Value to write.
        """
        self.logger.debug('Configuring %s = %s', name, repr(value))

        # Do the reasonable thing if a user passes an int
        if isinstance(value, int):
            value = chr(value)

        return self.interface.write(
            kiss.constants.FEND +
            getattr(kiss.constants, name.upper()) +
            kiss.util.escape_special_codes(value) +
            kiss.constants.FEND
        )

    def read(self, callback=None, readmode=True):
        """
        Reads data from KISS device.

        :param callback: Callback to call with decoded data.
        :param readmode: If False, immediately returns frames.
        :type callback: func
        :type readmode: bool
        :return: List of frames (if readmode=False).
        :rtype: list
        """
        self.logger.debug('callback=%s readmode=%s', callback, readmode)

        read_buffer = ''

        while 1:
            read_data = None
            if 'tcp' in self.interface_mode:
                read_data = self.interface.recv(kiss.constants.READ_BYTES)
            elif 'serial' in self.interface_mode:
                read_data = self.interface.read(kiss.constants.READ_BYTES)
                waiting_data = self.interface.inWaiting()
                if waiting_data:
                    read_data = ''.join([
                        read_data, self.interface.read(waiting_data)])

            if read_data is not None:
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

                if readmode:
                    # Loop through received frames
                    for frame in frames:
                        if len(frame) and ord(frame[0]) == 0:
                            self.logger.debug('frame=%s', frame)
                            if callback:
                                if 'tcp' in self.interface_mode:
                                    if self.strip_df_start:
                                        callback(
                                            kiss.util.strip_df_start(frame))
                                    else:
                                        callback(frame)
                                elif 'serial' in self.interface_mode:
                                    if self.strip_df_start:
                                        callback(
                                            kiss.util.strip_df_start(frame))
                                    else:
                                        callback(frame)
                elif not readmode:
                    if self.strip_df_start:
                        return [kiss.util.strip_df_start(f) for f in frames]
                    else:
                        return frames

            if not readmode:
                    if self.strip_df_start:
                        return [kiss.util.strip_df_start(f) for f in frames]
                    else:
                        return frames

    def write(self, frame):
        """
        Writes frame to KISS interface.

        :param frame: Frame to write.
        """
        interface_handler = None

        if 'tcp' in self.interface_mode:
            interface_handler = self.interface.send
        elif 'serial' in self.interface_mode:
            interface_handler = self.interface.write

        if interface_handler is not None:
            return interface_handler(''.join([
                kiss.constants.FEND,
                kiss.constants.DATA_FRAME,
                kiss.util.escape_special_codes(frame),
                kiss.constants.FEND
            ]))
