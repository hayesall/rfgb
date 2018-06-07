
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

from random import sample
from math import exp

import string

class Data(object):
    '''contains the relational data'''

    def __init__(self, regression=False, advice=False):
        """
        An RFGB Data object, which serves as the structure for the positives,
        negatives, facts, and other parameters.
        """

        self.regression = regression
        self.advice = advice
        self.adviceClauses = {} #advice clauses stored here
        self.facts = [] #facts
        self.pos = {} #positive examples
        self.neg = {} #negative examples
        self.examples = {} #for regression
        self.examplesTrueValue = {} #for regression
        self.target = None #target to be learned
        self.literals = {} #literals present in facts and their type specs
        self.variableType = {} #type of variable used for facts and target

    def setFacts(self, facts):
        """
        Mutate the facts in the data object.

        @method Data.setFacts
        @param  {list}          facts
        @return {}              None
        """
        self.facts = facts

    def getFacts(self):
        '''returns the facts in the data'''
        return self.facts

    def setPos(self,pos,target):
        '''set positive examples from pos list'''
        for example in pos:
            if example.split('(')[0] == target:
                self.pos[example] = 0.5 #set initial gradient to 1-0.5 for positive

    def setExamples(self,examples,target):
        '''set examples for regression'''
        for example in examples:
            predicate = example.split(' ')[0] #get predicate
            value = float(example.split(' ')[1]) # get true regression value
            if predicate.split('(')[0] == target:
                self.examplesTrueValue[predicate] = value #store true value of example
                self.examples[predicate] = value #set value for example, otherwise no variance

    def setNeg(self,neg,target):
        '''set negative examples from neg list'''
        for example in neg:
            if example.split('(')[0] == target:
                self.neg[example] = -0.5 #set initial gradient to 0-0.5 for negative

    def setTarget(self, bk, target):
        """
        Sets self.target as a target string.
        Sets self.variableType

        @method Data.setTarget
        @param  {list}          bk          List of strings representing modes.
        @param  {str}           target      Target relation or attribute.
        @return {}              (None)

        Example:

        >>> data = Data(regression=False)
        >>> background = ['friends(+person,-person)', friends(-person,+person),
                          'smokes(+person)', 'cancer(+person)']
        >>> target = 'cancer'
        >>> data.setTarget(background, target)
        >>> print(data.target)
        'cancer(C)'

        """
        # targetTypes are the types of variables in the target predicate.
        targetTypes = [i[:-1].split('(')[1].split(',') for i in bk if target in i][0]
        targetTypes = list(map(Utils.removeModeSymbols, targetTypes))

        targetArity = len(targetTypes)
        targetVariables = sample(Utils.UniqueVariableCollection, targetArity)

        self.target = target + '('
        for variable in targetVariables:
            self.target += variable + ','
            self.variableType[variable] = targetTypes[targetVariables.index(variable)]
        self.target = self.target[:-1] + ')'

    def getTarget(self):
        '''returns the target'''
        return self.target

    def getExampleTrueValue(self,example):
        '''returns true regression value of example during regression'''
        return self.examplesTrueValue[example]

    def getValue(self, example):
        """
        Returns the regression value for an example.

        Example:

        >>> trainingData = Utils.readTrainingData('cancer', path='testDomains/ToyCancer/train/')
        >>> x = trainingData.getValue('cancer(watson)')
        >>> x
        -0.5
        """
        if self.regression:
            return self.examples[example]

        if example in self.pos:
            return self.pos[example]
        else:
            return self.neg[example]

    def setBackground(self,bk):
        '''obtains the literals and their type specifications
           types can be variable or a list of constants
        '''
        bkWithoutTargets = [line for line in bk if '+' in line or '-' in line]
        for literalBk in bkWithoutTargets: #for every literal obtain name and type specification
            literalName = literalBk.split('(')[0]
            literalTypeSpecification = literalBk[:-1].split('(')[1].split(',')
            self.literals[literalName] = literalTypeSpecification

    def getLiterals(self):
        '''gets all the literals in the facts'''
        return self.literals

    def variance(self, examples):
        '''
        Calculates the variance of the regression values from a subset of the data.
        '''
        #print(examples)

        if not examples:
            return 0

        total = sum([self.getValue(example) for example in examples])
        numberOfExamples = len(examples)
        mean = total/float(numberOfExamples)
        sumOfSquaredError = sum([(self.getValue(example) - mean)**2 for example in examples])

        return sumOfSquaredError/float(numberOfExamples) #return variance

