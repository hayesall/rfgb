
# Copyright (C) 2017-2018 RFGB Contributors
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
rfgb.py
=======

Provides
    1. The ability to perform Relational Functional Gradient Boosting (RFGB)
       in Python.

Documentation
-------------

The vast majority of documentation is currently provided in-line with the
code, mostly consisting of high-level overviews and some usage examples.

As this grows in complexity, documentation will likely be found in either
the doc strings for individual functions (i.e. rfgb.__doc__), or online as
https://starling.utdallas.edu/
"""

from rfgb.utils import Utils
from rfgb.tree import node
from rfgb.boosting import updateGradients
from rfgb.boosting import performInference

__author__ = 'Kaushik Roy (@kkroy36)'
__copyright__ = 'Copyright (c) 2017-2018 RFGB Contributors'
__license__ = 'GNU General Public License v3.0 (GPLv3)'
__version__ = '0.2.0'
__maintainer__ = 'Alexander L. Hayes'
__email__ = 'alexander.hayes@utdallas.edu'
__status__ = 'Prototype'
