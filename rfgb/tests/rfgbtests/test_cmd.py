# -*- coding: utf-8 -*-

# Copyright © 2017-2019 rfgb Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (at the base of this repository). If not,
# see <http://www.gnu.org/licenses/>

"""
Test the init function twice. Once to create the directory, and
again to check whether an exception is raised properly if another
one is created.
"""

from __future__ import print_function
from __future__ import absolute_import

from ...cmd import init
import os
import sys
import unittest


def reset_directories():
    if os.path.exists(".rfgb/") or os.path.exists(".rfgb/models/"):
        os.rmdir(".rfgb/models/")
        os.rmdir(".rfgb/")


class InitTest(unittest.TestCase):
    """
    Tests for rfgb.cmd.init

    1. Make sure .rfgb directory does not currently exist.
    2. Run tests with both default parameter, and quiet parameter.
    """

    def test_init_default_run(self):
        reset_directories()

        # First run should create directories.
        init()
        self.assertTrue(os.path.exists(".rfgb/"))
        self.assertTrue(os.path.exists(".rfgb/models/"))

        # Second should exit and print message to console.
        with self.assertRaises(SystemExit) as ExitCode:
            init()
        self.assertEqual(ExitCode.exception.code, 1)

    def test_init_quiet_run(self):
        reset_directories()

        # First run should create directories.
        init(quiet=True)
        self.assertTrue(os.path.exists(".rfgb/"))
        self.assertTrue(os.path.exists(".rfgb/models/"))

        # Second should exit and print message to console.
        with self.assertRaises(SystemExit) as ExitCode:
            init(quiet=True)
        self.assertEqual(ExitCode.exception.code, 1)


# Remove directories at end of test.
reset_directories()
