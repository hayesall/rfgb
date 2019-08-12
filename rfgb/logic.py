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
(docstring)
"""

from __future__ import print_function

from copy import deepcopy
from random import sample
import itertools
import re

from .utils import Utils

# Thanks to Chris Meyers for some of this code:
# http://www.openbookproject.net/py4fun/prolog/prolog1.html.


class Term(object):
    """
    Class for term in prolog proof.
    """

    # Expect "x(y,z...)"
    def __init__(self, s):
        if s[-1] != ")":
            raise (Exception("Term should end with ')': %s" % [s]))
        flds = s.split("(")
        if len(flds) != 2:
            raise (Exception("Term should be composed of two fields: %s" % [s]))
        self.args = flds[1][:-1].replace(" ", "").split(",")
        self.pred = flds[0]


class Rule(object):
    """
    Class for logic rules in prolog proof.
    """

    # Expect "term:-term;term;..."
    def __init__(self, s):
        flds = s.split(":-")
        self.head = Term(flds[0])
        self.goals = []
        if len(flds) == 2:
            flds = re.sub("\),", ");", flds[1]).split(";")
            for fld in flds:
                self.goals.append(Term(fld))


class Goal(object):
    """class for each goal in rule during prolog search"""

    def __init__(self, rule, parent=None, env={}):
        goalId = Prover.goalId
        goalId += 1
        self.id = goalId
        self.rule = rule
        self.parent = parent
        self.env = deepcopy(env)
        # Start search with 1st subgoal
        self.inx = 0


class Prover(object):
    """class for prolog style proof of query"""

    rules = []
    goalId = 100
    trace = 0

    @staticmethod
    def unify(srcTerm, srcEnv, destTerm, destEnv):
        """
        Unification method.
        """
        nargs = len(srcTerm.args)
        if nargs != len(destTerm.args):
            return 0
        if srcTerm.pred != destTerm.pred:
            return 0
        for i in range(nargs):
            srcArg = srcTerm.args[i]
            destArg = destTerm.args[i]
            if srcArg <= "Z":
                srcVal = srcEnv.get(srcArg)
            else:
                srcVal = srcArg
            if srcVal:
                # Constant or defined Variable in source
                if destArg <= "Z":
                    # Variable in destination
                    destVal = destEnv.get(destArg)
                    if not destVal:
                        # Unify
                        destEnv[destArg] = srcVal
                    elif destVal != srcVal:
                        # Won't unify
                        return 0
                elif destArg != srcVal:
                    # Won't unify
                    return 0
        return 1

    @staticmethod
    def search(term):
        """
        Method to perform prolog style query search.
        """
        goalId = Prover.goalId
        trace = Prover.trace
        rules = Prover.rules
        unify = Prover.unify
        goalId = 0
        returnValue = False
        if trace:
            print("search", term)

        # Anything- just get a rule object.
        goal = Goal(Rule("got(goal):-x(y)"))
        # Target is the single goal
        goal.rule.goals = [term]
        if trace:
            print("stack", goal)

        # Begin the search.
        stack = [goal]
        while stack:
            # Next goal to consider:
            c = stack.pop()
            if trace:
                print("  pop", c)

            # Is this one finished?
            if c.inx >= len(c.rule.goals):
                # Yes. Our original goal?
                if c.parent is None:
                    if c.env:
                        # Yes. tell user we
                        print(c.env)
                    else:
                        # have a solution
                        returnValue = True
                    continue

                # Otherwise, resume parent goal.
                parent = deepcopy(c.parent)

                unify(c.rule.head, c.env, parent.rule.goals[parent.inx], parent.env)

                # Advance to next goal in body.
                parent.inx = parent.inx + 1
                if trace:
                    print("stack", parent)
                # Let it wait its turn.
                stack.append(parent)
                continue

            # No. more to do with this goal.
            # What we want to solve:
            term = c.rule.goals[c.inx]
            for rule in rules:
                # Walk down the rule database.
                if rule.head.pred != term.pred:
                    continue
                if len(rule.head.args) != len(term.args):
                    continue
                # A possible subgoal.
                child = Goal(rule, c)
                ans = unify(term, c.env, rule.head, child.env)
                if ans:
                    # if unifies, stack it up
                    if trace:
                        print("stack", child)
                    stack.append(child)
        return returnValue

    @staticmethod
    def prove(data, example, clause):
        """
        Proves if example satisfies clause given the data.
        Returns True if it satisfies, else return False.

        Prover.rules: contains all of the rules.
        Prover.trace: If this is 1, displays the proof tree.
        Prover.goalID: stores the goal ID.
        """
        Prover.rules = []
        Prover.trace = 0
        Prover.goalId = 100
        Prover.rules += [Rule(fact) for fact in data.getFacts()]
        Prover.rules += [Rule(clause)]

        # Proves query prolog-style:
        proofOutcome = Prover.search(Term(example))
        return proofOutcome


class Logic(object):
    """
    Class for logic operations.
    """

    @staticmethod
    def constantsPresentInLiteral(literalTypeSpecification):
        """
        Returns true if constants present in type specification.
        """
        # Check if there is a single non-variable.
        for item in literalTypeSpecification:
            if item[0] == "[":
                return True
        return False

    @staticmethod
    def getVariables(literal):
        """
        Returns variables in the literal.
        """
        # Get variables and constants in body literal.
        variablesAndConstants = literal[:-1].split("(")[1].split(",")

        # Get only the variables.
        variables = []
        for item in variablesAndConstants:
            if item in Utils.UniqueVariableCollection:
                variables.append(item)

        return variables

    @staticmethod
    def generateTests(literalName, literalTypeSpecification, clause):
        """
        Generates tests for literal according to modes and types.
        """

        target = clause.split(":-")[0]
        body = clause.split(":-")[1]
        targetVariables = target[:-1].split("(")[1].split(",")

        # Initialize a list of body variables.
        bodyVariables = []
        if body:
            # Get clause body literals
            bodyLiterals = [literal for literal in body.split(";") if literal]
            for literal in bodyLiterals:
                bodyVariables += Logic.getVariables(literal)

        clauseVariables = set(targetVariables + bodyVariables)
        lengthOfSpecification = len(literalTypeSpecification)

        testSpecification = []
        for i in range(lengthOfSpecification):
            # Check if data type is variable or constant.
            variable = False
            if literalTypeSpecification[i][0] != "[":
                variable = True
            # If the data type is variable.
            if variable:
                # Get mode (+ or -)
                mode = literalTypeSpecification[i][0]
                # Get the variable type.
                variableType = literalTypeSpecification[i][1:]

                # Variable must be an already existing variable in the clause
                # of the same type if it exists.
                if mode == "+":
                    # Get all clause variables of same type:

                    variableOfSameTypeInClause = []
                    for var in clauseVariables:
                        if Utils.data.variableType[var] == variableType:
                            variableOfSameTypeInClause.append(var)

                    if variableOfSameTypeInClause:
                        # If variables of same type exist in clause
                        testSpecification.append(variableOfSameTypeInClause)
                    else:
                        newVar = None
                        while True:
                            newVar = sample(Utils.UniqueVariableCollection, 1)
                            if newVar[0] not in clauseVariables:
                                break
                        testSpecification.append([newVar[0]])

                # Use new variable.
                if mode == "-":
                    newVar = None
                    while True:
                        newVar = sample(Utils.UniqueVariableCollection, 1)
                        if newVar[0] not in clauseVariables:
                            break
                    testSpecification.append([newVar[0]])

            # If data type is constant:
            else:
                listToAppend = literalTypeSpecification[i][1:-1].split(";")
                testSpecification.append(listToAppend)

        testVariablesAndConstants = Utils.cartesianProduct(testSpecification)
        literalCandidates = []

        # Form predicates and return all the test candidates for this literal
        for item in testVariablesAndConstants:
            literalCandidate = literalName + "(" + ",".join(item) + ")"
            literalCandidates.append(literalCandidate)
        return literalCandidates
