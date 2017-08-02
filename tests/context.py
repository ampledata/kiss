#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Context for tests for KISS Python Module."""

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import kiss  # NOQA pylint: disable=W0611,C0413
import kiss.constants  # NOQA pylint: disable=W0611,C0413

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'  # NOQA pylint: disable=R0801
__copyright__ = 'Copyright 2017 Greg Albrecht and Contributors'  # NOQA pylint: disable=R0801
__license__ = 'Apache License, Version 2.0'  # NOQA pylint: disable=R0801
