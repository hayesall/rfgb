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

        allowedVariables = [] #initialize allowed variables
        while len(allowedVariables) < numberOfVariables:
            for variable in Utils.UniqueVariableCollection:
                if variable in targetVariables and variable not in allowedVariables:
                    allowedVariables.append(variable)
                    break
