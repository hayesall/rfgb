"""
Copyright (C) 2017-2018 RFGB Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program (at the base of this repository). If not,
see <http://www.gnu.org/licenses/>
"""

from __future__ import print_function

from rfgb.utils import Utils
from rfgb.tree import node
from rfgb.boosting import updateGradients
from rfgb.boosting import performInference

import argparse

class Arguments:
    """@batflyer:

    For backward compatability reasons, flags ideally should function the same
    as they do in the Java code base.

    All flags which are valid in the Java distribution should also be valid in
    the Python version.

    For example, arguments for the former should work on the latter:
    $ java BoostSRL.jar ...
    $ python BoostSRL.py ...
    """

    def __init__(self):

        # Create an argument parser for interpreting user inputs.
        parser = argparse.ArgumentParser(prog="\n\n $ python RFGB.py",
                description="""RFGB: Relational Functional Gradient Boosting is
                a gradient-boosting approach to learning statistical relational
                models.
                """,
                epilog="""Copyright 2017-2018 RFGB Contributors. Distributed
                under the terms of the GNU GPL version 3 or later
                <http://gnu.org/licenses/gpl.html>.

                This is free software: you are free to change and redistribute
                it. There is NO WARRANTY, to the extent permitted by law.
                """)

        # Mutually exclusive group for learning or inference.
        learn_or_infer = parser.add_mutually_exclusive_group()
        learn_or_infer.add_argument("-l", "--learn", action="store_true",
                                    help="Learn a model from data.")
        learn_or_infer.add_argument("-i", "--infer", action="store_true",
                                    help="""Make inferences about data
                                    using a model.""")

        # Add in the arguments.
        parser.add_argument("-v", "-verbose", "--verbose",
                            help="Increase verbosity to help with debugging.",
                            default=False,
                            action="store_true")
        parser.add_argument("-trees", "--trees",
                            help="""Specify a number of boosted trees to learn.
                            Default: 10.""",
                            type=int,
                            default=10)
        parser.add_argument("-target", "--target",
                            help="""Target predicates to perform learning or
                            inference on.""",
                            type=str,
                            default=None,
                            action="append")
        parser.add_argument("-expAdvice", "--expAdvice",
                            help="...",
                            default=False,
                            action="store_true")
        parser.add_argument("-reg", "--reg",
                            help="""Use relational regression instead of
                            classification.""",
                            default=False,
                            action="store_true")

        # Optionally set the paths for train/test directory
        # (Utils.py will need to be updated to reference these.)
        parser.add_argument("-train", "--train", type=str, default="train/")
        parser.add_argument("-test", "--test", type=str, default="test/")

        # Get the arguments.
        self.args = parser.parse_args()


        """
        # Options such as this are possible, but not used in this way.
        self.expAdvice = self.args.expAdvice   # -expAdvice, --expAdvice
        self.verbose = self.args.verbose       # -v, -verbose, --verbose
        self.trees = self.args.trees           # -trees, --trees
        self.target = self.args.target         # -target, --target
        self.reg = self.args.reg               # -reg, --reg
        """

def main():
    '''main method'''
    parameters = Arguments().args
    #print(parameters)

    for target in parameters.target:

        # Read the training data.
        trainData = Utils.readTrainingData(target, path=parameters.train,
                                           regression=parameters.reg,
                                           advice=parameters.expAdvice)

        # Initialize an empty place holder for the trees.
        trees = []

        # Learn each tree and update the gradient.
        for i in range(parameters.trees):

            if parameters.verbose:
                print('='*20, "learning tree", str(i), '='*20)

            node.setMaxDepth(2)
            node.learnTree(trainData) # Learn relational regression tree
            trees.append(node.learnedDecisionTree)
            updateGradients(trainData, trees)

        for tree in trees:

            if parameters.verbose:
                print('='*30, "tree", str(trees.index(tree)), '='*30)

            for clause in tree:
                print(clause)

        # Read the testing data.
        testData = Utils.readTestData(target, path=parameters.test,
                                      regression=parameters.reg)
        # Get the probability of the test examples.
        #Boosting.performInference(testData, trees)
        performInference(testData, trees)

        if parameters.reg:
            # View test example values (for regression)
            print(testData.examples)
        else:
            # View test query probabilities (for classification)
            print(testData.pos)
            print(testData.neg)

if __name__ == '__main__':
    main()
