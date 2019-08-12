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


from __future__ import print_function
from __future__ import absolute_import
from ...logic import Term
from ...logic import Rule
from ...logic import Logic

import unittest


class TermTest(unittest.TestCase):
    """
    Tests for rfgb.logic.Term
    """

    def test_initialize_term_0(self):
        term = Term("()")
        self.assertEqual(term.pred, "")
        self.assertEqual(term.args, [""])

    def test_initialize_term_1(self):
        term = Term("person(batflyer)")
        self.assertEqual(term.pred, "person")
        self.assertEqual(term.args, ["batflyer"])

    def test_initialize_term_2(self):
        term = Term("drinks(person,beer)")
        self.assertEqual(term.pred, "drinks")
        self.assertEqual(term.args, ["person", "beer"])

    def test_initialize_term_3(self):
        term = Term("drinks(person,beer,pub)")
        self.assertEqual(term.pred, "drinks")
        self.assertEqual(term.args, ["person", "beer", "pub"])

    def test_initialize_term_4(self):
        term = Term("drinks(person, beer, pub)")
        self.assertEqual(term.pred, "drinks")
        self.assertEqual(term.args, ["person", "beer", "pub"])

    def test_initialize_bad_term_1(self):
        # Exception should be raised on account of the last item in the string
        # not being a ')'
        with self.assertRaises(Exception):
            term = Term(")(")

    def test_initialize_bad_term_2(self):
        # Exception should be raised due to the syntax error at the end.
        with self.assertRaises(Exception):
            term = Term("hello(world).")

    def test_initialize_bad_term_3(self):
        # Similar reason to previous.
        with self.assertRaises(Exception):
            term = Term("drinks(person, pub).")

    def test_initialize_bad_term_4(self):
        # Terms should be composed of two fields split on a '('
        with self.assertRaises(Exception):
            term = Term("x)")


class RuleTest(unittest.TestCase):
    """
    Tests for rfgb.logic.Rule
    """

    def test_initialize_rule_0(self):
        rule = Rule("smokes(x):-cancer(x)")
        self.assertEqual(rule.head.pred, "smokes")
        self.assertEqual(rule.head.args, ["x"])
        self.assertEqual(rule.goals[0].pred, "cancer")
        self.assertEqual(rule.goals[0].args, ["x"])

    def test_initialize_rule_1(self):
        rule = Rule("advises(x,y):-paper(x,y)")
        self.assertEqual(rule.head.pred, "advises")
        self.assertEqual(rule.head.args, ["x", "y"])
        self.assertEqual(rule.goals[0].pred, "paper")
        self.assertEqual(rule.goals[0].args, ["x", "y"])

    def test_initialize_rule_2(self):
        rule = Rule("advises(x,y):-paper(x,y);student(y)")
        self.assertEqual(rule.head.pred, "advises")
        self.assertEqual(rule.head.args, ["x", "y"])
        self.assertEqual(rule.goals[0].pred, "paper")
        self.assertEqual(rule.goals[0].args, ["x", "y"])
        self.assertEqual(rule.goals[1].pred, "student")
        self.assertEqual(rule.goals[1].args, ["y"])

    def test_initialize_bad_rule_1(self):
        with self.assertRaises(Exception):
            rule = Rule("")

    def test_initialize_bad_rule_2(self):
        with self.assertRaises(Exception):
            rule = Rule("advises(x,y):!-paper(v)")
