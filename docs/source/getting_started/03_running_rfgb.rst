============
Running rfgb
============

  .. toctree::
     :glob:
     :maxdepth: 1

Reasoning about the World
-------------------------

Object and their relationships are a natural way to think about the world. In this example, we have some facts about the world which we want to learn from. More specifically, we have a table of people and their relationships.

+-----------+------------+-------------+-------------+
| **Name**  | **Gender** | **Child**   | **Sibling** |
+-----------+------------+-------------+-------------+
| James     | Male       | [Harry]     | -           |
+-----------+------------+-------------+-------------+
| Lily      | Female     | [Harry]     | Petunia     |
+-----------+------------+-------------+-------------+
| Harry     | Male       | -           | -           |
+-----------+------------+-------------+-------------+
| Arthur    | Male       | [Ron, Fred] | -           |
+-----------+------------+-------------+-------------+
| Molly     | Female     | [Ron, Fred] | -           |
+-----------+------------+-------------+-------------+
| Ron       | Male       | -           | [Fred]      |
+-----------+------------+-------------+-------------+
| Fred      | Male       | -           | [Ron]       |
+-----------+------------+-------------+-------------+

Assume that the goal is to learn ``father(Y,X)``. We want to learn logical rules representing that domain object X is the father of Y (both of which are people in this case), given that you know information about their gender, children, and siblings.

From Tables to First-order Predicate Logic
------------------------------------------

Once we have a high-level idea of what these relationships look like, the next step is to convert this into predicate logic format. This format is standard for most Prolog-based systems.


A few assumptions we will make about our data:

1. 'Name' is an identifier.
2. 'Gender' is male or female in this case, so we can make it a true/false value.
3. 'Child' and 'Sibling' are binary relationships encoding a relationship between two people (e.g. ``childof(lily, harry)`` denotes that 'harry' is the childof 'lily').

The *target* we want to learn is ``father(x,y).`` To learn this rule, ``rfgb`` learns a decision tree that most effectively splits the positive and negative examples. This example is fairly small so a small number of trees should suffice, but for more complicated problem more may be needed to learn a robust model.

Positive Examples:

.. code-block:: prolog

		father(harrypotter,jamespotter).
		father(ginnyweasley,arthurweasley).
		father(ronweasley,arthurweasley).
		father(fredweasley,arthurweasley).
		...

Negative Examples:

.. code-block:: prolog

		father(harrypotter,mollyweasley).
		father(georgeweasley,jamespotter).
		father(harrypotter,arthurweasley).
		father(harrypotter,lilypotter).
		father(ginnyweasley,harrypotter).
		father(mollyweasley,arthurweasley).
		father(fredweasley,georgeweasley).
		father(georgeweasley,fredweasley).
		father(harrypotter,ronweasley).
		father(georgeweasley,harrypotter).
		father(mollyweasley,lilypotter).
		...

Facts:

.. code-block:: prolog

		  male(jamespotter).
		  male(harrypotter).
		  male(arthurweasley).
		  male(ronweasley).
		  male(fredweasley).
		  male(georgeweasley).
		  siblingof(ronweasley,fredweasley).
		  siblingof(ronweasley,georgeweasley).
		  siblingof(ronweasley,ginnyweasley).
		  siblingof(fredweasley,ronweasley).
		  siblingof(fredweasley,georgeweasley).
		  siblingof(fredweasley,ginnyweasley).
		  siblingof(georgeweasley,ronweasley).
		  siblingof(georgeweasley,fredweasley).
		  siblingof(georgeweasley,ginnyweasley).
		  siblingof(ginnyweasley,ronweasley).
		  siblingof(ginnyweasley,fredweasley).
		  siblingof(ginnyweasley,georgeweasley).
		  childof(jamespotter,harrypotter).
		  childof(lilypotter,harrypotter).
		  childof(arthurweasley,ronweasley).
		  childof(mollyweasley,ronweasley).
		  childof(arthurweasley,fredweasley).
		  childof(mollyweasley,fredweasley).
		  childof(arthurweasley,georgeweasley).
		  childof(mollyweasley,georgeweasley).
		  childof(arthurweasley,ginnyweasley).
		  childof(mollyweasley,ginnyweasley).
		  ...

Training a Model
----------------

There is one more piece we still need: background knowledge about the world.

.. code-block:: prolog

		// Parameters
		setParam: maxTreeDepth=3.
		setParam: nodeSize=1.
		setParam: numOfClauses=8.

		// Modes
		mode: male(+name).
		mode: childof(+name,+name).
		mode: siblingof(+name,-name).
		mode: father(+name,+name).

Begin training:

.. code-block:: bash

		python -m rfgb --help
