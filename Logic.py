from __future__ import print_function

import itertools,re
from Utils import Utils
from copy import deepcopy
from random import sample

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
        if trace : print("search", term)
        goal = Goal(Rule("got(goal):-x(y)"))      # Anything- just get a rule object
        goal.rule.goals = [term]                  # target is the single goal
        if trace : print("stack", goal)
        stack = [goal]                            # Start our search
        while stack :
            c = stack.pop()        # Next goal to consider
            if trace : print("  pop", c)
            if c.inx >= len(c.rule.goals) :       # Is this one finished?
                if c.parent == None :             # Yes. Our original goal?
                    if c.env : print(c.env)       # Yes. tell user we
                    else     : returnValue = True #print "Yes"        # have a solution
                    continue
                parent = deepcopy(c.parent)  # Otherwise resume parent goal
                unify (c.rule.head,c.env,parent.rule.goals[parent.inx],parent.env)
                parent.inx = parent.inx+1         # advance to next goal in body
                if trace : print("stack", parent)
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
                    if trace : print("stack", child)
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
            if item[0] == '[':
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
        '''generates tests for literal according to modes and types'''
        target = clause.split(":-")[0] #get clause target
        body = clause.split(":-")[1] #get clause body
        targetVariables = target[:-1].split('(')[1].split(',') #obtain target variables
        bodyVariables = [] #initialize body variables list
        if body:
            bodyLiterals = [literal for literal in body.split(";") if literal] #get clause body literals
            for literal in bodyLiterals:
                bodyVariables += Logic.getVariables(literal)
        clauseVariables = set(targetVariables+bodyVariables) #get all clause variables
        lengthOfSpecification = len(literalTypeSpecification) #get length of specification
        testSpecification = []
        for i in range(lengthOfSpecification):
            variable = False #check if data type is variable or constant
            if literalTypeSpecification[i][0]!='[':
                variable = True
            if variable: #if data type is variable
                mode = literalTypeSpecification[i][0] #get mode + or -
                variableType = literalTypeSpecification[i][1:] #get variable type
                if mode == '+': #variable must be an already existing variable in the clause of same type if exists
                    variableOfSameTypeInClause = [var for var in clauseVariables if Utils.data.variableType[var]==variableType] #get all clause variables of same type
                    if variableOfSameTypeInClause: #if variables of same type exist in clause
                        testSpecification.append(variableOfSameTypeInClause)
                    else:
                        newVar = None
                        while True:
                            newVar = sample(Utils.UniqueVariableCollection,1)
                            if newVar[0] not in clauseVariables:
                                break
                        testSpecification.append([newVar[0]])
                if mode == '-': #use new variable
                    newVar = None
                    while True:
                        newVar = sample(Utils.UniqueVariableCollection,1)
                        if newVar[0] not in clauseVariables:
                            break
                    testSpecification.append([newVar[0]])
            else: #if data type is constant
                listToAppend = literalTypeSpecification[i][1:-1].split(';')
                testSpecification.append(listToAppend)
        testVariablesAndConstants =  Utils.cartesianProduct(testSpecification)
        literalCandidates = []
        for item in testVariablesAndConstants: #form predicates and return all the test candidates for this literal
            literalCandidate = literalName+"("+",".join(item)+")"
            literalCandidates.append(literalCandidate)
        return literalCandidates
