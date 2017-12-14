import itertools
from Utils import Utils
from copy import deepcopy

class Logic(object):
    '''class for logic operations'''

    @staticmethod
    def constantsPresentInLiteral(literalTypeSpecification):
        '''returns true if constants present in type spec'''
        for item in literalTypeSpecification: #check if there is a single non variable
            if item != "var":
                return True
        return False

    @staticmethod
    def getVariables(literal):
        '''returns variables in the literal'''
        variablesAndConstants = literal.split[:-1].split('(')[1].split(',') #get variables and constants in body literal
        variables = [item for item in variableAndConstants if item in Utils.UniqueVariableCollection] #get only the variables
        return variables

    @staticmethod
    def generateTests(literalName,literalTypeSpecification,clause):
        '''generates tests with at least one variable in common
           with the target predicate
        '''
        target = clause.split(":-")[0] #get clause target
        body = clause.split(":-")[1] #get clause body
        bodyVariables = [] #initialize body variables list
        if body:
            bodyLiterals = body.split(",") #get clause body literals
            for literal in bodyLiterals:
                bodyVariables += Logic.getVariables(literal)
        numberOfVariables = 0 #initialize number of variables to 0
        for specification in literalTypeSpecification: #get number of variables of literal to be added
            if specification == "var":
                numberOfVariables += 1
        targetVariables = [] #initialize target variable list
        targetVariables = target[:-1].split('(')[1].split(',') #obtain target variables
        maxNumberOfFreeVariables = numberOfVariables-1 #get max number of free variables that literal can have
        allowedVariables = [] #initialize variables allowed in the literal to be added
        freeVariables = [variable for variable in Utils.UniqueVariableCollection if variable not in targetVariables][:maxNumberOfFreeVariables] #variables not in target
        allowedVariables = bodyVariables+targetVariables+freeVariables #allowed variables is combination of free and target variables
        permutations = [list(item) for item in list(itertools.permutations(allowedVariables,numberOfVariables))] #get all permutations of size number of variables
        specifications = [] #list of all possible type specifications including constants if any
        if Logic.constantsPresentInLiteral(literalTypeSpecification):
            cartesianProductInput = [[item] if item == "var" else item[1:-1].split(';') for item in literalTypeSpecification]
            cartesianProduct = Utils.cartesianProduct(cartesianProductInput)
            for itemSet in cartesianProduct:
                specifications.append(itemSet)
        else:
            specifications.append(literalTypeSpecification)
        literalCandidates = []
        for specification in specifications:
            for permutation in permutations:
                permutationCopy = deepcopy(permutation)
                specificationCopy = deepcopy(specification)
                specificationLength = len(specification)
                while permutationCopy:
                    for i in range(specificationLength):
                        specificationType = specificationCopy[i]
                        if specificationType == "var":
                            variable = permutationCopy.pop()
                            specificationCopy[i] = variable
                    literalCandidate = literalName+"("+ ",".join(specificationCopy)+")"
                    literalCandidates.append(literalCandidate)
        return literalCandidates
