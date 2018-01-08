from __future__ import print_function

from Utils import Utils
from Tree import node
from Boosting import Boosting
#from sys import argv

import argparse

class Arguments:
    """
    @batflyer:
    For backward compatability reasons, flags should function the same as they do in the Java code base.
    All flags which are valid in the Java distribution should also be valid in the Python version.

    For example, arguments for the former should work on the latter:
    $ java BoostSRL.jar ...
    $ python BoostSRL.py ...
    """

    def __init__(self):

        self.advice = False      # -expAdvice
        self.regression = False  # -reg
        self.verbose = False     # -v, -verbose, --verbose
        self.train = 'train'     # -train, --train
        self.test = 'test'       # -test, --test
        self.target = []         # -target, --target
        self.trees = 10          # -trees, --trees

        # Create an argument parser for interpreting user inputs.
        parser = argparse.ArgumentParser(prog="\n\n $ python RFGB.py",
                                         description="RFGB: Functional Gradient Boosting is a gradient-boosting approach to learning statistical relational models.",
                                         epilog="Copyright 2018 Free Software Foundation, Inc. License GPLv3+: GPU GPL version 3 or later <http://gnu.org/licenses/gpl.html>. This is free software: you are free to change and redistribute it. There is NO WARRANTY, to the extent permitted by law.")

        # Add in the arguments.
        parser.add_argument("-v", "-verbose", "--verbose",
                            help="Increase verbosity to help with debugging.",
                            action="store_true")
        parser.add_argument("-trees", "--trees",
                            help="Specify a number of boosted trees to learn. Default: 10.",
                            type=int,
                            default=10)
        parser.add_argument("-target", "--target",
                            help="Target predicates to perform learning or inference on.",
                            type=str,
                            action="append")
        parser.add_argument("-expAdvice",
                            help="...",
                            action="store_true")
        parser.add_argument("-reg",
                            help="Use relational regression instead of classification.",
                            action="store_true")

        # Get the arguments.
        self.args = parser.parse_args()
        
def main():
    '''main method'''
    parameters = Arguments().args
    print(parameters)

    for target in parameters.target:

        # Read the training data.
        data = Utils.readTrainingData(target, parameters.reg, parameters.expAdvice)
        # Initialize an empty place holder for the trees.
        trees = []

        # Learn each tree and update the gradient.
        for i in range(parameters.trees):
            
            if parameters.verbose:
                print('='*20, "learning tree", str(i), '='*20)
                
            node.setMaxDepth(2)
            node.learnTree(data) # Learn relational regression tree
            trees.append(node.learnedDecisionTree)
            Boosting.updateGradients(data, trees)

        for tree in trees:

            if parameters.verbose:
                print('='*30, "tree", str(trees.index(tree)), '='*30)
                
            for clause in tree:
                print(clause)

        # Read the testing data.
        testData = Utils.readTestData(target, parameters.reg)
        # Get the probability of the test examples.
        Boosting.performInference(testData, trees)

        #print testData.pos #--> uncomment to see test query probabilities (for classification)
        #print testData.neg

        #print testData.examples #--> uncomment to see test example values (for regression)

if __name__ == '__main__':
    """
    @batflyer
    Adding this section so RFGB can be either ran as an executable, or
    imported as a Python package (a la boostsrl-python-package).
    """
    main()
