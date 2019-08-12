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

from rfgbtests import *
import unittest

if __name__ == "__main__":
    """
    Main testing module for ``rfgb``, must be ran from the base of the
    project repository.

    For example:

    .. code-block:: bash

                    python rfgb/tests/tests.py

    Verbosity may be explicitly set by passing an integer with the ``-v``
    flag. The value will be passed into unittest.TextTestRunner, so integers
    higher than 1 will lead to more verbose outputs.

    .. code-block:: bash

                    python rfgb/tests/tests.py -v 2

    Individual modules may be tested with unittest via the command line.

    .. code-block:: bash

                    python -m unittest rfgb/tests/rfgbtests/test_Utils.py
                    .......
                    --------------------------------------------------
                    Ran 7 tests in 0.005s

                    OK
    """

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", default=1, type=int)
    args = parser.parse_args()

    testsuite = unittest.TestLoader().discover(".")
    runner = unittest.TextTestRunner(verbosity=args.verbose)

    """
    @hayesall:

    I have not found a more elegant way to handle this problem, but
    to summarize: coverage and Travis-ci only seem to recognize errors
    when an exception is raised. TextTestRunner.run does not appear to
    raise exceptions on failures, so instead this must be done explicitly.
    """

    results = runner.run(testsuite)
    if results.failures or results.errors:
        raise (Exception("Encountered errors during runner.run"))
