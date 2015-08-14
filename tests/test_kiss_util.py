#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for KISS Util Module."""

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.co>'
__copyright__ = 'Copyright 2015 Orion Labs, Inc. and Contributors'
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


if __name__ == '__main__':
    unittest.main()
