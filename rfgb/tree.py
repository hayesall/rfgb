
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
(docstring)
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from .utils import Utils
from .logic import Logic
from .logic import Prover

from copy import deepcopy

class node(object):
    '''this is a node in a tree'''
    expandQueue = [] #Breadth first search node expansion strategy
    depth = 0 #initial depth is 0 because no node present
    maxDepth = 1 #max depth set to 1 because we want to at least learn a tree of depth 1
    learnedDecisionTree = [] #this will hold all the clauses learned
    data = None #stores all the facts, positive and negative examples

    @staticmethod
    def setMaxDepth(depth):
        '''method to set max depth'''
        node.maxDepth = depth

    def __init__(self, test=None, examples=None, information=None, level=None, parent=None, pos=None):
        '''constructor for node class
           contains test condition or clause
           contains examples
           contains information notion (some score)
           contains level in the tree of node
           contains parent node pointer
           and contains position in the tree
        '''
        self.test = test #set test condition, which will be a horn clause
        if level > 0: #check if root
            self.parent = parent #if not root set parent as the nodes parent
        else:
            self.parent = "root" #if root, set parent to "root" to signify root
        self.pos = pos #position of the node, i.e. "left" or "right"
        self.examples = examples #all examples that are available for testing at this node
        self.information = information #information contained at this node
        self.level = level #level of the node, 0 for root
        self.left = None #left subtree
        self.right = None #right subtree
        node.expandQueue.insert(0,self) #add to the queue of nodes to expand

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

    def getTrueExamples(self, clause, test, data):
        '''returns all examples that satisfy clause
           with conjoined test literal
        '''
        tExamples = [] #intialize list of true examples
        clauseCopy = deepcopy(clause)
        if clauseCopy[-1] == "-": #construct clause for prover
            clauseCopy += test
        elif clauseCopy[-1] == ';':
            clauseCopy = clauseCopy.replace(';', ',') + test
        print ("testing clause: ",clauseCopy) # --> to keep track of output, following for loop can be parallelized
        for example in self.examples:
            if Prover.prove(data,example,clauseCopy): #prove if example satisfies clause
                tExamples.append(example)
        return tExamples

    def expandOnBestTest(self, data=None):
        '''expands the node based on the best test'''
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
        if self.parent!="root":
                tests = [test for test in tests if not test in ancestorTests]
        tests = set(tests)

        # Check which test scores the best.
        for test in tests:
            # Examples which are satisfied.
            tExamples = self.getTrueExamples(clause, test, data)
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

        print("best test found at current node: ",self.test)


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
