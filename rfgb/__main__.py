
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

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from .boosting import updateGradients
from .boosting import performInference
from .tree import node
from .utils import Utils
from ._metadata import __version__
from . import rdn

import argparse


"""
For backwards compatability with the Java codebase, flags should ideally
perform the same functions. In cases where performing the same functions
would be grossly misguided, follow with appropriate documentation.

For example:

.. code-block:: bash

                $ java rfgb.jar ...
                $ python rfgb.py ...
"""

# Create an argument parser for interpretting user inputs.
parser = argparse.ArgumentParser(description="""rfgb.py: Relational Functional
                                 Gradient Boosting is a gradient-boosting
                                 approach to learning statistical relational
                                 models.
                                 """,
                                 epilog="""Copyright 2017-2018 RFGB
                                 Contributors. Distributed under the terms of
                                 the GNU GPL version 3 or later.
                                 <http://gnu.org/licenses/gpl.html>

                                 This is free software: you are free to change
                                 and redistribute it. There is NO WARRANTY, to
                                 the extent permitted by law.""")

parser.add_argument('-V', '--version', action="store_true",
                    help="show version number and exit")

# Create subparsers for learning different types of models, their respective
# arguments may be set individually (for example, if advice is implemented
# for RDNs but has not been worked out for MLNs).

# This is different from BoostSRL's codebase, where the default is RDN and
# MLNs are learned by supplying a -mln flag. This change is to make things
# more-easily extended in the future.
subparsers = parser.add_subparsers(title='Models',
                                   description="""Subcommands for learning
                                   different types of models.""",
                                   help="""$ python -m rfgb rdn""",
                                   dest='model')
rdn_parser = subparsers.add_parser('rdn', description="""Relational Dependency
                                   Networks""")
mln_parser = subparsers.add_parser('mln', description="""Markov Logic
                                   Networks: Hopefully coming soon! (TM)""")

# RDN-specific arguments.
rdn_parser.add_argument('-advice', '--advice', help="""Trigger learning with
                        expert advice. Currently reads from an advice.txt
                        file stored in the same location as the data.""",
                        action="store_true")
rdn_parser.add_argument('-reg', '--regression', help="""Learn a regression
                        model instead of a classification model.""",
                        action="store_true")
rdn_learn_or_infer = rdn_parser.add_mutually_exclusive_group()
rdn_learn_or_infer.add_argument('-l', '--learn', action='store_true',
                                help='Learn an RDN.')
rdn_learn_or_infer.add_argument('-i', '--infer', action='store_true',
                                help='Infer with an RDN.')

# Control what is displayed on the console,
# either a verbose output, a progress bar, or nothing at all.
console = rdn_parser.add_mutually_exclusive_group()
console.add_argument("-v", "-verbose", "--verbose", action="store_true",
                     help="Print outputs and logs to console.")
console.add_argument("-q", "-quiet", "--quiet", action="store_true",
                     help="Display nothing on the console.")
console.add_argument("-p", "-progress", "--progress", action="store_true",
                     help="Display a tqdm progress bar.")

output_style = rdn_parser.add_mutually_exclusive_group()
output_style.add_argument("-log", "--log", action="store_true",
                          help="Log outputs to a file.")

rdn_parser.add_argument("-trees", "--trees", type=int, default=10,
                    help="""Specify the number of boosted regression
                    trees to learn. Default: 10.""")
rdn_parser.add_argument("-target", "--target",
                    type=str, default=None, action='append',
                    help="Target predicate(s) to learn/infer about.")

# Arguments for setting inputs and outputs.
rdn_parser.add_argument("-train", "--train", type=str, default="train/",
                    help="""Set the training directory.""")
rdn_parser.add_argument("-test", "--test", type=str, default="test/",
                    help="""Set the testing directory.""")

# Get the arguments
parameters = parser.parse_args()

if parameters.version:
    print(__version__)
    exit(0)

def LearnMLN():
    print('Coming Soon.')

# RDN Learning and Inference
if parameters.model == 'rdn':

    # Learn a set of trees.
    trees = rdn.learn(parameters.target, path=parameters.train,
                      numTrees=parameters.trees,
                      regression=parameters.regression,
                      advice=parameters.advice)

    # Make inferences for each target.
    for target in trees:
        results = rdn.infer(target, trees[target], path=parameters.test,
                            regression=parameters.regression)

        print(results)

elif parameters.model == 'mln':
    LearnMLN()
else:
    raise(Exception('Tried to invoke a model that is not possible.'))

exit(0)
"""
for target in parameters.target:

    # Read the training data:
    trainData = Utils.readTrainingData(target, path=parameters.train,
                                       regression=parameters.regression,
                                       advice=parameters.advice)

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
                                  regression=parameters.regression)

    # Get the probability of the test examples.
    performInference(testData, trees)

    if parameters.regression:
        # View test example values (for regression).
        print(testData.examples)
    else:
        # View test query probabilities (for classification).
        print(testData.pos)
        print(testData.neg)

# Exit with no errors if the bottom is reached successfully.
exit(0)
"""
