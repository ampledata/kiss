#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for KISS Classes."""

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


import logging
import random
import unittest

import aprs
import dummyserial

from .context import kiss

from . import constants


class SerialKISSTestCase(unittest.TestCase):

    """Test class for KISS Python Module."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(kiss.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(kiss.LOG_LEVEL)
        _console_handler.setFormatter(kiss.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def setUp(self):
        """Setup."""
        self.test_frames = open(constants.TEST_FRAMES, 'r')
        self.test_frame = self.test_frames.readlines()[0].strip()
        self.random_serial_port = self.random()
        self.random_baudrate = self.random(5, constants.NUMBERS)
        self._logger.debug(
            'random_serial_port=%s random_baudrate=%s',
            self.random_serial_port,
            self.random_baudrate
        )

    def tearDown(self):
        """Teardown."""
        self.test_frames.close()

    @classmethod
    def random(cls, length=8, alphabet=None):
        """
        Generates a random string for test cases.
        :param length: Length of string to generate.
        :param alphabet: Alphabet to use to create string.
        :type length: int
        :type alphabet: str
        """
        alphabet = alphabet or constants.ALPHANUM
        return ''.join(random.choice(alphabet) for _ in xrange(length))

    @classmethod
    def print_frame(cls, frame):
        try:
            # Decode raw APRS frame into dictionary of separate sections
            decoded_frame = aprs.util.decode_frame(frame)

            # Format the APRS frame (in Raw ASCII Text) as a human readable frame
            formatted_aprs = aprs.util.format_aprs_frame(decoded_frame)

            # This is the human readable APRS output:
            print formatted_aprs

        except Exception as ex:
            print ex
            print "Error decoding frame:"
            print "\t%s" % frame

    def test_write(self):
        ks = kiss.SerialKISS(port=self.random_serial_port, speed='9600')
        ks.interface = dummyserial.Serial(port=self.random_serial_port)
        ks._write_handler = ks.interface.write

        frame = {
            'source': self.random(6),
            'destination': self.random(6),
            'path': ','.join([self.random(6), self.random(6)]),
            'text': ' '.join([self.random(), 'test_write', self.random()])
        }
        self._logger.debug('frame="%s"', frame)

        frame_encoded = aprs.util.encode_frame(frame)
        self._logger.debug('frame_encoded="%s"', frame_encoded)

        ks.write(frame_encoded)

    def test_write_and_read(self):
        """Tests writing-to and reading-from a Dummy Serial port."""
        frame = {
            'source': self.random(6),
            'destination': self.random(6),
            'path': ','.join([self.random(6), self.random(6)]),
            'text': ' '.join([
                self.random(), 'test_write_and_read', self.random()])
        }
        self._logger.debug('frame="%s"', frame)

        frame_encoded = aprs.util.encode_frame(frame)
        self._logger.debug('frame_encoded="%s"', frame_encoded)

        frame_escaped = kiss.escape_special_codes(frame_encoded)
        self._logger.debug('frame_escaped="%s"', frame_escaped)

        frame_kiss = ''.join([
            kiss.FEND,
            kiss.DATA_FRAME,
            frame_escaped,
            kiss.FEND
        ])
        self._logger.debug('frame_kiss="%s"', frame_kiss)

        ks = kiss.SerialKISS(
            port=self.random_serial_port, speed=self.random_baudrate)

        ks.interface = dummyserial.Serial(
            port=self.random_serial_port,
            baudrate=self.random_baudrate,
            ds_responses={frame_encoded: frame_kiss}
        )
        ks._write_handler = ks.interface.write
        ks.write(frame_encoded)

        read_data = ks._read_handler(len(frame_kiss))
        self.assertEqual(read_data, frame_kiss)

    def test_config_xastir(self):
        """Tests writing Xastir config to KISS TNC."""
        ks = kiss.SerialKISS(
            port=self.random_serial_port, speed=self.random_baudrate)

        ks.interface = dummyserial.Serial(
            port=self.random_serial_port,
            baudrate=self.random_baudrate
        )
        ks._write_handler = ks.interface.write
        ks.config_xastir()


if __name__ == '__main__':
    unittest.main()
