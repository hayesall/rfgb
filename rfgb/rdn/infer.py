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

from ..boosting import performInference
from ..utils import Utils


def infer(target, trees, path="", regression=False):
    """
    .. versionadded:: 0.3.0

    Perform inference on data with a set of trees.

    .. note:: This currently requires that test data is stored as files
              on disk.

    :param trees: Trees to perform inference with.
    :type trees: list of str.

    :param path: Path to the location test data is stored.
    :type path: str.

    :param regression: Infer with a regression model instead of classification.
    :type regression: bool.

    :default regression: False

    :returns: Tuple of results. In classification these results will be a tuple
              of positive and negative examples. In regression this will be
              the examples.
    :rtype: tuple
    """

    # Read the testing data.
    testData = Utils.readTestData(target, path=path, regression=regression)

    # Get the probability of the test examples.
    performInference(testData, trees)

    if regression:
        return testData.examples
    else:
        return (testData.pos, testData.neg)
