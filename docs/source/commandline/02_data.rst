====
Data
====

As data scientists, a great deal of time is often spent getting data into a particular format. It is overly-ambitious to claim that we have *solved* this problem, but we try to reduce the time spent cleaning data.

The format we use is similar to *Prolog*, but with a clear distinction between *data* and *programs*.

Machine Learning is often described as learning a function over a vector :math:`x` such that we can learn a target value :math:`y`.

.. math::

  f(x) = P( y | x )

Defining Terms
--------------

The terms we invoke to describe these functions are **Positives**, **Negatives**, **Facts**, and **Background Knowledge**.

* **Positive** examples are true (or correct) examples that we want to learn from.

* **Negative** examples are false (or incorrect), examples that we do not want to do.

* **Facts** are features we use to learn. We make the assumption that some combination of the facts can be used to distinguish between positives and negatives.

* **Background Knowledge** comes in many forms, but is a way to introduce more information to learn more effectively. If a classifier is learning to distinguish handwritten digits, extra negative examples might be created by rotating digits. *Background Knowledge* about this domain might involve **not** rotating "6" and "9", since they are identical when rotated.

Background Knowledge is often described as the "black magic" or "expert knowledge" in machine learning. Many of our methods are designed to effectively incorporate this kind of knowledge, and solicit it in a variety of ways.

Format
------

Positives, negatives, and facts are contained in ``pos.txt``, ``neg.txt``, and ``facts.txt``. Some examples are contained in the ``testDomains`` directory at the base of this repository.

For example: ``testDomains/HeartAttack/train/``:

+-----------------------+-----------------------+-----------------------+
| ``pos.txt``           | ``neg.txt``           | ``facts.txt``         |
+-----------------------+-----------------------+-----------------------+
|.. code-block:: prolog |.. code-block:: prolog |.. code-block:: prolog |
|                       |                       |                       |
|    ha(p1)             |    ha(p2)             |    chol(p1,high)      |
|    ha(p6)             |    ha(p3)             |    race(p1,r1)        |
|                       |    ha(p4)             |    chol(p2,medium)    |
|                       |    ha(p5)             |    race(p2,r1)        |
|                       |    ha(p7)             |    chol(p3,medium)    |
|                       |    ha(p8)             |    race(p3,r1)        |
|                       |    ha(p9)             |    chol(p4,medium)    |
|                       |    ha(p10)            |    race(p4,r1)        |
|                       |                       |    chol(p5,low)       |
|                       |                       |    race(p5,r1)        |
|                       |                       |    chol(p6,high)      |
|                       |                       |    race(p6,r2)        |
|                       |                       |    chol(p7,medium)    |
|                       |                       |    race(p7,r2)        |
|                       |                       |    chol(p8,medium)    |
|                       |                       |    race(p8,r2)        |
|                       |                       |    chol(p9,medium)    |
|                       |                       |    race(p9,r2)        |
|                       |                       |    chol(p10,low)      |
|                       |                       |    race(p10,r2)       |
+-----------------------+-----------------------+-----------------------+

.. code-block:: prolog

  ha(person)
  chol(+person,[low;medium;high])
  race(+person,[r1;r2])

Positve

The latter are inspired by the FOIL method and paper.
