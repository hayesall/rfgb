import itertools,re
from Utils import Utils
from copy import deepcopy

#Thanks to Chris Meyers for some of this code --> http://www.openbookproject.net/py4fun/prolog/prolog1.html.

class Term(object):
    '''class for term in prolog proof'''
    def __init__ (self, s) :   # expect "x(y,z...)"
        if s[-1] != ')' : fatal("Syntax error in term: %s" % [s])
        flds = s.split('(')
        if len(flds) != 2 : fatal("Syntax error in term: %s" % [s])
        self.args = flds[1][:-1].split(',')
        self.pred = flds[0]

class Rule(object):
    '''class for logic rules in prolog proof'''
    def __init__ (self, s) :   # expect "term-:term;term;..."
        flds = s.split(":-")
        self.head = Term(flds[0])
        self.goals = []
        if len(flds) == 2 :
            flds = re.sub("\),",");",flds[1]).split(";")
            for fld in flds : self.goals.append(Term(fld))

class Goal(object):
    '''class for each goal in rule during prolog search'''
    def __init__ (self, rule, parent=None, env={}) :
        goalId = Prover.goalId
        goalId += 1
        self.id = goalId
        self.rule = rule
        self.parent = parent
        self.env = deepcopy(env)
        self.inx = 0      # start search with 1st subgoal

class Prover(object):
    '''class for prolog style proof of query'''
    rules = []
    goalId = 100
    trace = 0

    @staticmethod
    def unify (srcTerm, srcEnv, destTerm, destEnv) :
        "unification method"
        nargs = len(srcTerm.args)
        if nargs        != len(destTerm.args) : return 0
        if srcTerm.pred != destTerm.pred      : return 0
        for i in range(nargs) :
            srcArg  = srcTerm.args[i]
            destArg = destTerm.args[i]
            if srcArg <= 'Z' : srcVal = srcEnv.get(srcArg)
            else             : srcVal = srcArg
            if srcVal :    # constant or defined Variable in source
                if destArg <= 'Z' :  # Variable in destination
                    destVal = destEnv.get(destArg)
                    if not destVal : destEnv[destArg] = srcVal  # Unify !
                    elif destVal != srcVal : return 0           # Won't unify
                elif     destArg != srcVal : return 0           # Won't unify
        return 1

    @staticmethod
    def search (term) :
        '''method to perform prolog style query search'''
        goalId = Prover.goalId
        trace = Prover.trace
        rules = Prover.rules
        unify = Prover.unify
        goalId = 0
        returnValue = False
        if trace : print "search", term
        goal = Goal(Rule("got(goal):-x(y)"))      # Anything- just get a rule object
        goal.rule.goals = [term]                  # target is the single goal
        if trace : print "stack", goal
        stack = [goal]                            # Start our search
        while stack :
            c = stack.pop()        # Next goal to consider
            if trace : print "  pop", c
            if c.inx >= len(c.rule.goals) :       # Is this one finished?
                if c.parent == None :             # Yes. Our original goal?
                    if c.env : print  c.env       # Yes. tell user we
                    else     : returnValue = True #print "Yes"        # have a solution
                    continue
                parent = deepcopy(c.parent)  # Otherwise resume parent goal
                unify (c.rule.head,c.env,parent.rule.goals[parent.inx],parent.env)
                parent.inx = parent.inx+1         # advance to next goal in body
                if trace : print "stack", parent
                stack.append(parent)              # let it wait its turn
                continue
            # No. more to do with this goal.
            term = c.rule.goals[c.inx]            # What we want to solve
            for rule in rules :                     # Walk down the rule database
                if rule.head.pred      != term.pred      : continue
                if len(rule.head.args) != len(term.args) : continue
                child = Goal(rule, c)               # A possible subgoal
                ans = unify (term, c.env, rule.head, child.env)
                if ans :                            # if unifies, stack it up
                    if trace : print "stack", child
                    stack.append(child)
        return returnValue

    @staticmethod
    def prove(data,example,clause):
        '''proves if example satisfies clause given the data
           returns True if satisfies else returns False
        '''
        Prover.rules = [] #contains all rules
        Prover.trace = 0  #if trace is 1 displays proof tree
        Prover.goalId = 100 #stores goal Id
        Prover.rules += [Rule(fact) for fact in data.getFacts()]
        Prover.rules += [Rule(clause)]
        proofOutcome = Prover.search(Term(example)) #proves query prolog style
        return proofOutcome

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
        variablesAndConstants = literal[:-1].split('(')[1].split(',') #get variables and constants in body literal
        variables = [item for item in variablesAndConstants if item in Utils.UniqueVariableCollection] #get only the variables
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
            bodyLiterals = [literal for literal in body.split(";") if literal] #get clause body literals
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
        allowedVariables = list(set(bodyVariables+targetVariables+freeVariables)) #allowed variables is combination of free and target variables
        permutations = [list(item) for item in list(itertools.permutations(allowedVariables,numberOfVariables))] #get all permutations of size number of variables
        specifications = [] #list of all possible type specifications including constants if any
        if Logic.constantsPresentInLiteral(literalTypeSpecification): #check if constants present
            cartesianProductInput = [[item] if item == "var" else item[1:-1].split(';') for item in literalTypeSpecification] 
            cartesianProduct = Utils.cartesianProduct(cartesianProductInput) #perform cartesian product of variable specifications with each of the constants
            for itemSet in cartesianProduct: #set the cartesian product as specifications
                specifications.append(itemSet)
        else:
            specifications.append(literalTypeSpecification) #if no constants then the current specification is enough
        literalCandidates = [] #initialize list that will hold all candidate test literals
        for specification in specifications: #for each specification,
            for permutation in permutations: #from each permutation of allowed variables,
                permutationCopy = deepcopy(permutation)
                specificationCopy = deepcopy(specification)
                specificationLength = len(specification)
                while permutationCopy:
                    for i in range(specificationLength):
                        specificationType = specificationCopy[i]
                        if specificationType == "var":
                            variable = permutationCopy.pop() #substitute an allowed variable where type is "var"
                            specificationCopy[i] = variable
                    literalCandidate = literalName+"("+ ",".join(specificationCopy)+")" #create predicate with name,variables and constants
                    literalCandidates.append(literalCandidate) #add to all possible test candidates
        return literalCandidates #return all test candidates for proving
