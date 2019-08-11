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
rfgb
====

Provides
    1. The ability to perform Relational Functional Gradient Boosting (RFGB)
       in Python.

Documentation
-------------

The vast majority of documentation is currently provided in-line with the
code, mostly consisting of high-level overviews and some usage examples.

As this grows in complexity, documentation will likely be found in either
the doc strings for individual functions (i.e. rfgb.__doc__), or online.
"""

from .utils import Utils
from .tree import node
from .boosting import updateGradients
from .boosting import performInference

from ._metadata import (
    __author__,
    __maintainer__,
    __email__,
    __copyright__,
    __license__,
    __version__,
    __status__,
)
