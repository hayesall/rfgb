from Utils import Utils
from math import log,exp
from Logic import Prover
from copy import deepcopy
class Boosting(object):
    '''boosting class'''

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
    def updateGradients(data,trees):
        '''updates the gradients of the data'''
        #P = sigmoid of sum of gradients given by each tree learned so far
        for example in data.pos: #for each positive example compute 1 - P
            sumOfGradients = Boosting.computeSumOfGradients(example,trees,data)
            probabilityOfExample = Utils.sigmoid(sumOfGradients)
            updatedGradient = 1 - probabilityOfExample
            data.pos[example] = updatedGradient
        for example in data.neg: #for each negative example compute 0 - P
            sumOfGradients = Boosting.computeSumOfGradients(example,trees,data)
            probabilityOfExample = Utils.sigmoid(sumOfGradients)
            updatedGradient = 0 - probabilityOfExample
            data.neg[example] = updatedGradient

    @staticmethod
    def performInference(testData,trees):
        '''computes probability for test examples'''
        logPrior = log(0.5/float(1-0.5)) #initialize log odds of assumed prior probability for example
        for example in testData.pos:
            sumOfGradients = Boosting.computeSumOfGradients(example,trees,testData) #compute sum of gradients
            testData.pos[example] = Utils.sigmoid(logPrior+sumOfGradients) #calculate probability as sigmoid(log odds)
        for example in testData.neg:
            sumOfGradients = Boosting.computeSumOfGradients(example,trees,testData) #compute sum of gradients
            testData.neg[example] = Utils.sigmoid(logPrior+sumOfGradients) #calculate probability as sigmoid(log odds)
