==========
Unit Tests
==========

The main testing module for ``rfgb`` must be ran from the base of the project repository.

For example:

.. code-block:: bash

                python rfgb/tests/tests.py

Verbosity may be explicitly set by passing an integer with the ``-v`` flag. The value will be passed into unittest.TextTestRunner, so integers higher than 1 will lead to more verbose outputs.

.. code-block:: bash

                python rfgb/tests/tests.py -v 2

Testing Individual Modules
--------------------------

Individual modules may be tested with unittest via the command line.

.. code-block:: bash

                python -m unittest rfgb/tests/rfgbtests/test_Utils.py
                .......
                --------------------------------------------------
                Ran 7 tests in 0.005s

                OK
