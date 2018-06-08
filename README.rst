Relational Functional Gradient Boosting (RFGB)
==============================================

*Relational Functional Gradient Boosting in Python.*

  .. image:: https://img.shields.io/github/license/starling-lab/rfgb.py.svg?style=flat-square
	   :target: https://github.com/starling-lab/rfgb.py/blob/master/LICENSE
  .. image:: https://img.shields.io/github/tag/starling-lab/rfgb.py.svg?style=flat-square
	   :target: https://github.com/starling-lab/rfgb.py/releases
  .. image:: https://img.shields.io/travis/starling-lab/rfgb.py.svg?style=flat-square
	   :target: https://travis-ci.org/starling-lab/rfgb.py.svg?branch=master
  .. image:: https://img.shields.io/codecov/c/github/starling-lab/rfgb.py/master.svg?style=flat-square
	   :target: https://codecov.io/gh/starling-lab/rfgb.py?branch=master
  .. image:: https://readthedocs.org/projects/rfgbpy/badge/?version=stable&style=flat-square
	   :target: https://rfgbpy.readthedocs.io/en/stable/

**Kaushik Roy** (`@kkroy36`_) and **Alexander L. Hayes** (`@batflyer`_)

Installation
------------

Stable builds on PyPi

.. code-block:: bash

		pip install rfgb

Development builds on GitHub

.. code-block:: bash

		pip install git+git://github.com/starling-lab/rfgb.py.git

Quick-Start
-----------
		
1. ``git clone https://github.com/starling-lab/rfgb.py.git``
2. ``cd rfgb.py``
3. Perform classification in a logistics domain:

   .. code-block:: bash

		   python -m rfgb -target unload -train testDomains/Logistics/train/ -test testDomains/Logistics/test/ -trees 10

Classification with Expert Advice (``-expAdvice``)
--------------------------------------------------

Preferred and non-preferred labels may be provided as advice during classification via logical rules. This advice may be specified in a file named ``advice.txt`` in the train directory for a dataset.

Four datasets (BlocksWorld, HeartAttack, Logistics, and MoodDisorder) have an advice file included for demonstration

1. Logistics

   .. code-block:: bash

		   python -m rfgb -expAdvice -target unload -train testDomains/Logistics/train/ -test testDomains/Logistics/test/ -trees 10

2. HeartAttack

   .. code-block:: bash

		   python -m rfgb -expAdvice -target ha -train testDomains/HeartAttack/train/ -test testDomains/HeartAttack/test/ -trees 10

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

- [ ] Test cases (codecov >90%)
- [ ] Learning Markov Logic Networks
- [ ] Learning with Soft-Margin

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
