#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for KISS Util Module."""

__author__ = 'Greg Albrecht W2GMD <gba@onbeep.com>'
__copyright__ = 'Copyright 2013 OnBeep, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


import unittest

from .context import kiss

from . import constants


# pylint: disable=R0904,C0103
class KISSUtilTestCase(unittest.TestCase):

    """Test class for KISS Python Module."""

    def setUp(self):
        """Setup."""
        self.test_frames = open(constants.TEST_FRAMES, 'r')
        self.test_frame = self.test_frames.readlines()[0].strip()

    def tearDown(self):
        """Teardown."""
        self.test_frames.close()

    def test_escape_special_codes_fend(self):
        """
        Tests `kiss.util.escape_special_codes` util function.
        """
        fend = kiss.util.escape_special_codes(kiss.constants.FEND)
        self.assertEqual(fend, kiss.constants.FESC_TFEND)

    def test_escape_special_codes_fesc(self):
        """
        Tests `kiss.util.escape_special_codes` util function.
        """
        fesc = kiss.util.escape_special_codes(kiss.constants.FESC)
        self.assertEqual(fesc, kiss.constants.FESC_TFESC)

    def test_extract_ui(self):
        """
        Tests `kiss.util.extract_ui` util function.
        """
        frame_ui = kiss.util.extract_ui(self.test_frame)
        self.assertEqual('APRX240W2GMD 6WIDE1 1', frame_ui)


if __name__ == '__main__':
    unittest.main()
