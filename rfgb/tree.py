
# Copyright (C) 2017-2018 RFGB Contributors

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program (at the base of this repository). If not,
# see <http://www.gnu.org/licenses/>

"""
(docstring)
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from .utils import Utils
from .logic import Logic
from .logic import Prover

from copy import deepcopy
import random


class node:
    """
    A node in a tree.

    Overview of the following variables and structures:

    - ``expandQueue``: Breadth-first search node expansion strategy.
    - ``depth``: Initially set to 0 because no node is present.
    - ``maxDepth``: 1 because we want to learn a tree with at least depth 1.
    - ``learnedDecisionTree``: will hold all of the learned clauses.
    - ``data``: stores the facts and positive/negative examples.

    Constructor for the node class.

    :param test: Test condition or a horn clause.
    :param exampels: All examples that are available for testing at
                     this node.
    :param information: Information notion (some score) contained at this
                        node.
    :param level: Level in the tree of node.
    :param parent: Pointer to the parent node.
    :param pos: Position in the tree (i.e. "left" or "right").
    """

    expandQueue = []
    depth = 0
    maxDepth = 1
    learnedDecisionTree = []
    data = None

    def __init__(self, test=None, examples=None, information=None,
                 level=None, parent=None, pos=None):
        self.test = test

        if level > 0:
            # If not root, set the parent node.
            self.parent = parent
        else:
            # otherwise, set parent to 'root' to signify the root.
            self.parent = 'root'

        # Position of the node, i.e. 'left' or 'right'.
        self.pos = pos
        self.examples = examples #all examples that are available for testing at this node
        self.information = information #information contained at this node
        self.level = level #level of the node, 0 for root
        self.left = None #left subtree
        self.right = None #right subtree
        node.expandQueue.insert(0,self) #add to the queue of nodes to expand

    @staticmethod
    def setMaxDepth(depth):
        """
        Method for setting the max depth of the tree.
        """
        node.maxDepth = depth

    @staticmethod
    def initTree(trainingData):
        """Method for creating the root node."""

        node.data = trainingData
        node.expandQueue = [] #reset node queue for every tree to be learned
        node.learnedDecisionTree = [] #reset clauses for every tree to be learned

        if trainingData.regression:
            # Regression examples can be collected from trainingData.examples (since there are no pos/neg).
            examples = trainingData.examples.keys()
        else:
            # For all other models, we consider a set of positive and negative examples.
            examples = list(trainingData.pos.keys()) + list(trainingData.neg.keys())

        node(None, examples, trainingData.variance(examples), 0, 'root')

    @staticmethod
    def learnTree(data):
        '''method to learn the decision tree'''

        node.initTree(data) #create the root
        while len(node.expandQueue) > 0:
            curr = node.expandQueue.pop()
            curr.expandOnBestTest(data)
        node.learnedDecisionTree.sort(key = len)
        node.learnedDecisionTree = node.learnedDecisionTree[::-1]

    def getTrueExamples(self, clause, test, data, verbose=False):
        """
        Returns all examples that satisfy the clause with
        conjoined test literal.
        """

        # Initialize list of true examples.
        tExamples = []
        clauseCopy = deepcopy(clause)

        # Construct clause for prover.
        if clauseCopy[-1] == "-":
            clauseCopy += test
        elif clauseCopy[-1] == ';':
            clauseCopy = clauseCopy.replace(';', ',') + test

        if verbose:
            print("Testing clause", clauseCopy)

        # To keep track of output, the following for loop can be parallellized
        for example in self.examples:
            # Prove if example satisfies clause.
            if Prover.prove(data, example, clauseCopy):
                tExamples.append(example)
        return tExamples

    def expandOnRandomTest(self, data=None, verbose=False):
        """
        Expands the node randomly.
        """

        # Get the target, initialize the clause learned at this node with an
        # empty body. Loop to obtain clause learned at this node.
        target = data.getTarget()
        clause = target + ':-'
        curr = self
        ancestorTests = []

        while curr.parent != 'root':
            if curr.pos == 'left':
                clause += curr.parent.test + ';'
                ancestorTests.append(curr.parent.test)
            elif curr.pos == 'right':
                ancestorTests.append(curr.parent.test)
                # What is this?
                clause += '' # "!" + curr.parent.test + ','
            curr = curr.parent

        if self.level == node.maxDepth or round(self.information, 3) == 0:
            if clause[-1] != '-':
                node.learnedDecisionTree.append(clause[:-1] + ' ' +
                                        str(Utils.getleafValue(self.examples)))
            else:
                node.learnedDecisionTree.append(clause + ' ' +
                                        str(Utils.getleafValue(self.examples)))
            return

        if clause[-2] == '-':
            clause = clause[:-1]

        if verbose:
            print('-' * 80)
            print('pos:', self.pos)
            print('node depth:', self.level)
            print('parent:', self.parent)
            print('examples at node:', self.examples)
            if self.parent != 'root':
                print('test at parent:', self.parent.test)
            print('clause for generate test at current node', clause)

        # Initialize values for deciding the test to expand on.
        minScore = float('inf')
        bestTest = ''
        # Initialize lists for test examples that do or do not satisfy the
        # clause. Then get all literals that the facts contain.
        bestTExamples = []
        bestFExamples = []
        literals = data.getLiterals()

        tests = []
        # For each literal, generate test conditions.
        for literal in literals:
            literalName = literal
            literalTypeSpecification = literals[literal]
            # Generate all literal, variable, and constant combinations.
            tests += Logic.generateTests(literalName,
                                         literalTypeSpecification,
                                         clause)
        if self.parent != 'root':
            tests = set([test for test in tests if not test in ancestorTests])

        # Select a random test:
        bestTest = random.sample(tests, 1)

        # Examples which are satisfied by this test are the "best".
        bestTExamples = self.getTrueExamples(clause, bestTest, data)
        bestFExamples = [example for example in self.examples if example not in bestTExamples]
        example_len = len(self.examples)

        self.test = bestTest

        if verbose:
            print('Random test selected at current node:', self.test)

        # If True examples need further explaining,
        # create left node and add to the queue.
        if len(bestTExamples) > 0:

            self.left = node(None, bestTExamples, data.variance(bestTExamples),
                             self.level + 1, self, 'left')
            if self.level + 1 > node.depth:
                node.depth = self.level + 1

        # If False examples need further explaining,
        # create right node and add to the queue.
        if len(bestFExamples) > 0:

            self.right = node(None, bestFExamples, data.variance(bestFExamples),
                              self.level + 1, self, 'right')

            if self.level + 1 > node.depth:
                node.depth = self.level + 1

        # If no examples append to clause as is.
        if self.test == '' or round(self.information, 3) == 0:
            if clause[-1] != '-':
                node.learnedDecisionTree.append(clause[:-1])
            else:
                node.learnedDecisionTree.append(clause)
            return


    def expandOnBestTest(self, data=None, verbose=False):
        """
        Expands the node based on the best test.
        """

        target = data.getTarget() #get the target
        clause = target+":-" #initialize clause learned at this node with empty body
        curr = self #while loop to obtain clause learned at this node
        ancestorTests = []
        while curr.parent!="root":
            if curr.pos == "left":
                clause += curr.parent.test+";"
                ancestorTests.append(curr.parent.test)
            elif curr.pos == "right":
                ancestorTests.append(curr.parent.test)
                clause += ""#"!"+curr.parent.test+","
            curr = curr.parent
        if self.level == node.maxDepth or round(self.information,3) == 0:
            if clause[-1]!='-':
                node.learnedDecisionTree.append(clause[:-1]+" "+str(Utils.getleafValue(self.examples)))
            else:
                node.learnedDecisionTree.append(clause+" "+str(Utils.getleafValue(self.examples)))
            return
        if clause[-2] == '-':
            clause = clause[:-1]

        if verbose:
            print('-'*80)
            #print "facts: ",data.getFacts()
            print("pos: ",self.pos)
            print("node depth: ",self.level)
            print("parent: ",self.parent)
            print("examples at node: ",self.examples)
            if self.parent != "root":
                print("test at parent: ",self.parent.test)
            print("clause for generate test at current node: ",clause)

        #print "examples at current node: ",self.examples
        minScore = float('inf') #initialize minimum weighted variance to be 0
        bestTest = "" #initalize best test to empty string
        bestTExamples = [] #list for best test examples that satisfy clause
        bestFExamples = [] #list for best test examples that don't satisfy clause
        literals = data.getLiterals() #get all the literals that the data (facts) contains
        tests = []

        for literal in literals: #for every literal generate test conditions
            literalName = literal
            literalTypeSpecification = literals[literal]
            tests += Logic.generateTests(literalName,literalTypeSpecification,clause) #generate all possible literal, variable and constant combinations

        if self.parent != 'root':
                tests = [test for test in tests if not test in ancestorTests]

        tests = set(tests)

        # Check which test scores the best.
        for test in tests:
            # Examples which are satisfied.
            tExamples = self.getTrueExamples(clause, test, data, verbose=True)
            # Examples which are not satisfied (under closed world assumption).
            fExamples = [example for example in self.examples if example not in tExamples]
            # Total number of examples.
            example_len = len(self.examples)

            # Calculated the weighted variance:
            score = ((len(tExamples)/example_len) * data.variance(tExamples) +
                     (len(fExamples)/example_len) * data.variance(fExamples))

            #score = ((len(tExamples)/float(len(self.examples)))*Utils.variance(tExamples) + (len(fExamples)/float(len(self.examples)))*Utils.variance(fExamples))

            if score < minScore: #if score lower than current lowest
                minScore = score #assign new minimum
                bestTest = test #assign new best test
                bestTExamples = tExamples #collect satisfied examples
                bestFExamples = fExamples #collect unsatisfied examples
        Utils.addVariableTypes(bestTest) #add variable types of new variables
        self.test = bestTest #assign best test after going through all literal specs

        print("Best test found at the current node:", self.test, score)

        # If True examples need further explaining, create left node and add to the queue.
        if len(bestTExamples) > 0:

            self.left = node(None, bestTExamples, data.variance(bestTExamples), self.level+1, self, "left")

            #self.left = node(None,bestTExamples,Utils.variance(bestTExamples),self.level+1,self,"left")
            if self.level+1 > node.depth:
                node.depth = self.level+1

        # If False examples need further explaining, create right node and add to the queue.
        if len(bestFExamples) > 0:

            self.right = node(None, bestFExamples, data.variance(bestFExamples), self.level+1, self, "right")

            #self.right = node(None,bestFExamples,Utils.variance(bestFExamples),self.level+1,self,"right")

            if self.level+1 > node.depth:
                node.depth = self.level+1
        if self.test == "" or round(self.information,3) == 0: #if no examples append clause as is
            if clause[-1]!='-':
                node.learnedDecisionTree.append(clause[:-1])
            else:
                node.learnedDecisionTree.append(clause)
            return
