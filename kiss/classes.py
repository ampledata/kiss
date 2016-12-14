#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python KISS Module Class Definitions."""

import logging
import socket

import serial

import kiss

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


class KISS(object):

    """KISS Object Class."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(kiss.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(kiss.LOG_LEVEL)
        _console_handler.setFormatter(kiss.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, strip_df_start=False):
        self.strip_df_start = strip_df_start
        self.interface = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __del__(self):
        self.stop()

    def _read_handler(self, read_bytes=None):  # pylint: disable=R0201
        """
        Helper method to call when reading from KISS interface.
        """
        read_bytes = read_bytes or kiss.READ_BYTES

    def _write_handler(self, frame=None):  # pylint: disable=R0201
        """
        Helper method to call when writing to KISS interface.
        """
        del frame

    def stop(self):
        """
        Helper method to call when stopping KISS interface.
        """
        pass

    def start(self, **kwargs):
        """
        Helper method to call when starting KISS interface.
        """
        pass

    def write_setting(self, name, value):
        """
        Writes KISS Command Codes to attached device.

        http://en.wikipedia.org/wiki/KISS_(TNC)#Command_Codes

        :param name: KISS Command Code Name as a string.
        :param value: KISS Command Code Value to write.
        """
        self._logger.debug('Configuring %s=%s', name, repr(value))

        # Do the reasonable thing if a user passes an int
        if isinstance(value, int):
            value = chr(value)

        return self.interface.write(
            kiss.FEND +
            getattr(kiss, name.upper()) +
            kiss.escape_special_codes(value) +
            kiss.FEND
        )

    def read(self, read_bytes=None, callback=None, readmode=True):  # NOQA pylint: disable=R0912
        """
        Reads data from KISS device.

        :param callback: Callback to call with decoded data.
        :param readmode: If False, immediately returns frames.
        :type callback: func
        :type readmode: bool
        :return: List of frames (if readmode=False).
        :rtype: list
        """
        self._logger.debug(
            'read_bytes=%s callback="%s" readmode=%s',
            read_bytes, callback, readmode)

        read_buffer = ''

        while 1:
            read_data = self._read_handler(read_bytes)

            if read_data is not None and len(read_data):
                self._logger.debug(
                    'read_data(%s)="%s"', len(read_data), read_data)

                frames = []

                split_data = read_data.split(kiss.FEND)
                len_fend = len(split_data)
                self._logger.debug(
                    'split_data(len_fend=%s)="%s"', len_fend, split_data)

                # Handle NMEAPASS on T3-Micro
                if len(read_data) >= 900:
                    if kiss.NMEA_HEADER in read_data and '\r\n' in read_data:
                        if callback:
                            callback(read_data)
                        elif not readmode:
                            return [read_data]

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
                    # Iterate through split_data and extract just the frames.
                    for i in range(0, len_fend - 1):
                        _str = ''.join([read_buffer, split_data[i]])
                        self._logger.debug('i=%s _str="%s"', i, _str)
                        if _str:
                            frames.append(_str)
                            read_buffer = ''
                    if split_data[len_fend - 1]:
                        read_buffer = split_data[len_fend - 1]

                # Fixup T3-Micro NMEA Sentences
                frames = map(kiss.strip_nmea, frames)

                # Remove None frames.
                frames = filter(None, frames)

                # Maybe.
                frames = map(kiss.recover_special_codes, frames)

                if self.strip_df_start:
                    frames = map(kiss.strip_df_start, frames)

                if readmode:
                    for frame in frames:
                        callback(frame)
                elif not readmode:
                    return frames

    def write(self, frame):
        """
        Writes frame to KISS interface.

        :param frame: Frame to write.
        """
        self._logger.debug('frame(%s)="%s"', len(frame), frame)

        frame_escaped = kiss.escape_special_codes(frame)
        self._logger.debug(
            'frame_escaped(%s)="%s"', len(frame_escaped), frame_escaped)

        frame_kiss = ''.join([
            kiss.FEND,
            kiss.DATA_FRAME,
            frame_escaped,
            kiss.FEND
        ])
        self._logger.debug(
            'frame_kiss(%s)="%s"', len(frame_kiss), frame_kiss)

        self._write_handler(frame_kiss)


class TCPKISS(KISS):

    """KISS TCP Class."""

    def __init__(self, host, port, strip_df_start=False):
        self.address = (host, int(port))
        self.strip_df_start = strip_df_start
        super(TCPKISS, self).__init__(strip_df_start)

    def _read_handler(self, read_bytes=None):
        read_bytes = read_bytes or kiss.READ_BYTES
        read_data = self.interface.recv(read_bytes)
        self._logger.debug('len(read_data)=%s', len(read_data))
        if read_data == '':
            raise kiss.SocketClosetError('Socket Closed')
        return read_data

    def stop(self):
        if self.interface:
            self.interface.shutdown(socket.SHUT_RDWR)

    def start(self):
        """
        Initializes the KISS device and commits configuration.
        """
        self.interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._logger.debug('Conntecting to %s', self.address)
        self.interface.connect(self.address)
        self._write_handler = self.interface.send


class SerialKISS(KISS):

    """KISS Serial Class."""

    def __init__(self, port, speed, strip_df_start=False):
        self.port = port
        self.speed = speed
        self.strip_df_start = strip_df_start
        super(SerialKISS, self).__init__(strip_df_start)

    def _read_handler(self, read_bytes=None):
        read_bytes = read_bytes or kiss.READ_BYTES
        read_data = self.interface.read(read_bytes)
        if len(read_data):
            self._logger.debug(
                'read_data(%s)="%s"', len(read_data), read_data)
        waiting_data = self.interface.inWaiting()
        if waiting_data:
            self._logger.debug('waiting_data="%s"', waiting_data)
            read_data = ''.join([
                read_data, self.interface.read(waiting_data)])
        return read_data

    def _write_defaults(self, **kwargs):
        """
        Previous verious defaulted to Xastir-friendly configs. Unfortunately
        those don't work with Bluetooth TNCs, so we're reverting to None.

        Use `config_xastir()` for Xastir defaults.
        """
        return [self.write_setting(k, v) for k, v in kwargs.items()]

    def config_xastir(self):
        """
        Helper method to set default configuration to those that ship with
        Xastir.
        """
        return self._write_defaults(
            **kiss.DEFAULT_KISS_CONFIG_VALUES)

    def kiss_on(self):
        """Turns KISS ON."""
        self.interface.write(kiss.KISS_ON)

    def kiss_off(self):
        """Turns KISS OFF."""
        self.interface.write(kiss.KISS_OFF)

    def stop(self):
        if self.interface and self.interface.isOpen():
            self.interface.close()

    def start(self, **kwargs):
        """
        Initializes the KISS device and commits configuration.

        See http://en.wikipedia.org/wiki/KISS_(TNC)#Command_codes
        for configuration names.

        :param **kwargs: name/value pairs to use as initial config values.
        """
        self._logger.debug('kwargs=%s', kwargs)
        self.interface = serial.Serial(self.port, self.speed)
        self.interface.timeout = kiss.SERIAL_TIMEOUT
        self._write_handler = self.interface.write
        self._write_defaults(**kwargs)
