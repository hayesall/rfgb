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
Initializes an empty .rfgb directory for storing models and metadata.
"""

from __future__ import print_function

import os
import sys


def init(quiet=False):

    if not os.path.exists(".rfgb"):
        os.makedirs(".rfgb")
        os.makedirs(".rfgb/models/")

        if not quiet:
            print(
                "Initialized empty rfgb repository at", os.path.abspath(".") + "/.rfgb/"
            )
    else:
        print(".rfgb/ already exists.", file=sys.stderr)
        exit(1)
