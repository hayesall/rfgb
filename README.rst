##############################################
Relational Functional Gradient Boosting (rfgb)
##############################################

|PyPi|_ |License|_ |Travis|_ |Codecov|_ |ReadTheDocs|_

.. |PyPi| image:: https://img.shields.io/pypi/v/rfgb.svg
  :alt: Python Package Index (PyPi) latest version.
.. _PyPi: https://pypi.org/project/rfgb/

.. |License| image:: https://img.shields.io/github/license/hayesall/rfgb.svg
  :alt: License.
.. _License: https://github.com/hayesall/rfgb/blob/master/LICENSE

.. |Travis| image:: https://travis-ci.org/hayesall/rfgb.svg?branch=master
  :alt: Master branch build status.
.. _Travis: https://travis-ci.org/hayesall/rfgb

.. |Codecov| image:: https://codecov.io/gh/hayesall/rfgb/branch/master/graphs/badge.svg?branch=master
  :alt: Master branch code coverage.
.. _Codecov: https://codecov.io/github/hayesall/rfgb?branch=master

.. |ReadTheDocs| image:: https://readthedocs.org/projects/rfgb/badge/?version=latest
  :alt: Documentation build status and link to documentation.
.. _ReadTheDocs: http://rfgb.readthedocs.io/en/latest/

**rfgb**: Relational Functional Gradient Boosting (in Python).

- **Documentation**: https://rfgb.readthedocs.io/en/latest/
- **Questions?** Contact `Alexander L. Hayes (hayesall) <https://hayesall.com>`_

Installation
------------

Stable builds may be installed from PyPi

.. code-block:: bash

		pip install rfgb

Or develop further by cloning the repository

.. code-block:: bash

		git clone https://github.com/hayesall/rfgb.git
		cd rfgb/
		python setup.py develop

Quick-Start
-----------

Learning with a relational dependency network.

.. code-block:: bash

   cd testDomains/Logistics/
   rfgb init
   rfgb learn rdn -target unload

Additional options for each subcommand may be viewed by passing ``-h`` as a parameter.

.. code-block:: bash

   rfgb -h
   rfgb learn rdn -h


Classification with Expert Advice (``-advice``)
--------------------------------------------------

Preferred and non-preferred labels may be provided as advice during classification via logical rules. This advice may be specified in a file named ``advice.txt`` in the train directory for a dataset.

Four datasets (BlocksWorld, HeartAttack, Logistics, and MoodDisorder) have an advice file included for demonstration

1. Logistics

.. code-block:: bash

    cd testDomains/Logistics/
    rfgb init
    rfgb learn rdn -advice -target unload

2. HeartAttack

.. code-block:: bash

    cd testDomains/HeartAttack/
    rfgb init
    rfgb learn rdn -advice -target ha


Targets
-------

"Targets" specify what is learned, examples of the target are provided in ``pos.txt``, ``neg.txt``, or ``examples.txt`` (for regression). These are specified here for convenience.

+---------------+------------------------+
| **Dataset**   | **Target**             |
+---------------+------------------------+
| BlocksWorld   | ``putdown``            |
+---------------+------------------------+
| BostonHousing | ``medv``               |
+---------------+------------------------+
| HeartAttack   | ``ha``                 |
+---------------+------------------------+
| Insurance     | ``value``              |
+---------------+------------------------+
| Logistics     | ``unload``             |
+---------------+------------------------+
| MoodDisorder  | ``bipolar``            |
+---------------+------------------------+
| TicTacToe     | ``put`` or ``dontput`` |
+---------------+------------------------+
| ToyCancer     | ``cancer``             |
+---------------+------------------------+
| XOR           | ``xor``                |
+---------------+------------------------+

In Development
--------------

- Test cases (codecov >90%)
- General interaction improvements for commandline and library
- Learning Markov Logic Networks

License
-------

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

A full `copy of the license <https://github.com/hayesall/rfgb/blob/master/LICENSE>`_ is available in the base of this repository. For more information, see https://www.gnu.org/licenses/
