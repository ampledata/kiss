#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for TCPKISS Class."""

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


import logging
import random
import unittest

import aprs

from mocket.mocket import Mocket, MocketEntry, MocketSocket, mocketize, create_connection

from .context import kiss

from . import constants

import kiss.constants   # FIXME


class TCPKISSTestCase(unittest.TestCase):

    """Test class for KISS Python Module."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(kiss.constants.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(kiss.constants.LOG_LEVEL)
        _console_handler.setFormatter(kiss.constants.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def setUp(self):
        """Setup."""
        self.test_frames = open(constants.TEST_FRAMES, 'r')
        self.test_frame = self.test_frames.readlines()[0].strip()
        self.random_host = self.random()
        self.random_port = int(self.random(5, constants.NUMBERS))
        self._logger.debug(
            'random_host=%s random_port=%s',
            self.random_host,
            self.random_port
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

    @mocketize
    def test_write(self):
        frame = {
            'source': self.random(6),
            'destination': self.random(6),
            'path': ','.join([self.random(6), self.random(6)]),
            'text': ' '.join([self.random(), 'test_write', self.random()])
        }
        self._logger.debug('frame="%s"', frame)

        frame_encoded = aprs.util.encode_frame(frame)
        self._logger.debug('frame_encoded="%s"', frame_encoded)

        ks = kiss.TCPKISS(host=self.random_host, port=self.random_port)
        a = (self.random_host, self.random_port)

        entry = MocketEntry(a, frame_encoded)
        Mocket.register(entry)
        self._logger.debug(a)
        self._logger.debug(entry.get_response())

        ks.interface = create_connection(a)
        ks._write_handler = ks.interface.sendall
        def _pass(): pass
        ks.stop = _pass

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

        frame_encoded = aprs.util.encode_frame(frame)
        self._logger.debug(
            'frame_encoded(%s)="%s"', len(frame_encoded), frame_encoded)

        frame_escaped = kiss.escape_special_codes(frame_encoded)
        self._logger.debug(
            'frame_escaped(%s)="%s"', len(frame_escaped), frame_escaped)

        frame_kiss = ''.join([
            kiss.constants.FEND,
            kiss.constants.DATA_FRAME,
            frame_escaped,
            kiss.constants.FEND
        ])
        self._logger.debug(
            'frame_kiss(%s)="%s"', len(frame_kiss), frame_kiss)

        ks = kiss.TCPKISS(host=self.random_host, port=self.random_port)
        a = (self.random_host, self.random_port)

        entry = MocketEntry(a, (frame_kiss))
        Mocket.register(entry)

        ks.interface = create_connection(a)
        ks._write_handler = ks.interface.sendall

        def _pass(): pass
        ks.stop = _pass

        ks.write(frame_encoded)
        _read_data = ks.read(len(frame_kiss), readmode=False)
        self._logger.debug(
            '_read_data(%s)="%s"', len(_read_data), _read_data)

        read_data = _read_data[0]
        self._logger.debug(
            'frame_kiss(%s)="%s"', len(frame_kiss), frame_kiss)
        self._logger.debug(
            'read_data(%s)="%s"', len(read_data), read_data)
        self.assertEqual(read_data, frame_kiss.split(kiss.constants.FEND)[1])


if __name__ == '__main__':
    unittest.main()
