from __future__ import print_function

from Utils import Utils
from Tree import node
from Boosting import Boosting
#from sys import argv

import argparse

class Arguments:
    """@batflyer:

    For backward compatability reasons, flags should function the same as they do in the Java code base.
    All flags which are valid in the Java distribution should also be valid in the Python version.

    For example, arguments for the former should work on the latter:
    $ java BoostSRL.jar ...
    $ python BoostSRL.py ...
    """

    def __init__(self):
        
        # Create an argument parser for interpreting user inputs.
        parser = argparse.ArgumentParser(prog="\n\n $ python RFGB.py",
                                         description="RFGB: Functional Gradient Boosting is a gradient-boosting approach to learning statistical relational models.",
                                         epilog="Copyright 2018 Free Software Foundation, Inc. License GPLv3+: GPU GPL version 3 or later <http://gnu.org/licenses/gpl.html>. This is free software: you are free to change and redistribute it. There is NO WARRANTY, to the extent permitted by law.")

        # Mutually exclusive group for learning or inference.
        learn_or_infer = parser.add_mutually_exclusive_group()
        learn_or_infer.add_argument("-l", "--learn", action="store_true", help="Learn a model from data.")
        learn_or_infer.add_argument("-i", "--infer", action="store_true", help="Make inferences about data using a model.")

        # Add in the arguments.
        parser.add_argument("-v", "-verbose", "--verbose",
                            help="Increase verbosity to help with debugging.",
                            default=False,
                            action="store_true")
        parser.add_argument("-trees", "--trees",
                            help="Specify a number of boosted trees to learn. Default: 10.",
                            type=int,
                            default=10)
        parser.add_argument("-target", "--target",
                            help="Target predicates to perform learning or inference on.",
                            type=str,
                            default=None,
                            action="append")
        parser.add_argument("-expAdvice", "--expAdvice",
                            help="...",
                            default=False,
                            action="store_true")
        parser.add_argument("-reg", "--reg",
                            help="Use relational regression instead of classification.",
                            default=False,
                            action="store_true")

        # Optionally set the paths for train/test directory (Utils.py will need to be updated to reference these.)
        parser.add_argument("-train", "--train", type=str, default="train/")
        parser.add_argument("-test", "--test", type=str, default="test/")

        # Get the arguments.
        self.args = parser.parse_args()


        """@batflyer

        Adding these here for completeness, currently they are not referenced anywhere in the program.
        """
        self.expAdvice = self.args.expAdvice   # -expAdvice, --expAdvice
        self.verbose = self.args.verbose       # -v, -verbose, --verbose
        self.trees = self.args.trees           # -trees, --trees
        self.target = self.args.target         # -target, --target
        self.reg = self.args.reg               # -reg, --reg

def main():
    '''main method'''
    parameters = Arguments().args
    #print(parameters)

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
