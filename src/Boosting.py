"""
Copyright (C) 2017-2018 RFGB Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program (at the base of this repository). If not,
see <http://www.gnu.org/licenses/>
"""

from Utils import Utils
from math import log,exp
from Logic import Prover
from copy import deepcopy
class Boosting(object):
    '''boosting class'''
    
    logPrior = log(0.5/float(1-0.5))

    @staticmethod
    def computeAdviceGradient(example):
        '''computes the advice gradients as nt-nf'''
        nt,nf = 0,0
        target = Utils.data.target.split('(')[0]
        for clause in Utils.data.adviceClauses:
            if Prover.prove(Utils.data,example,clause):
                if target in Utils.data.adviceClauses[clause]['preferred']:
                    nt += 1
                if target in Utils.data.adviceClauses[clause]['nonPreferred']:
                    nf += 1
        return (nt-nf)

    @staticmethod
    def inferTreeValue(clauses,query,data):
        '''returns probability of query
           given data and clauses learned
        '''
        for clause in clauses: #for every clause in the tree
            clauseCopy = deepcopy(clause)
            clauseValue = float(clauseCopy.split(" ")[1])
            clauseRule = clauseCopy.split(" ")[0].replace(";",",")
            if not clauseRule.split(":-")[1]:
                return clauseValue
            if Prover.prove(data,query,clauseRule): #check if query satisfies clause
                return clauseValue
    
    @staticmethod
    def computeSumOfGradients(example,trees,data):
        '''computes new gradient for example'''
        sumOfGradients = 0
        for tree in trees: #add leaf values satisfied by example in each tree
            gradient = Boosting.inferTreeValue(tree,example,data)
            sumOfGradients += gradient
        return sumOfGradients #return the sum

    @staticmethod
    def updateGradients(data,trees,loss="LS",delta=None):
        '''updates the gradients of the data'''
        if not data.regression:
            logPrior = Boosting.logPrior
            #P = sigmoid of sum of gradients given by each tree learned so far
            for example in data.pos: #for each positive example compute 1 - P
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,data)
                probabilityOfExample = Utils.sigmoid(logPrior+sumOfGradients)
                updatedGradient = 1 - probabilityOfExample
                if data.advice:
                    adviceGradient = Boosting.computeAdviceGradient(example)
                    updatedGradient += adviceGradient
                data.pos[example] = updatedGradient
            for example in data.neg: #for each negative example compute 0 - P
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,data)
                probabilityOfExample = Utils.sigmoid(logPrior+sumOfGradients)
                updatedGradient = 0 - probabilityOfExample
                if data.advice:
                    adviceGradient = Boosting.computeAdviceGradient(example)
                    updatedGradient += adviceGradient
                data.neg[example] = updatedGradient
        if data.regression:
            for example in data.examples: #compute gradient as y-y_hat
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,data)
                trueValue = data.getExampleTrueValue(example)
                exampleValue = sumOfGradients
                if loss == "LS":
                    updatedGradient = trueValue - exampleValue
                    data.examples[example] = updatedGradient
                elif loss == "LAD":
                    updatedGradient = 0
                    gradient = trueValue - exampleValue
                    if gradient:
                        updatedGradient = gradient/float(abs(gradient))
                    data.examples[example] = updatedGradient
                elif loss == "Huber":
                    gradient = trueValue - exampleValue
                    updatedGradient = 0
                    if gradient:
                        if gradient > float(delta):
                            updatedGradient = gradient/float(abs(gradient))
                        elif gradient <= float(delta):
                            updatedGradient = gradient
                    data.examples[example] = updatedGradient

    @staticmethod
    def performInference(testData,trees):
        '''computes probability for test examples'''
        logPrior = Boosting.logPrior
        if not testData.regression:
            logPrior = log(0.5/float(1-0.5)) #initialize log odds of assumed prior probability for example
            for example in testData.pos:
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,testData) #compute sum of gradients
                testData.pos[example] = Utils.sigmoid(logPrior+sumOfGradients) #calculate probability as sigmoid(log odds)
            for example in testData.neg:
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,testData) #compute sum of gradients
                testData.neg[example] = Utils.sigmoid(logPrior+sumOfGradients) #calculate probability as sigmoid(log odds)
        elif testData.regression:
            for example in testData.examples:
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,testData)
                testData.examples[example] = sumOfGradients
