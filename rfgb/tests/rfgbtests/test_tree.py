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

from __future__ import print_function
from __future__ import absolute_import
from ...tree import node
import unittest


class TreeTest(unittest.TestCase):
    def test_setNodeDepth(self):

        node.setMaxDepth(1)
        self.assertEqual(node.maxDepth, 1)

        node.setMaxDepth(2)
        self.assertEqual(node.maxDepth, 2)

        node.setMaxDepth(3)
        self.assertEqual(node.maxDepth, 3)

        node.setMaxDepth(100)
        self.assertEqual(node.maxDepth, 100)
