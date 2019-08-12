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
rfgb
----

(docstring for main function)
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from .boosting import updateGradients
from .boosting import performInference
from .tree import node
from .utils import Utils
from ._metadata import __version__

# Imports for subpackages
from . import cmd
from . import rdn

import argparse
import os
import sys

# Create an argument parser for interpretting user inputs.
PARSER = argparse.ArgumentParser(
    prog="rfgb",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=(
        "rfgb: Relational Functional Gradient Boosting is a gradient-boosting\n"
        "approach to learning statistical relational models.\n\n"
        "Start a working area (see also: rfgb help tutorial)\n"
        "   init    Initialize an empty .rfgb directory at current location."
    ),
    epilog=(
        "Copyright © 2017-2019 rfgb Contributors. Distributed under the terms\n"
        "of the GNU GPL version 3 or later. <http://gnu.org/licenses/gpl.html>\n"
        "This is free software: you are free to change and redistribute it.\n"
        "There is NO WARRANTY, to the extent permitted by law.\n"
    ),
)

# Create subparsers for learning different types of models, their respective
# arguments may be set individually (for example, if advice is implemented
# for RDNs but has not been worked out for MLNs).

# This is different from BoostSRL's codebase, where the default is RDN and
# MLNs are learned by supplying a -mln flag. This change is to make things
# more-easily extended in the future.
SUBPARSERS = PARSER.add_subparsers(
    title="rfgb Subcommands", help="$ rfgb --help", dest="_rfgb"
)

INIT_PARSER = SUBPARSERS.add_parser(
    "init",
    description=(
        "Initialize an rfgb package in the current directory for saving,\n"
        "loading, and managing models.",
    ),
    help="Initialize a .rfgb directory.",
)
HELP_PARSER = SUBPARSERS.add_parser(
    "help", description="Commandline references for common actions."
)

LEARN_PARSER = SUBPARSERS.add_parser(
    "learn", description="Specify the model to learn.", help="Learn various SRL models."
)

INFER_PARSER = SUBPARSERS.add_parser(
    "infer",
    description="Make inferences using the working model.",
    help="Infer with various SRL models.",
)

# Sub-commands specific to learning different models.
LEARN_SUBPARSER = LEARN_PARSER.add_subparsers(
    title="RFGB Learn",
    description="Learning statistical relational models.",
    help="$ rfgb learn --help",
    dest="_learn",
)
RDN_PARSER = LEARN_SUBPARSER.add_parser(
    "rdn",
    description="Relational Dependency Networks",
    help="Relational Dependency Networks",
)
MLN_PARSER = LEARN_SUBPARSER.add_parser(
    "mln", description="Markov Logic Networks", help="Markov Logic Networks"
)
SPN_PARSER = LEARN_SUBPARSER.add_parser(
    "spn", description="Sum-Product Networks", help="Sum-Product Networks"
)
RRBM_PARSER = LEARN_SUBPARSER.add_parser(
    "rrbm",
    description="Relational Restricted Boltzmann Machines",
    help="Relational Restricted Boltzmann Machines",
)

# infer-specific arguments
INFER_PARSER.add_argument(
    "-target",
    "--target",
    type=str,
    default=None,
    action="append",
    help="Target predicate(s) to infer.",
)

# init-specific arguments
INFER_PARSER.add_argument(
    "-test", "--test", type=str, default="test/", help="Set the testing directory."
)
INIT_PARSER.add_argument("-q", "--quiet", help="Quiet output.", action="store_true")

# RDN-specific arguments.
RDN_PARSER.add_argument(
    "-advice",
    "--advice",
    help=(
        "Trigger learning with expert advice. Currently reads from an "
        "advice.txt file stored in the same location as the data."
    ),
    action="store_true",
)
RDN_PARSER.add_argument(
    "-reg",
    "--regression",
    help="Learn a regression model instead of a classification model.",
    action="store_true",
)
RDN_PARSER.add_argument(
    "-softm",
    "--softm",
    help=(
        "Softmax boosting. Set the false positive weight (alpha)"
        "and false negative weight (beta) along with this parameter."
    ),
    default=False,
    action="store_true",
)
RDN_PARSER.add_argument(
    "-alpha",
    "--alpha",
    help="Set the alpha value for use with softm.",
    type=float,
    default=0.0,
)
RDN_PARSER.add_argument(
    "-beta",
    "--beta",
    help="Set the beta value for use with softm.",
    type=float,
    default=0.0,
)
RDN_PARSER.add_argument(
    "-trees",
    "--trees",
    type=int,
    default=10,
    help="Specify the number of boosted regression trees to learn (Default: 10)",
)
RDN_PARSER.add_argument(
    "-target",
    "--target",
    type=str,
    default=None,
    action="append",
    help="Target predicate(s) to learn.",
)
RDN_PARSER.add_argument(
    "-train", "--train", type=str, default="train/", help="Set the training directory."
)

# Get the arguments
PARAMETERS = PARSER.parse_args()

if PARAMETERS._rfgb == "init":
    # Initialize an empty rfgb repository for loading and saving models.
    cmd.init(quiet=PARAMETERS.quiet)

elif PARAMETERS._rfgb == "help":
    print("Help information.")

elif PARAMETERS._rfgb == "learn":

    if PARAMETERS._learn == "rdn":
        print("Learning RDN.")

        if not PARAMETERS.target:
            raise (ValueError("'target' must be provided."))

        TREES = rdn.learn(
            PARAMETERS.target,
            path=PARAMETERS.train,
            regression=PARAMETERS.regression,
            advice=PARAMETERS.advice,
            softm=PARAMETERS.softm,
            alpha=PARAMETERS.alpha,
            beta=PARAMETERS.beta,
        )

    elif PARAMETERS._learn == "mln":
        print("Learning MLN (TODO)")
        exit(1)

    elif PARAMETERS._learn == "spn":
        print("Learning SPN (TODO)")
        exit(1)

    elif PARAMETERS._learn == "rrbm":
        print("Learning RRBM (TODO)")
        exit(1)

elif PARAMETERS._rfgb == "infer":

    if PARAMETERS.target:
        TARGETS = PARAMETERS.target
    else:
        # Collect each target from the files in the .rfgb/models/ directory.
        TARGETS = list(
            map(lambda s: s.replace(".json", ""), os.listdir(".rfgb/models/"))
        )

    for target in TARGETS:

        model = Utils.load(".rfgb/models/" + target + ".json")
        settings, trees = model[0], model[1]

        results = rdn.infer(
            target, trees, path=PARAMETERS.test, regression=settings["regression"]
        )

        # Print results for easy viewing.
        print(results)

    exit(0)

else:
    print("Reached end of program without performing any action.")
    exit(1)
exit(0)
