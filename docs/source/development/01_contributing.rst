============
Contributing
============

  .. toctree::
     :glob:
     :maxdepth: 1

From the BoostSRL Contributing Guidelines:

| "Our goal is to push the boundaries of machine learning and statistical relational learning through open development and explainable approaches to decision making in both learning and inference. We believe that these are some of the best ways to create trustworthy systems that people can learn from and interract with in their daily lives."

The goal in this project is to match and eventually extend beyond `BoostSRL <https://github.com/starling-lab/BoostSRL>`_ (the Java version of the codebase), contributions which further this are welcome.

Code of Conduct
---------------

We adopt the `Contributor Covenant Code of Conduct <https://www.contributor-covenant.org/>`_

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at alexander.hayes@utdallas.edu. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate for the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of the incident.

Development Cheat-Sheet
-----------------------

1. **Fork and clone the source from GitHub**

   .. code-block:: bash

		   git clone https://github.com/starling-lab/rfgb.py.git

2. **Building local copy of documentation**

   We use Sphinx autodoc with a combination of inline docstrings and reStructuredText for documenting this project. Pull requests and further updates should include appropriate documentation.
   
   A local copy of the documentation may be built from the Makefile:

   .. code-block:: bash

		   cd docs
		   make html
		   xdg-open build/html/index.html

3. **Running the unit tests**

   ``rfgb/tests/`` contains a suite of unit tests, these can be ran via the following:

   .. code-block:: bash

		   python rfgb/tests/tests.py

   .. note:: As of 0.2.0, these should be ran from the base of the repository due to their import structure.
