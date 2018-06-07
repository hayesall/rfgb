
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
-------

(docstring for main function)
"""

from __future__ import print_function
from __future__ import absolute_import

from .boosting import updateGradients
from .boosting import performInference
from .tree import node
from .utils import Utils

import argparse

class Arguments:
    """
    For backwards compatability with the Java codebase, flags should ideally
    perform the same functions. In cases where performing the same functions
    would be grossly misguided, follow with appropriate documentation.

    For example:

    .. code-block:: bash

                    $ java rfgb.jar ...
                    $ python rfgb.py ...
    """

    def __init__(self):

        # Create an argument parser for interpretting user inputs.
        parser = argparse.ArgumentParser(description="""rfgb.py: Relational
                                         Functional Gradient Boosting is a
                                         gradient-boosting approach to learning
                                         statistical relational models.
                                         """,
                                         epilog="""Copyright 2017-2018 RFGB
                                         Contributors. Distributed under the
                                         terms of the GNU GPL version 3 or
                                         later.
                                         <http://gnu.org/licenses/gpl.html>

                                         This is free software: you are free
                                         to change and redistribute it. There
                                         is NO WARRANTY, to the extent
                                         permitted by law.""")

        # Mutually exclusive group for performing learning or inference
        learn_or_infer = parser.add_mutually_exclusive_group()
        learn_or_infer.add_argument("-l", "--learn", action="store_true",
                                    help="Learn a model from data.")
        learn_or_infer.add_argument("-i", "--infer", action="store_true",
                                    help="Test data with a model.")

        # Add in the arguments
        parser.add_argument("-v", "-verbose", "--verbose",
                            help="Incrase verbosity to help with debugging.",
                            default=False,
                            action="store_true")
        parser.add_argument("-trees", "--trees",
                            help="""Specify the number of boosted regression
                            trees to learn. Default: 10.""",
                            type=int,
                            default=10)
        parser.add_argument("-target", "--target",
                            help="Target predicate(s) to learn/infer about.",
                            type=str,
                            default=None,
                            action="append")
        parser.add_argument("-expAdvice", "--expAdvice",
                            help="""Trigger learning with expert advice.
                            Currently reads from an advice.txt file stored
                            in the same location as the data.""",
                            default=False,
                            action="store_true")
        parser.add_argument("-reg", "--reg",
                            help="""Learn a relational regression model instead
                            of learning for classification.""",
                            default=False,
                            action="store_true")

        # Optionally set the paths for train/test directory.
        parser.add_argument("-train", "--train", type=str, default="train/")
        parser.add_argument("-test", "--test", type=str, default="test/")

        # Get the arguments
        self.args = parser.parse_args()

parameters = Arguments().args

for target in parameters.target:

    # Read the training data:
    trainData = Utils.readTrainingData(target, path=parameters.train,
                                       regression=parameters.reg,
                                       advice=parameters.expAdvice)

    # Initialize an empty list for the trees.
    trees = []

    # Learn each tree and update the gradients.
    for i in range(parameters.trees):

        if parameters.verbose:
            print('=' * 20, "Learning Tree", str(i), "=" * 20)

        node.setMaxDepth(2)
        node.learnTree(trainData)
        trees.append(node.learnedDecisionTree)
        updateGradients(trainData, trees)

    for tree in trees:

        if parameters.verbose:
            print('=' * 20, "Tree", str(trees.index(tree)), "=" * 20)

        for clause in tree:

            if parameters.verbose:
                print(clause)

    # Read the testing data.
    testData = Utils.readTestData(target, path=parameters.test,
                                  regression=parameters.reg)

    # Get the probability of the test examples.
    performInference(testData, trees)

    if parameters.reg:
        # View test example values (for regression).
        print(testData.examples)
    else:
        # View test query probabilities (for classification).
        print(testData.pos)
        print(testData.neg)

# Exit with no errors if the bottom is reached successfully.
exit(0)
