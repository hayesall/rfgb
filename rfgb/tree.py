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
Data structures and methods for learning decision trees.
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from .utils import Utils
from .logic import Logic
from .logic import Prover

from copy import deepcopy


class node:
    """
    A node in a tree.

    :param expandQueue: Breadth first search node expansion strategy
    :param depth: initial depth is 0 because no node present
    :param maxDepth: max depth set to 1 because we want to at least learn a tree of depth 1
    :param learnedDecisionTree: this will hold all the clauses learned
    :param data: stores all the facts, positive and negative examples
    """

    expandQueue = []
    depth = 0
    maxDepth = 1
    learnedDecisionTree = []
    data = None

    def __init__(
        self,
        test=None,
        examples=None,
        information=None,
        level=None,
        parent=None,
        pos=None,
    ):
        """
        Constructor for node class.

        :param test: Test condition in the form of a horn clause.
        :param examples: Examples available for testing at this node.
        :param information: Information contained at this node.
        :param level: Level of this node in the tree (0 for root).
        :param parent: "root", or a pointer to the parent.
        :param pos: Position in the tree ('left' or 'right')
        """
        self.test = test
        if level > 0:
            self.parent = parent
        else:
            self.parent = "root"
        self.pos = pos
        self.examples = examples
        self.information = information
        self.level = level
        self.left = None
        self.right = None

        # Add to the queue of nodes to expand.
        node.expandQueue.insert(0, self)

    @staticmethod
    def setMaxDepth(depth):
        """
        Set the maximum depth of the tree.
        """
        node.maxDepth = depth

    @staticmethod
    def initTree(trainingData):
        """
        Create the root node of the tree.
        """

        node.data = trainingData

        # Reset node queue for every tree to be learned.
        node.expandQueue = []
        # Reset clauses for every tree to be learned.
        node.learnedDecisionTree = []

        if trainingData.regression:
            # Regression examples can be collected from trainingData.examples
            # (since there are no pos/neg).
            examples = trainingData.examples.keys()
        else:
            # For all other models, we consider a set of positive and
            # negative examples.
            examples = list(trainingData.pos.keys()) + list(trainingData.neg.keys())

        node(
            test=None,
            examples=examples,
            information=trainingData.variance(examples),
            level=0,
            parent="root",
        )

    @staticmethod
    def learnTree(data):
        """
        Method to create and learn the decision tree.
        """

        # Create the root
        node.initTree(data)

        while len(node.expandQueue) > 0:
            current = node.expandQueue.pop()
            current.expandOnBestTest(data)

        node.learnedDecisionTree.sort(key=lambda x: len(x.split(" ")[0]))
        node.learnedDecisionTree = node.learnedDecisionTree[::-1]

    def getTrueExamples(self, clause, test, data):
        """
        Returns all examples that satisfy the clause
        with conjoined test literal.
        """

        # Initialize a list of true examples.
        trueExamples = []
        clauseCopy = deepcopy(clause)

        # Construct clause for prover
        if clauseCopy[-1] == "-":
            clauseCopy += test
        elif clauseCopy[-1] == ";":
            clauseCopy = clauseCopy.replace(";", ",") + test

        # Prove if example satisfies clause.
        for example in self.examples:
            if Prover.prove(data, example, clauseCopy):
                trueExamples.append(example)
        return trueExamples

    def expandOnBestTest(self, data=None):
        """
        Expand the node based on the best test.
        """

        target = data.getTarget()
        # Initialize clause learned at this node with empty body.
        clause = target + ":-"

        current = self
        ancestorTests = []
        while current.parent != "root":

            if current.pos == "left":
                clause += current.parent.test + ";"
                ancestorTests.append(current.parent.test)
            elif current.pos == "right":
                ancestorTests.append(current.parent.test)

            current = current.parent

        if self.level == node.maxDepth or round(self.information, 3) == 0:

            if clause[-1] != "-":
                node.learnedDecisionTree.append(
                    clause[:-1] + " " + str(Utils.getleafValue(self.examples))
                )
            else:
                node.learnedDecisionTree.append(
                    clause + " " + str(Utils.getleafValue(self.examples))
                )
            return

        if clause[-2] == "-":
            clause = clause[:-1]

        # Initialize minimum weighted variance to a low value.
        minScore = float("inf")
        bestTest = ""

        # List for best test  examples which satisfy  or do not satisfy clause.
        bestTExamples, bestFExamples = [], []
        # Get all the literals contained in the facts.
        literals = data.getLiterals()

        tests = []
        # For every literal generate test conditions.
        for literal in literals:
            literalName = literal[0]
            literalTypeSpecification = literal[1]

            # Generate all possible literal, variable, and constant combinations
            tests += Logic.generateTests(literalName, literalTypeSpecification, clause)

        if self.parent != "root":
            tests = [test for test in tests if not test in ancestorTests]
        tests = set(tests)

        # Check which test scores the best.
        for test in tests:
            # Examples which are satisfied.
            tExamples = self.getTrueExamples(clause, test, data)
            # Examples which are not satisfied (under closed world assumption).
            fExamples = [
                example for example in self.examples if example not in tExamples
            ]
            # Total number of examples.
            example_len = len(self.examples)

            # Calculated the weighted variance:
            score = (len(tExamples) / example_len) * data.variance(tExamples) + (
                len(fExamples) / example_len
            ) * data.variance(fExamples)

            if score < minScore:  # if score lower than current lowest
                minScore = score  # assign new minimum
                bestTest = test  # assign new best test
                bestTExamples = tExamples  # collect satisfied examples
                bestFExamples = fExamples  # collect unsatisfied examples
        Utils.addVariableTypes(bestTest)  # add variable types of new variables
        self.test = bestTest  # assign best test after going through all literal specs

        print("Best test found at the current node: ", self.test)

        # If True examples need further explaining,
        # create left node and add to the queue.
        if len(bestTExamples) > 0:

            self.left = node(
                test=None,
                examples=bestTExamples,
                information=data.variance(bestTExamples),
                level=self.level + 1,
                parent=self,
                pos="left",
            )

            if self.level + 1 > node.depth:
                node.depth = self.level + 1

        # If False examples need further explaining,
        # create right node and add to the queue.
        if len(bestFExamples) > 0:

            self.right = node(
                test=None,
                examples=bestFExamples,
                information=data.variance(bestFExamples),
                level=self.level + 1,
                parent=self,
                pos="right",
            )

            if self.level + 1 > node.depth:
                node.depth = self.level + 1

        # If there are no examples, append clause as it is.
        # if no examples append clause as is
        if self.test == "" or round(self.information, 3) == 0:
            if clause[-1] != "-":
                node.learnedDecisionTree.append(clause[:-1])
            else:
                node.learnedDecisionTree.append(clause)
            return
