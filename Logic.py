import itertools
from Utils import Utils
class Logic(object):
    '''class for logic operations'''

    @staticmethod
    def generateTests(literalName,literalTypeSpecification,target):
        '''generates tests with at least one variable in common
           with the target predicate
        '''
        numberOfVariables = 0 #initialize number of variables to 0
        for specification in literalTypeSpecification:
            if specification == "var":
                numberOfVariables += 1
        targetVariables = [] #initialize target variable list
        targetVariables = target[:-1].split('(')[1].split(',') #obtain target variables
        maxNumberOfFreeVariables = numberOfVariables-1 #get max number of free variables that literal can have
        allowedVariables = [] #initialize variables allowed in the literal to be added
        freeVariables = [variable for variable in Utils.UniqueVariableCollection if variable not in targetVariables][:maxNumberOfFreeVariables] #variables not in target
        allowedVariables = targetVariables+freeVariables #allowed variables is combination of free and target variables
        permutations = list(itertools.permutations(allowedVariables,numberOfVariables)) #get all permutations of size number of variables
        print target
        print literalName
        print literalTypeSpecification
        print permutations
        exit()
        
        
