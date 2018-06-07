# RFGB Unit Testing Overview

Unit tests should be invoked from the root of the repository. This is because individual test files invoke `sys.path.append('.')` to behave consistently and import modules from the correct sources.

To run the unit testing framework, run tests from the root directory.

```bash
[localhost]$ python tests/tests.py
```

To invoke a specific test suite (for example, only test the Utils.py module), run it instead.

```bash
[localhost]$ python tests/rfgbtests/test_Utils.py
```

## Organization

Unit tests should be organized so that they test functionality pertaining to a specific module. Files which test a specific module should be named test_**module**.py and placed in the `tests/rfgb/` directory.

Running the full unit testing framework (`tests/tests.py`) tests the contents of the `/rfgb/` directory.

A new file can be created by wrapping the tests with Python's unittest framework (additional documentation should be consulted online [Python 2](https://docs.python.org/2/library/unittest.html) [Python 3](https://docs.python.org/3/library/unittest.html)).

```python
import sys
import unittest

sys.path.append('./src/')

# import the appropriate module(s)
from (module) import (something)

class (module)Test(unittest.TestCase):

	# Unit tests should be preceded by "test_"

	def test_something(self):
		self.assertEqual(2, 2)
		
if __name__ == '__main__':
	# This line allows the test suite to be invoked when called.
	unittest.main()
```
