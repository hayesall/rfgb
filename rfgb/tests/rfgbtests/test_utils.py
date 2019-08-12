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
Unit tests for Utils.py

Tests should be ordered in the same manner as they are defined in Utils.py
"""

from __future__ import absolute_import
from ...utils import Data
from ...utils import Utils
import unittest


class UtilsTest(unittest.TestCase):
    def test_sigmoid(self):
        """
        tests: sigmoid function.
        """
        self.assertEqual(Utils.sigmoid(-5), 0.006692850924284856)
        self.assertEqual(Utils.sigmoid(-0.001), 0.49975000002083336)
        self.assertEqual(Utils.sigmoid(0), 0.5)
        self.assertEqual(Utils.sigmoid(0.0001), 0.5000249999999792)
        self.assertEqual(Utils.sigmoid(0.01), 0.5024999791668749)
        self.assertEqual(Utils.sigmoid(0.5), 0.6224593312018546)
        self.assertEqual(Utils.sigmoid(1), 0.7310585786300049)
        self.assertEqual(Utils.sigmoid(5), 0.9933071490757152)

    def test_removeModeSymbols(self):
        """
        tests: removeModeSymbols function.
        """
        self.assertEqual(Utils.removeModeSymbols("+drinks"), "drinks")
        self.assertEqual(Utils.removeModeSymbols("-drinks"), "drinks")
        self.assertEqual(Utils.removeModeSymbols("#drinks"), "drinks")

    def test_setTarget_1(self):
        """
        tests: Data.setTarget (attribute case).
        """

        # Some setup that needs to take place.

        target = "cancer"
        background = [
            "friends(+person,-person)",
            "friends(-person,+person)",
            "smokes(+person)",
            "cancer(person)",
        ]

        # setTarget has some random behavior, but always returns the target
        # bound to a letter.
        for _ in range(100):
            # Set the target (introducing a random variable).
            data = Data(regression=False)
            data.setBackground(background)
            data.setTarget(background, target)

            # Assert the presence of the target.
            self.assertTrue(target in data.target)

            # Get the random variable.
            instance = data.target.split("(")[1][0]

            # Assert that the random variable belongs to the
            # UniqueVariableCollection.
            self.assertTrue(instance in Utils.UniqueVariableCollection)

    def test_setTarget_2(self):
        """
        tests: Data.setTarget (relation case).
        """

        # Some setup that needs to take place.
        target = "friends"
        background = [
            "friends(+person,-person)",
            "friends(-person,+person)",
            "smokes(+person)",
            "cancer(person)",
        ]

        for _ in range(100):
            # Set the target (introducing two random variables).
            data = Data(regression=False)
            data.setBackground(background)
            data.setTarget(background, target)

            # Assert the presence of the target.
            self.assertTrue(target in data.target)

            # Get the two random variables.
            instance = data.target.split("(")[1].split(")")[0].split(",")

            # Assert arity of friendship is 2, and that variables belong to
            # UniqueVariableCollection.
            self.assertEqual(len(instance), 2)
            self.assertTrue(instance[0] in Utils.UniqueVariableCollection)
            self.assertTrue(instance[1] in Utils.UniqueVariableCollection)

    def test_setTarget_3(self):
        """
        tests: Data.setTarget (3-arity case).
        """

        target = "drinks"
        background = ["drinks(+person,-drink,-city)"]

        for _ in range(100):
            # Set the target (introducing three random variables).
            data = Data(regression=False)
            data.setBackground(background)
            data.setPos(
                ["drinks(Jeremy,Wine,Paris)", "drinks(Ulrich,Beer,Frankfurt)"], target
            )
            data.setTarget(background, target)

            # Assert the presence of the target.
            self.assertTrue(target in data.target)

            # Get the three random variables.
            instance = data.target.split("(")[1].split(")")[0].split(",")

            # Assert arity of drinks is 3, variables are not duplicated, and
            # belong to UniqueVariableCollection.
            self.assertEqual(len(instance), 3)
            self.assertTrue(instance[0] in Utils.UniqueVariableCollection)
            self.assertTrue(instance[1] in Utils.UniqueVariableCollection)
            self.assertTrue(instance[2] in Utils.UniqueVariableCollection)

    def test_read_test_data_toy_cancer(self):
        """
        tests: readTestData on the ToyCancer dataset.
        """
        sampleData = Utils.readTestData("cancer", path="testDomains/ToyCancer/test/")

        # Verify that regression and advice were not specified.
        self.assertEqual(sampleData.regression, False)
        self.assertEqual(sampleData.advice, False)

        # sampleData.facts should return a list of strings.
        self.assertEqual(
            sampleData.facts,
            [
                "friends(zod,xena)",
                "friends(xena,watson)",
                "friends(watson,voldemort)",
                "friends(voldemort,yoda)",
                "friends(yoda,zod)",
                "friends(xena,zod)",
                "friends(watson,xena)",
                "friends(voldemort,watson)",
                "friends(yoda,voldemort)",
                "friends(zod,yoda)",
                "smokes(zod)",
                "smokes(xena)",
                "smokes(yoda)",
            ],
        )

        # sampleData.pos should return a dictionary with the
        # initial gradients set to 0.5
        self.assertEqual(
            sampleData.pos,
            {
                "cancer(zod)": 0.8581489350995122,
                "cancer(xena)": 0.8581489350995122,
                "cancer(yoda)": 0.8581489350995122,
            },
        )
        # sampleData.neg should return a dictionary with the
        # initial gradients set to -0.5
        self.assertEqual(
            sampleData.neg,
            {
                "cancer(voldemort)": -0.1418510649004878,
                "cancer(watson)": -0.1418510649004878,
            },
        )

        # sampleData.literals should be an empty dictionary.
        self.assertEqual(sampleData.literals, [])

        # Test some of the Data object functions, they should not
        # mutate contents.
        self.assertEqual(sampleData.facts, sampleData.getFacts())
        self.assertEqual(sampleData.literals, sampleData.getLiterals())

    def test_read_test_data_boston_housing(self):
        """
        tests: readTestData on the BostonHousing dataset.
        """
        sampleData = Utils.readTestData(
            "medv", path="testDomains/BostonHousing/test/", regression=True
        )

        # Verify that regression was specified but advice was not.
        self.assertEqual(sampleData.regression, True)
        self.assertEqual(sampleData.advice, False)

        # sampleData.facts should return a list of strings
        with open("testDomains/BostonHousing/test/facts.txt") as f:
            bostonHousingFacts = f.read().splitlines()
        self.assertEqual(sampleData.facts, bostonHousingFacts)

        # sampleData.examples should return a dictionary where the first
        # item is the predicate and the second item is the regression value.
        with open("testDomains/BostonHousing/test/examples.txt") as f:
            bostonHousingExamples = f.read().splitlines()

        for e in bostonHousingExamples:
            ePred, eVal = e.split()
            self.assertTrue(ePred in sampleData.examples)
            self.assertTrue(float(eVal) in list(sampleData.examples.values()))

        self.assertEqual(
            sampleData.examples,
            {
                "medv(id348)": 23.1,
                "medv(id369)": 50.0,
                "medv(id344)": 23.9,
                "medv(id152)": 19.6,
                "medv(id120)": 19.3,
                "medv(id53)": 25.0,
                "medv(id422)": 14.2,
                "medv(id115)": 18.5,
                "medv(id235)": 29.0,
                "medv(id448)": 12.6,
                "medv(id3)": 34.7,
                "medv(id211)": 21.7,
                "medv(id334)": 22.2,
                "medv(id313)": 19.4,
                "medv(id13)": 21.7,
                "medv(id42)": 26.6,
                "medv(id439)": 84.0,
                "medv(id45)": 21.2,
                "medv(id183)": 37.9,
                "medv(id212)": 19.3,
                "medv(id374)": 13.8,
                "medv(id238)": 31.5,
                "medv(id294)": 23.9,
                "medv(id7)": 22.9,
                "medv(id62)": 16.0,
                "medv(id153)": 15.3,
                "medv(id345)": 31.2,
                "medv(id163)": 50.0,
                "medv(id341)": 18.7,
                "medv(id50)": 19.4,
                "medv(id208)": 22.5,
                "medv(id167)": 50.0,
                "medv(id70)": 20.9,
                "medv(id143)": 13.4,
                "medv(id217)": 23.3,
                "medv(id29)": 18.4,
                "medv(id181)": 39.8,
                "medv(id342)": 32.7,
                "medv(id59)": 23.3,
                "medv(id27)": 16.6,
                "medv(id188)": 32.0,
                "medv(id435)": 11.7,
                "medv(id173)": 23.1,
                "medv(id10)": 18.9,
            },
        )
