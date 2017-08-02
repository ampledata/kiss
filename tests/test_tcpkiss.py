#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for TCPKISS Class."""

import unittest

import aprs

from mocket.mocket import (Mocket, MocketEntry, MocketSocket, mocketize,
                           create_connection)

from .context import kiss
from .context import kiss_test_classes  # pylint: disable=R0801

from . import constants

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Greg Albrecht and Contributors'  # NOQA pylint: disable=R0801
__license__ = 'Apache License, Version 2.0'  # NOQA pylint: disable=R0801


class TCPKISSTestCase(kiss_test_classes.KISSTestClass):

    """Test class for KISS Python Module."""

    def setUp(self):
        """Setup."""
        self.test_frames = open(constants.TEST_FRAMES, 'rb')
        self.test_frame = self.test_frames.read()
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

    @mocketize
    def _test_write(self):
        frame = "%s>%s:%s" % (
            self.random(6),
            ','.join([self.random(6), self.random(6), self.random(6)]),
            ' '.join([
                self.random(), 'test_write', self.random()])
        )
        aprs_frame = aprs.Frame(frame)
        kiss_frame = aprs_frame.encode_kiss()

        ks = kiss.TCPKISS(host=self.random_host, port=self.random_port)
        a = (self.random_host, self.random_port)

        entry = MocketEntry(a, kiss_frame)
        Mocket.register(entry)
        self._logger.debug(a)
        self._logger.debug(entry.get_response())

        ks.interface = create_connection(a)
        ks._write_handler = ks.interface.sendall

        def _pass(): pass

        ks.stop = _pass

        ks.write(kiss_frame)

    # FIXME: Broken.
    @unittest.skip
    @mocketize
    def test_write_and_read(self):
        """Tests writing-to and reading-from TCP Host."""
        frame = "%s>%s:%s" % (
            self.random(6),
            ','.join([self.random(6), self.random(6), self.random(6)]),
            ' '.join([
                self.random(), 'test_write_and_read', self.random()])
        )
        aprs_frame = aprs.Frame(frame)
        kiss_frame = aprs_frame.encode_kiss()

        ks = kiss.TCPKISS(host=self.random_host, port=self.random_port)
        a = (self.random_host, self.random_port)

        entry = MocketEntry(a, [kiss_frame])
        entry_1 = MocketEntry(('localhost', 80), True)
        Mocket.register(entry)

        ks.interface = create_connection(a)
        ks._write_handler = ks.interface.sendall

        def _pass(): pass
        ks.stop = _pass

        ks.write(kiss_frame)

        _read_data = ks.read(len(kiss_frame), readmode=False)

        self._logger.info(
            '_read_data(%s)="%s"', len(_read_data), _read_data)

        # read_data = _read_data[0]
        # self._logger.debug(
        #    'frame_kiss(%s)="%s"', len(frame_kiss), frame_kiss)
        # self._logger.debug(
        #    'read_data(%s)="%s"', len(read_data), read_data)
        # self.assertEqual(read_data, frame_kiss.split(kiss.FEND)[1])


if __name__ == '__main__':
    unittest.main()
