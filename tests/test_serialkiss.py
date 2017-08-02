#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for KISS Classes."""

import unittest

import aprs
import dummyserial

from .context import kiss
from .context import kiss_test_classes  # pylint: disable=R0801

from . import constants

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Greg Albrecht and Contributors'  # NOQA pylint: disable=R0801
__license__ = 'Apache License, Version 2.0'  # NOQA pylint: disable=R0801


class SerialKISSTestCase(kiss_test_classes.KISSTestClass):

    """Test class for KISS Python Module."""

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

    def test_write(self):
        ks = kiss.SerialKISS(port=self.random_serial_port, speed='9600')
        ks.interface = dummyserial.Serial(port=self.random_serial_port)
        ks._write_handler = ks.interface.write

        frame = aprs.Frame()
        frame.source = aprs.Callsign(self.random(6))
        frame.destination = aprs.Callsign(self.random(6))
        frame.path = [
            aprs.Callsign(self.random(6)),
            aprs.Callsign(self.random(6))
        ]
        frame.text = ' '.join([
            self.random(), 'test_write', self.random()])

        self._logger.debug('frame="%s"', frame)

        frame_encoded = frame.encode_kiss()
        self._logger.debug('frame_encoded="%s"', frame_encoded)

        ks.write(frame_encoded)

    # FIXME: Currently broken.
    def test_write_and_read(self):
        """Tests writing-to and reading-from a Dummy Serial port."""
        frame = aprs.Frame()
        frame.source = aprs.Callsign(self.random(6))
        frame.destination = aprs.Callsign(self.random(6))
        frame.path = [
            aprs.Callsign(self.random(6)),
            aprs.Callsign(self.random(6))
        ]
        frame.text = ' '.join([
            self.random(), 'test_write_and_read', self.random()])

        self._logger.debug('frame="%s"', frame)

        frame_encoded = frame.encode_kiss()
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
        # self.assertEqual(read_data, frame_kiss)

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