class Utils(object):
    '''class for utilities used by program
       reading files
    '''

    """@batflyer

    'string' module can cause compatability issues between Python 2 and Python 3,
    switched from using string.uppercase to using string.ascii_uppsercase,
    the latter should work with both versions.
    """

    data = None #attribute to store data (facts,positive and negative examples)
    UniqueVariableCollection = set(list(string.ascii_uppercase))

    @staticmethod
    def sigmoid(x):
        '''returns sigmoid of x'''
        return exp(x)/float(1+exp(x))

    @staticmethod
    def removeModeSymbols(inputString):
        """
        Returns a string with the mode symbols (+,-,#) removed.

        Example:
            >>> i = "#city"
            >>> o = removeModeSymbols(i)
            >>> print(o)
            city

            >>> i = ["+drinks", "-drink", "-city"]
            >>> o = list(map(removeModeSymbols, i))
            >>> print(o)
            ["drinks", "drink", "city"]
        """
        return inputString.replace('+', '').replace('-', '').replace('#', '')

    @staticmethod
    def addVariableTypes(literal):
        '''adds type of variables contained in literal'''
        literalName = literal.split('(')[0] #get literal name
        literalTypeSpecification = Utils.data.literals[literalName] #get background info
        literalArguments = literal[:-1].split('(')[1].split(',') #get arguments
        numberOfArguments = len(literalArguments)
        for i in range(numberOfArguments):
            if literalTypeSpecification[i][0]!='[':
                variable = literalArguments[i]
                if variable not in Utils.data.variableType.keys():
                    Utils.data.variableType[variable] = literalTypeSpecification[i][1:]

    @staticmethod
    def getleafValue(examples):
        '''returns average of regression values for examples'''
        if not examples:
            return 0
        total = 0
        for example in examples:
            total += Utils.data.getValue(example)
        return total/float(len(examples))

    @staticmethod
    def readTrainingData(target, path='train/', regression=False, advice=False):

        """
        Reads the training data from files.

        Required Arguments:
            target: the target predicate.

        Optional Arguments:
            path: (default: 'train/')
                The path to the testing data.
            regression: (default: False)
                If regression is true, reads from 'examples.txt' instead of
                'pos.txt' and 'neg.txt'
            advice: (default: False)
                If advice is true, reads from an advice file, which should
                be contained in the same directory as 'pos.txt' and 'neg.txt'

        Returns:
            A Data object representing the train data.
        """

        Utils.data = Data(regression=regression, advice=advice)
        #trainData = Data(regression=regression, advice=advice)
        #Utils.data.regression = regression
        #Utils.data.advice = advice

        if advice:
            with open(path + "advice.txt") as fp: #read advice from train folder
                adviceFileLines = fp.read().splitlines()

                for line in adviceFileLines:
                    adviceClause = line.split(' ')[0] #get advice clause

                    Utils.data.adviceClauses[adviceClause] = {}
                    #trainData.adviceClauses[adviceClause] = {}

                    preferredTargets = line.split(' ')[1][1:-1].split(',')
                    if preferredTargets[0]:
                        Utils.data.adviceClauses[adviceClause]['preferred'] = preferredTargets
                        #trainData.adviceClauses[adviceClause]['preferred'] = preferredTargets
                    elif not preferredTargets[0]:
                        Utils.data.adviceClauses[adviceClause]['preferred'] = []
                        #trainData.adviceClauses[adviceClause]['preferred'] = []

                    nonPreferredTargets = line.split(' ')[2][1:-1].split(',')
                    if nonPreferredTargets[0]:
                        Utils.data.adviceClauses[adviceClause]['nonPreferred'] = nonPreferredTargets
                        #trainData.adviceClauses[adviceClause]['nonPreferred'] = nonPreferredTargets
                    elif not nonPreferredTargets[0]:
                        Utils.data.adviceClauses[adviceClause]['nonPreferred'] = []
                        #trainData.adviceClauses[adviceClause]['nonPreferred'] = []

        with open(path + "facts.txt") as fac:
            Utils.data.setFacts(fac.read().splitlines())
            #trainData.setFacts(fac.read().splitlines())

        if regression:
            with open(path + "examples.txt") as exam:
                Utils.data.setExamples(exam.read().splitlines(), target)
                #trainData.setExamples(exam.read().splitlines(), target)
        else:
            with open(path + "pos.txt") as pos:
                Utils.data.setPos(pos.read().splitlines(), target)
                #trainData.setPos(pos.read().splitlines(), target)
            with open(path + "neg.txt") as neg:
                Utils.data.setNeg(neg.read().splitlines(), target)
                #trainData.setNeg(neg.read().splitlines(), target)

        with open(path + "bk.txt") as fp:
            bk = fp.read().splitlines()

            Utils.data.setBackground(bk)
            Utils.data.setTarget(bk, target)
            #trainData.setBackground(bk)
            #trainData.setTarget(bk, target, regression=regression)

        return Utils.data
        #return trainData

    @staticmethod
    def readTestData(target, path='test/', regression=False):

        """
        Reads the testing data from files.

        Required Arguments:
            target: the target predicate.

        Optional Arguments:
            path: (default: 'test/')
                The path to the testing data.
            regression: (default: False)
                If regression is true, reads from 'examples.txt' instead of
                'pos.txt' and 'neg.txt'

        Returns:
            A Data object representing the test data.
        """

        testData = Data()
        testData.regression = regression

        with open(path + "facts.txt") as facts:
            testData.setFacts(facts.read().splitlines())

        if regression:
            with open(path + "examples.txt") as exam:
                examples = exam.read().splitlines()
                testData.setExamples(examples, target)
        else:
            # If we are not using regression, read from pos.txt and neg.txt
            with open(path + "pos.txt") as pos:
                testData.setPos(pos.read().splitlines(), target)
            with open(path + "neg.txt") as neg:
                testData.setNeg(neg.read().splitlines(), target)

        return testData


    @staticmethod
    def cartesianProduct(itemSets):
        '''returns cartesian product of all the sets
           contained in the item sets
        '''
        modifiedItemSets = [] #have to create new input where each single element is in its own set
        for itemSet in itemSets:
            modifiedItemSet = []
            for element in itemSet:
                modifiedItemSet.append([element]) #does the above task
            modifiedItemSets.append(modifiedItemSet)
        while len(modifiedItemSets) > 1: #perform cartesian product of first 2 sets
            set1 = modifiedItemSets[0]
            set2 = modifiedItemSets[1]
            pairWiseProducts = []
            for item1 in set1:
                for item2 in set2:
                    pairWiseProducts.append(item1+item2) #cartesian product performed here
            modifiedItemSets.remove(set1) #remove first 2 sets
            modifiedItemSets.remove(set2)
            modifiedItemSets.insert(0,pairWiseProducts) #insert cartesian product in its place and repeat
        return modifiedItemSets[0] #return the final cartesian product sets
