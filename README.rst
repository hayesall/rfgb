Relational Functional Gradient Boosting (RFGB)
==============================================

*Relational Functional Gradient Boosting in Python.*

  .. image:: https://img.shields.io/github/license/starling-lab/rfgb.py.svg?style=flat-square
	   :target: https://github.com/starling-lab/rfgb.py/blob/master/LICENSE
  .. image:: https://img.shields.io/github/tag/starling-lab/rfgb.py.svg?style=flat-square
	   :target: https://github.com/starling-lab/rfgb.py/releases
  .. image:: https://img.shields.io/travis/starling-lab/rfgb.py.svg?style=flat-square
	   :target: https://travis-ci.org/starling-lab/rfgb.py
  .. image:: https://img.shields.io/codecov/c/github/starling-lab/rfgb.py/master.svg?style=flat-square
	   :target: https://codecov.io/gh/starling-lab/rfgb.py?branch=master
  .. image:: https://readthedocs.org/projects/rfgbpy/badge/?version=stable&style=flat-square
	   :target: https://rfgbpy.readthedocs.io/en/stable/

**Kaushik Roy** (`@kkroy36`_) and **Alexander L. Hayes** (`@batflyer`_)

Installation
------------

Stable builds may be installed from PyPi

.. code-block:: bash

		pip install rfgb

Or develop further by cloning the repository

.. code-block:: bash

		git clone https://github.com/starling-lab/rfgb.py.git
		cd rfgb.py/
		python setup.py develop

Quick-Start
-----------

Learning with a relational dependency network.

   .. code-block:: bash

		   cd testDomains/Logistics/
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

A full `copy of the license <https://github.com/starling-lab/rfgb.py/blob/master/LICENSE>`_ is available in the base of this repository. For more information, see https://www.gnu.org/licenses/

Acknowledgements
----------------

The authors would like to thank Professor Sriraam Natarajan, Professor Gautam Kunapuli, and fellow members of the `StARLinG Lab <https://starling.utdallas.edu>`_ at the University of Texas at Dallas.

  .. _`@kkroy36`: https://github.com/kkroy36/
  .. _`@batflyer`: https://github.com/batflyer/
