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
(docstring for utils)
"""

from random import sample
from math import exp

import codecs
import json
import string


class Data(object):
    """Object containing the relational data."""

    def __init__(
        self, regression=False, advice=False, softm=False, alpha=0.0, beta=0.0
    ):
        """
        An RFGB Data object, which serves as the structure for the positives,
        negatives, facts, and other parameters.

        adviceClauses: dictionary of advice clauses.
        facts: list of strings representing facts.
        pos: dictionary of positive examples.
        neg: dictionary of negative examples.
        examples: dictionary of examples for regression.
        examplesTrueValue: true value for use during regression.
        target: Target(s) to be learned or inferred.
        literals: Literals present in facts or their type specifications.
        variableType: Type of variable for facts and target.
        """

        self.regression = regression
        self.advice = advice
        self.adviceClauses = {}
        self.facts = []
        self.pos = {}
        self.neg = {}
        self.examples = {}
        self.examplesTrueValue = {}
        self.target = None
        self.literals = []
        self.literalTypes = {}
        self.variableType = {}

        self.softm = softm
        self.alpha = alpha
        self.beta = beta

    def setFacts(self, facts):
        """
        Mutate the facts in the data object.

        :param facts: List of strings representing the facts.
        :type facts: list.

        :returns: None
        """
        self.facts = facts

    def getFacts(self):
        """returns the facts in the data"""
        return self.facts

    def setPos(self, pos, target):
        """
        Set positive examples based on the contents of a list.
        """
        for example in pos:
            if example.split("(")[0] == target:
                # Set initial gradient to 0.5 for positives.
                self.pos[example] = 1 - Utils.sigmoid(-1.8)

    def setExamples(self, examples, target):
        """
        Set examples for regression.
        """
        for example in examples:
            # Get the predicate.
            predicate = example.split(" ")[0]
            # Get the true regression value.
            value = float(example.split(" ")[1])
            if predicate.split("(")[0] == target:
                # Store the true value in examplesTrueValue dictionary.
                self.examplesTrueValue[predicate] = value
                # Set the value, otherwise none.
                self.examples[predicate] = value

    def setNeg(self, neg, target):
        """
        Set negative examples based on the contents of a list.
        """
        for example in neg:
            if example.split("(")[0] == target:
                # Set initial gradient to -0.5 for negative examples.
                self.neg[example] = -Utils.sigmoid(-1.8)

    def setTarget(self, bk, target):
        """
        Sets self.target as a target string.
        Sets self.variableType

        :param bk: List of strings representing modes.
        :type bk: list.

        :param target: Target relation or attribute.
        :type target: str.

        :returns: None

        Example:

        .. code-block:: python

                        from rfgb.utils import Data

                        data = Data(regression=False)
                        background = ['friends(+person,-person)',
                                      'friends(-person,+person)',
                                      'smokes(+person)',
                                      'cancer(-person)']
                        target = 'cancer'

                        data.setTarget(background, target)

                        print(data.target)
                        # 'cancer(C)'
        """
        # targetTypes are the types of variables in the target predicate.
        targetTypes = [i[:-1].split("(")[1].split(",") for i in bk if target in i][0]
        targetTypes = list(map(Utils.removeModeSymbols, targetTypes))

        targetArity = len(targetTypes)
        targetVariables = sample(Utils.UniqueVariableCollection, targetArity)

        self.target = target + "("
        for variable in targetVariables:
            self.target += variable + ","
            self.variableType[variable] = targetTypes[targetVariables.index(variable)]
        self.target = self.target[:-1] + ")"

    def getTarget(self):
        """
        Returns the target.
        """
        return self.target

    def getExampleTrueValue(self, example):
        """
        Returns true regression value of an example for regression learning.
        """
        return self.examplesTrueValue[example]

    def getValue(self, example):
        """
        Returns the regression value for an example.

        Example:

        .. code-block:: python

                        from rfgb.utils import Utils
                        from rfgb.utils import Data

                        trainingData = Utils.readTrainingData('cancer',
                                            path='testDomain/ToyCancer/train/')

                        x = trainingData.getValue('cancer(earl)')
                        # x == -0.5, since earl doesn't have cancer.

                        y = trainingData.getValue('cancer(alice)')
                        # y == 0.5, since alice does have cancer
        """
        if self.regression:
            return self.examples[example]

        if example in self.pos:
            return self.pos[example]
        else:
            return self.neg[example]

    def setBackground(self, bk):
        """
        Obtains the literals and their type specifications. Types can be
        either variable or a list of constants.
        """

        bkWithoutTargets = [line for line in bk if "+" in line or "-" in line]

        # For every literal, obtain name and type specifications.
        for literalBk in bkWithoutTargets:
            literalName = literalBk.split("(")[0]
            literalTypeSpecification = literalBk[:-1].split("(")[1].split(",")
            self.literalTypes[literalName] = literalTypeSpecification
            self.literals.append([literalName, literalTypeSpecification])

    def getLiterals(self):
        """gets all the literals in the facts"""
        return self.literals

    def variance(self, examples):
        """
        Calculates the variance of the regression values from a subset of the
        data.
        """

        if not examples:
            return 0

        total = sum([self.getValue(example) for example in examples])
        numberOfExamples = len(examples)
        mean = total / float(numberOfExamples)
        sumOfSquaredError = sum(
            [(self.getValue(example) - mean) ** 2 for example in examples]
        )

        return sumOfSquaredError / float(numberOfExamples)  # return variance


class Utils(object):
    """
    Class of utilities used by rfgb, such as reading files, removing mode
    symbols, calculating Cartesian Products, etc.
    """

    # Attribute to store data (facts, positves, negatives)
    data = None
    UniqueVariableCollection = set(list(string.ascii_uppercase))

    @staticmethod
    def sigmoid(x):
        """
        :param x: Number to apply sigmoid to.
        :type x: int or float

        :returns: ``exp(x)/float(1+exp(x))``
        :rtype: float
        """
        return exp(x) / float(1 + exp(x))

    @staticmethod
    def removeModeSymbols(inputString):
        """
        Returns a string with the mode symbols (+,-,#) removed.

        Example:

        .. code-block:: python

                        from rfgb.utils import Utils

                        removeModeSymbols('#city')
                        # == 'city'

                        i = ['+drinks', '-drink', '-city']
                        o = list(map(removeModeSymbols, i))
                        # o == ['drinks', 'drink', 'city']
        """
        return inputString.replace("+", "").replace("-", "").replace("#", "")

    @staticmethod
    def addVariableTypes(literal):
        """
        As literals are encountered, update Utils.data.variableType with the
        type of the variables encountered.

        :param literal: A literal of the form smokes(W) or friends(A,B)
        :type literal: str.
        """

        # Get the name of the literal.
        literalName = literal.split("(")[0]

        # Get background info for the literal
        literalTypeSpecification = Utils.data.literalTypes[literalName]

        # Get the arguments
        literalArguments = literal[:-1].split("(")[1].split(",")

        # Get the number of arguments.
        for i in range(len(literalArguments)):
            if literalTypeSpecification[i][0] != "[":
                variable = literalArguments[i]
                if variable not in Utils.data.variableType.keys():
                    Utils.data.variableType[variable] = literalTypeSpecification[i][1:]

    @staticmethod
    def getleafValue(examples):
        """returns average of regression values for examples"""
        if not examples:
            return 0
        total = 0
        for example in examples:
            total += Utils.data.getValue(example)
        return total / float(len(examples))

    @staticmethod
    def save(location, saveItem):
        """
        Dumps json version of learnedDecisionTree to location.

        :param location: Name of the file to write.
        :type location: str.

        :returns: None.
        """
        with codecs.open(location, encoding="utf-8", mode="w") as f:
            json.dump(saveItem, f, indent=2)

    @staticmethod
    def load(location):
        """
        Loads json version of learnedDecisionTree from location.

        :param location: Name of the file to load.
        :type location: str.

        :returns: None.
        """
        with codecs.open(location, encoding="utf-8", mode="r") as f:
            return json.load(f)

    @staticmethod
    def readTrainingData(
        target,
        path="train/",
        regression=False,
        advice=False,
        softm=False,
        alpha=0.0,
        beta=0.0,
    ):
        """
        Reads the training data from files.

        :param target: The target predicate.
        :type target: str.

        :param path: Path to the training data.
        :type path: str.

        :param regression: Read from ``examples.txt`` instead of ``pos.txt``
                           and ``neg.txt``.
        :type regression: bool

        :param advice: Read advice from an advice file, which should be
                       contained in the same directory as the examples.
        :type advice: bool

        :default path: 'train/'
        :default regression: False
        :default advice: False

        :returns: A Data object representing the training data.
        :rtype: :py:class:`.utils.Data`
        """

        Utils.data = Data(
            regression=regression, advice=advice, softm=softm, alpha=alpha, beta=beta
        )
        # trainData = Data(regression=regression, advice=advice)
        # Utils.data.regression = regression
        # Utils.data.advice = advice

        if advice:
            with open(path + "advice.txt") as fp:  # read advice from train folder
                adviceFileLines = fp.read().splitlines()

                for line in adviceFileLines:
                    adviceClause = line.split(" ")[0]  # get advice clause

                    Utils.data.adviceClauses[adviceClause] = {}
                    # trainData.adviceClauses[adviceClause] = {}

                    preferredTargets = line.split(" ")[1][1:-1].split(",")
                    if preferredTargets[0]:
                        Utils.data.adviceClauses[adviceClause][
                            "preferred"
                        ] = preferredTargets
                        # trainData.adviceClauses[adviceClause]['preferred'] = preferredTargets
                    elif not preferredTargets[0]:
                        Utils.data.adviceClauses[adviceClause]["preferred"] = []
                        # trainData.adviceClauses[adviceClause]['preferred'] = []

                    nonPreferredTargets = line.split(" ")[2][1:-1].split(",")
                    if nonPreferredTargets[0]:
                        Utils.data.adviceClauses[adviceClause][
                            "nonPreferred"
                        ] = nonPreferredTargets
                        # trainData.adviceClauses[adviceClause]['nonPreferred'] = nonPreferredTargets
                    elif not nonPreferredTargets[0]:
                        Utils.data.adviceClauses[adviceClause]["nonPreferred"] = []
                        # trainData.adviceClauses[adviceClause]['nonPreferred'] = []

        with open(path + "facts.txt") as fac:
            Utils.data.setFacts(fac.read().splitlines())
            # trainData.setFacts(fac.read().splitlines())

        if regression:
            with open(path + "examples.txt") as exam:
                Utils.data.setExamples(exam.read().splitlines(), target)
                # trainData.setExamples(exam.read().splitlines(), target)
        else:
            with open(path + "pos.txt") as pos:
                Utils.data.setPos(pos.read().splitlines(), target)
                # trainData.setPos(pos.read().splitlines(), target)
            with open(path + "neg.txt") as neg:
                Utils.data.setNeg(neg.read().splitlines(), target)
                # trainData.setNeg(neg.read().splitlines(), target)

        with open(path + "bk.txt") as fp:
            bk = fp.read().splitlines()

            Utils.data.setBackground(bk)
            Utils.data.setTarget(bk, target)
            # trainData.setBackground(bk)
            # trainData.setTarget(bk, target, regression=regression)

        return Utils.data
        # return trainData

    @staticmethod
    def readTestData(target, path="test/", regression=False):
        """
        Reads the testing data from files.

        :param target: The target predicate.
        :type target: str.

        :param path: Path to the training data.
        :type path: str.

        :param regression: Read from ``examples.txt`` instead of ``pos.txt``
                           and ``neg.txt``.
        :type regression: bool

        :default path: 'train/'
        :default regression: False

        :returns: A Data object representing the training data.
        :rtype: :py:class:`.utils.Data`
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
        """
        Returns the Cartesian Product of all sets contained in the item sets.
        """

        # Create new input where each element is in its own set.
        modifiedItemSets = []
        for itemSet in itemSets:
            modifiedItemSet = []
            for element in itemSet:
                modifiedItemSet.append([element])
            modifiedItemSets.append(modifiedItemSet)

        # Perform Cartesian Product of the first two sets.
        while len(modifiedItemSets) > 1:
            set1 = modifiedItemSets[0]
            set2 = modifiedItemSets[1]
            pairWiseProducts = []
            for item1 in set1:
                for item2 in set2:
                    # Cartesian Product performed here.
                    pairWiseProducts.append(item1 + item2)

            # Remove the first two sets.
            modifiedItemSets.remove(set1)
            modifiedItemSets.remove(set2)
            # Insert the Cartesian Product in their place and repeat.
            modifiedItemSets.insert(0, pairWiseProducts)

        # Return the final Cartesian Product Sets
        return modifiedItemSets[0]
