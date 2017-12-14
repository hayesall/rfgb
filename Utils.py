import string
from random import sample
class Data(object):
    '''contains the relational data'''

    def __init__(self):
        '''constructor for the Data class'''
        self.facts = [] #facts
        self.pos = {} #positive examples
        self.neg = {} #negative examples
        self.target = None #target to be learned

    def setFacts(self,facts):
        '''set facts from facts list'''
        self.facts = facts

    def setPos(self,pos):
        '''set positive examples from pos list'''
        for example in pos:
            self.pos[example] = 0.5 #set initial gradient to 1-0.5 for positive

    def setNeg(self,neg):
        '''set negative examples from neg list'''
        for example in neg:
            self.neg[example] = -0.5 #set initial gradient to 0-0.5 for negative

    def setTarget(self):
        '''sets the target'''
        firstPositiveInstance = self.pos.keys()[0] #get the first positive example in the dictionary
        targetPredicate = firstPositiveInstance.split('(')[0] #get predicate name
        targetArity = len(firstPositiveInstance.split('(')[1].split(',')) #get predicate arity
        targetVariables = sample(Utils.UniqueVariableCollection,targetArity) #get some variables according to arity
        self.target = targetPredicate+"(" #construct target string
        for variable in targetVariables:
            self.target += variable+","
        self.target = self.target[:-1]+")"

    def getTarget(self):
        '''returns the target'''
        return self.target

    def getValue(self,example):
        '''returns regression value for example'''
        for ex in self.pos: #check first among positive examples and return value
            if ex == example:
                return self.pos[example]
        for ex in self.neg: #check next among negative examples and return values
            if ex == example:
                return self.neg[example]
        
class Utils(object):
    '''class for utilities used by program
       reading files
    '''
    data = None #attribute to store data (facts,positive and negative examples)
    UniqueVariableCollection = set(list(string.uppercase))
    @staticmethod
    def readTrainingData():
        '''reads the training data from files'''
        Utils.data = Data() #create object to hold data for each tree
        with open("train/facts.txt") as fp: #read facts from train folder
            facts = fp.read().splitlines()
            Utils.data.setFacts(facts)
        with open("train/pos.txt") as fp: #read positive examples from train folder
            pos = fp.read().splitlines()
            Utils.data.setPos(pos)
        with open("train/neg.txt") as fp: #read negative examples from train folder
            neg = fp.read().splitlines()
            Utils.data.setNeg(neg)
        Utils.data.setTarget()
        return Utils.data

    @staticmethod
    def variance(examples):
        '''method to calculate variance
           in regression values for all
           examples
        '''
        total = 0 #initialize total regression value 
        for example in examples:
            total += Utils.data.getValue(example) #cimpute total
        numberOfExamples = len(examples) #get number of examples
        mean = total/float(numberOfExamples) #calc mean as total/number
        sumOfSquaredError = 0 #initialize sum of squared errors
        for example in examples: #calculate total squared difference from mean
            sumOfSquaredError += (Utils.data.getValue(example)-mean)**2
        return sumOfSquaredError/float(numberOfExamples) #return variance
            
