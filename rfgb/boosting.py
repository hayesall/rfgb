
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
rfgb.boosting.py
================

Provides
--------

    1. Core methods for performing learning and inference.

Documentation
-------------

"""

from __future__ import division

from .utils import Utils
from .logic import Prover

from math import log
from math import exp
from copy import deepcopy

__logPrior__ = log(0.5/float(1-0.5))

"""
class Boosting(object):
    '''boosting class'''

    # Wouldn't `logPrior = 0.0` be easier?
    logPrior = log(0.5/float(1-0.5))
"""

def computeAdviceGradient(example):
    """
    Name:
        rfgb.Boosting.computeAdviceGradient
    Performs:
        Computes the advice gradients as 'NumberTrue - NumberFalse'.
    """

    nt, nf = 0, 0
    target = Utils.data.target.split('(')[0]
    for clause in Utils.data.adviceClauses:
        if Prover.prove(Utils.data, example, clause):
            if target in Utils.data.adviceClauses[clause]['preferred']:
                nt += 1
            if target in Utils.data.adviceClauses[clause]['nonPreferred']:
                nf += 1
    return (nt-nf)

def inferTreeValue(clauses, query, data):
    """
    Name:
        rfgb.Boosting.inferTreeValue
    Performs:
        Returns the probability of query given data and clauses learned.
    """
    for clause in clauses:
        clauseCopy = deepcopy(clause)
        clauseValue = float(clauseCopy.split(" ")[1])
        clauseRule = clauseCopy.split(" ")[0].replace(";",",")
        if not clauseRule.split(":-")[1]:
            return clauseValue
        if Prover.prove(data,query,clauseRule): #check if query satisfies clause
            return clauseValue

def computeSumOfGradients(example, trees, data):
    """
    Overview:
    ---------
    Name:
        rfgb.Boosting.computeSumOfGradients
    Performs:
        Computes new gradients for an example.

    ==========================================================================
    Positional arguments:
    ---------------------

    @param  {str}
    @param  {list}
    @param  {object}
    """

    sumOfGradients = 0

    # Add leaf values satisfied by example in each tree.
    for tree in trees:
        gradient = inferTreeValue(tree, example, data)
        sumOfGradients += gradient
    return sumOfGradients


def updateGradients(data, trees, loss='LS', delta=None):
    """
    Overview:
    ---------

    Name:
        rfgb.Boosting.updateGradients
    Performs:
        Updates the gradients of the data.

    ==========================================================================
    Positional arguments:
    ---------------------

    @param  {object}        data            rfgb data object for training or
                                            testing data (and parameters).
    @param  {list}          trees           List of strings representing trees.

    ==========================================================================
    Keyword arguments:
    ------------------

    @param  {str}           loss            Loss function for regression.
                                            allowed: ['LS', 'LAD', 'Huber']
    @param  {float}         delta           Delta value for Huber loss.

    ==========================================================================
    Examples:
    ---------

    >>> from rfgb.Boosting import updateGradients
    """

    if data.regression:
        # If this is regression data, compute gradient as y - y_hat

        for example in data.examples:
            sumOfGradients = computeSumOfGradients(example,trees,data)
            trueValue = data.getExampleTrueValue(example)

            if loss == "LS":
                # Least Squares
                data.examples[example] = trueValue - sumOfGradients

            elif loss == "LAD":
                # Least Absolute Deviation
                updatedGradient = 0
                gradient = trueValue - sumOfGradients
                if gradient:
                    updatedGradient = gradient/float(abs(gradient))
                data.examples[example] = updatedGradient

            elif loss == "Huber":
                # Huber Loss
                gradient = trueValue - sumOfGradients
                updatedGradient = 0
                if gradient:
                    if gradient > float(delta):
                        updatedGradient = gradient/float(abs(gradient))
                    elif gradient <= float(delta):
                        updatedGradient = gradient
                data.examples[example] = updatedGradient

    else:
        # If this is classification data, compute 1 - P for each positive.
        """
        logPrior = __logPrior__

        for example in data.pos:
            sumOfGradients = computeSumOfGradients(example, trees, data)
        """

        logPrior = __logPrior__
        #P = sigmoid of sum of gradients given by each tree learned so far
        for example in data.pos: #for each positive example compute 1 - P
            sumOfGradients = computeSumOfGradients(example,trees,data)
            probabilityOfExample = Utils.sigmoid(logPrior+sumOfGradients)
            updatedGradient = 1 - probabilityOfExample
            if data.advice:
                adviceGradient = computeAdviceGradient(example)
                updatedGradient += adviceGradient
            data.pos[example] = updatedGradient
        for example in data.neg: #for each negative example compute 0 - P
            sumOfGradients = computeSumOfGradients(example,trees,data)
            probabilityOfExample = Utils.sigmoid(logPrior+sumOfGradients)
            updatedGradient = 0 - probabilityOfExample
            if data.advice:
                adviceGradient = computeAdviceGradient(example)
                updatedGradient += adviceGradient
            data.neg[example] = updatedGradient

def performInference(testData, trees):
    """
    Overview:
    ---------
    Name:
        rfgb.Boosting.performInference
    Performs:
        Computes the probabilities for test examples.

    ==========================================================================
    Positional arguments:
    ---------------------

    @param  {object}            testData        Data object for testing.
    @param  {list}              trees           List of strings representing
                                                learned decision trees.

    ==========================================================================
    Examples:
    ---------

    >>> from rfgb.Boosting import performInference
    """

    logPrior = __logPrior__
    if not testData.regression:
        logPrior = log(0.5/float(1-0.5)) #initialize log odds of assumed prior probability for example
        for example in testData.pos:
            sumOfGradients = computeSumOfGradients(example,trees,testData) #compute sum of gradients
            testData.pos[example] = Utils.sigmoid(logPrior+sumOfGradients) #calculate probability as sigmoid(log odds)
        for example in testData.neg:
            sumOfGradients = computeSumOfGradients(example,trees,testData) #compute sum of gradients
            testData.neg[example] = Utils.sigmoid(logPrior+sumOfGradients) #calculate probability as sigmoid(log odds)
    elif testData.regression:
        for example in testData.examples:
            sumOfGradients = computeSumOfGradients(example,trees,testData)
            testData.examples[example] = sumOfGradients
