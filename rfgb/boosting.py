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
Core methods for performing learning and inference, such as computing
gradients, updating gradients, and performing inference.

Documentation
-------------
"""

from __future__ import division

from .utils import Utils
from .logic import Prover

from math import log
from math import exp
from copy import deepcopy

_log_prior = -1.8


def computeAdviceGradient(example):
    """
    Proves each clause (:meth:`.Prover.prove`) and computes the advice gradient
    as ``NumberTrue - NumberFalse``.

    :param example:
    :type example:
    """

    nt, nf = 0, 0
    target = Utils.data.target.split("(")[0]
    for clause in Utils.data.adviceClauses:
        if Prover.prove(Utils.data, example, clause):
            if target in Utils.data.adviceClauses[clause]["preferred"]:
                nt += 1
            if target in Utils.data.adviceClauses[clause]["nonPreferred"]:
                nf += 1
    return nt - nf


def computeSumOfGradients(example, trees, data):
    """
    Computes new gradients for an example.

    :param example:
    :type example:

    :param trees:
    :type trees:

    :param data:
    :type data:
    """

    sumOfGradients = 0

    # Add leaf values satisfied by example in each tree.
    for tree in trees:
        gradient = inferTreeValue(tree, example, data)
        sumOfGradients += gradient
    return sumOfGradients


def inferTreeValue(clauses, query, data):
    """
    Returns the probability of `query` given data and the clauses learned.

    :param clauses:
    :type clauses:

    :param query:
    :type query:

    :param data:
    :type data:
    """
    for clause in clauses:

        clauseCopy = deepcopy(clause)
        clauseValue = float(clauseCopy.split(" ")[1])
        clauseRule = clauseCopy.split(" ")[0].replace(";", ",")

        if not clauseRule.split(":-")[1]:
            return clauseValue
        if Prover.prove(data, query, clauseRule):
            # Check if query satisifes clause
            return clauseValue


def performInference(testData, trees):
    """
    Computes the probabilities for test examples.

    :param testData: Data for testing.
    :type testData: :py:class:`.utils.Data` object.

    :param trees: List of strings representing learned decision trees.
    :type trees: list.

    Example:

    .. code-block:: python

                    from rfgb.boosting import performInference

    """

    logPrior = _log_prior
    if not testData.regression:

        # Initialize log odds of assumed prior probability for example.

        for example in testData.pos:

            # Compute sum of gradients
            sumOfGradients = computeSumOfGradients(example, trees, testData)

            # Calculate probability as sigmoid(log odds)
            testData.pos[example] = Utils.sigmoid(logPrior + sumOfGradients)

        for example in testData.neg:

            # Compute sum of gradients
            sumOfGradients = computeSumOfGradients(example, trees, testData)

            # Calculate probability as sigmoid(log odds)
            testData.neg[example] = Utils.sigmoid(logPrior + sumOfGradients)

    elif testData.regression:
        logPrior = 0.0
        for example in testData.examples:
            sumOfGradients = computeSumOfGradients(example, trees, testData)
            testData.examples[example] = sumOfGradients


def updateGradients(data, trees, loss="LS", delta=None):
    """
    Update gradients of the data.

    :param data: Training or testing data (with parameters).
    :type data: :py:class:`.utils.Data` object.

    :param trees: List of strings representing trees.
    :type trees: list.

    :param loss: Loss function for regression (currently implemented:
                 'LS', 'LAD', 'Huber').
    :type loss: str.

    :param delta: Delta value for Huber loss.
    :type delta: float

    Example:

    .. code-block:: python

                    from rfgb.boosting import updateGradients

    """

    if data.regression:
        # If this is regression data, compute gradient as y - y_hat

        for example in data.examples:
            sumOfGradients = computeSumOfGradients(example, trees, data)
            trueValue = data.getExampleTrueValue(example)

            if loss == "LS":
                # Least Squares
                data.examples[example] = trueValue - sumOfGradients

            elif loss == "LAD":
                # Least Absolute Deviation
                updatedGradient = 0
                gradient = trueValue - sumOfGradients
                if gradient:
                    updatedGradient = gradient / float(abs(gradient))
                data.examples[example] = updatedGradient

            elif loss == "Huber":
                # Huber Loss
                gradient = trueValue - sumOfGradients
                updatedGradient = 0
                if gradient:
                    if gradient > float(delta):
                        updatedGradient = gradient / float(abs(gradient))
                    elif gradient <= float(delta):
                        updatedGradient = gradient
                data.examples[example] = updatedGradient

    else:
        # If this is classification data, compute 1 - P for each positive.
        """

        logPrior = __logPrior__

        # P = sigmoid(sum of gradients) given by each tree learned so far.

        for example in data.pos:
            # For each positive example compute 1 - P
            sumOfGradients = computeSumOfGradients(example, trees, data)
            prob = Utils.sigmoid(logPrior + sumOfGradients)
            updatedGradient = 1 - prob
            if data.advice:
                adviceGradient = computeAdviceGradient(example)
                updatedGradient += adviceGradient
            data.pos[example] = updatedGradient

        for example in data.neg:
            # For each negative example compute 0 - P
            sumOfGradients = computeSumOfGradients(example, trees, data)
            prob = Utils.sigmoid(logPrior + sumOfGradients)
            updatedGradient = 0 - prob
            if data.advice:
                adviceGradient = computeAdviceGradient(example)
                updatedGradient += adviceGradient
            data.neg[example] = updatedGradient

        """

        logPrior = _log_prior

        if data.softm:

            for example in data.pos:

                sumOfGradients = computeSumOfGradients(example, trees, data)
                prob = Utils.sigmoid(logPrior + sumOfGradients)
                updatedGradient = 1 - prob / (prob + (1 - prob) * exp(data.alpha))
                data.pos[example] = updatedGradient

            for example in data.neg:

                sumOfGradients = computeSumOfGradients(example, trees, data)
                prob = Utils.sigmoid(logPrior + sumOfGradients)
                updatedGradient = 1 - prob / (prob + (1 - prob) * exp(-data.beta))
                data.neg[example] = updatedGradient

        else:

            for example in data.pos:

                sumOfGradients = computeSumOfGradients(example, trees, data)
                prob = Utils.sigmoid(logPrior + sumOfGradients)
                updatedGradient = 1 - prob

                if data.advice:
                    updatedGradient += computeAdviceGradient(example)

                data.pos[example] = updatedGradient

            for example in data.neg:

                sumOfGradients = computeSumOfGradients(example, trees, data)
                prob = Utils.sigmoid(logPrior + sumOfGradients)
                updatedGradient = 0 - prob

                if data.advice:
                    updatedGradient += computeAdviceGradient(example)

                data.neg[example] = updatedGradient
