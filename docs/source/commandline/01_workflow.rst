========
Workflow
========

CLI interface for performing learning and inference with different types of statistical relational learning methods, and managing these learned models for particular data sets.

Some of the ideas built here are shamelessly inspired by Git, so the workflows for using the commandline interface to ``rfgb`` should hopefully feel somewhat familiar to those familiar with version control.

.. code-block:: text

                $ pip install rfgb
                $ rfgb --help
                usage: rfgb [-h] [-V] {init,learn,infer} ...

                rfgb: Relational Functional Gradient Boosting is a gradient-boosting
                approach to learning statistical relational models.

                optional arguments:
                  -h, --help          show this help message and exit
                  -V, --version       show version number and exit

                rfgb Subcommands:
                  Commands and subcommands for rfgb.

                  {init,learn,infer}  $ rfgb --help
                    init              Initialize a .rfgb directory.
                    learn             Learn various SRL models.
                    infer             Infer with various SRL models.

Assuming you start with a training and test set (we'll talk about those later), you can initialize a place where your models and meta-data will be stored.

.. code-block:: text

                $ rfgb init

This creates a ``.rfgb`` directory containing a ``models`` directory.
