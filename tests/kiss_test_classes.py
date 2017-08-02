#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for KISS Classes."""

import logging
import random
import unittest

from .context import kiss

from . import constants

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Greg Albrecht and Contributors'  # NOQA pylint: disable=R0801
__license__ = 'Apache License, Version 2.0'  # NOQA pylint: disable=R0801


class KISSTestClass(unittest.TestCase):  # pylint: disable=R0904

    """Test class for KISS Python Module."""

    _logger = logging.getLogger(__name__)  # pylint: disable=R0801
    if not _logger.handlers:  # pylint: disable=R0801
        _logger.setLevel(kiss.LOG_LEVEL)  # pylint: disable=R0801
        _console_handler = logging.StreamHandler()  # pylint: disable=R0801
        _console_handler.setLevel(kiss.LOG_LEVEL)  # pylint: disable=R0801
        _console_handler.setFormatter(kiss.LOG_FORMAT)  # pylint: disable=R0801
        _logger.addHandler(_console_handler)  # pylint: disable=R0801
        _logger.propagate = False  # pylint: disable=R0801

    @classmethod
    def random(cls, length=8, alphabet=constants.ALPHANUM):
        """
        Generates a random string for test cases.

        :param length: Length of string to generate.
        :param alphabet: Alphabet to use to create string.
        :type length: int
        :type alphabet: str
        """
        return ''.join(random.choice(alphabet) for _ in range(length))

    @classmethod
    def print_frame(cls, frame):
        print('{}'.format(aprs.Frame(frame)))
