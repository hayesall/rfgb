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

from ..boosting import updateGradients
from ..tree import node
from ..utils import Utils


def learn(
    targets,
    numTrees=10,
    path="",
    regression=False,
    advice=False,
    softm=False,
    alpha=0.0,
    beta=0.0,
    saveJson=True,
):
    """
    .. versionadded:: 0.3.0

    Learn a relational dependency network from facts and positive/negative
    examples via relational regression trees.

    .. note:: This currently requires that training data is stored as files
              on disk.

    :param targets: List of target predicates to learn models for.
    :type targets: list of str.

    :param numTrees: Number of trees to learn.
    :type numTrees: int.

    :param path: Path to the location training data is stored.
    :type path: str.

    :param regression: Learn a regression model instead of classification.
    :type regression: bool.

    :param advice: Read an advice file from the same directory as trainPath.
    :type advice: bool.

    :default regression: False
    :default advice: False

    :returns: Dictionary where the key is the target and the value is the
              set of trees returned for that target.
    :rtype: dict.
    """

    # Models will be returned as a dictionary, where the name of the predicate
    # will be bound to the set of trees learned for it.
    models = {}

    for target in targets:

        # Read the training data.
        trainData = Utils.readTrainingData(
            target,
            path=path,
            regression=regression,
            advice=advice,
            softm=softm,
            alpha=alpha,
            beta=beta,
        )

        # Initialize an empty list for the trees.
        trees = []

        # Learn each tree and update the gradients.
        for i in range(numTrees):

            node.setMaxDepth(2)
            node.learnTree(trainData)
            trees.append(node.learnedDecisionTree)
            updateGradients(trainData, trees)

            # Save the models learned at this step.
            if saveJson:

                # Collect the parameters used to learn these trees:
                params = {
                    "target": target,
                    "trees": i + 1,
                    "regression": regression,
                    "advice": advice,
                    "softm": softm,
                    "alpha": alpha,
                    "beta": beta,
                }

                # Save a json file containing parameters and trees learned.
                model = [params, trees]
                Utils.save(".rfgb/models/" + target + ".json", model)

        models[target] = trees

    return models
