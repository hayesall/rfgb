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
.. versionadded:: 0.3.0

Learn and infer with relational dependency networks.

.. code-block:: python

    # Example script for performing learning and inference.

    from rfgb import rdn

    # rdn.learn requires a list of targets as strings.
    trees = rdn.learn(['cancer'], path='testDomains/ToyCancer/train/')

    # rdn.learn returns a dictionary mapping targets to trees.
    cancer_trees = trees['cancer']

    # rdn.infer classification returns a tuple of pos and neg.
    results = rdn.infer('cancer', cancer_trees, path='testDomains/ToyCancer/test/')

    # ({'cancer(xena)': 0.34460796550872186,
    #   'cancer(yoda)': 0.34460796550872186,
    #   'cancer(zod)': 0.34460796550872186},
    #  {'cancer(watson)': 0.34460796550872186,
    #   'cancer(voldemort)': 0.34460796550872186})
"""

from .learn import learn
from .infer import infer
