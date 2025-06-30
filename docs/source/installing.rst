Installation
============

How to installing the module
------------------------------------

Install the project into your Python environment:

.. code:: console

    $ pip install pythonic-fp.circulararray

Importing the module
------------------------------------

Import the ``CA`` class and ``ca`` "factory function" into your code.

.. code:: python

    from pythonic_fp.circulararray import CA, ca

.. Note::

   Like the built-in Python list, ``CA`` takes up to one iterable, while
   the ``ca`` function behaves like Python's ``[]`` syntax. ``ca`` creates
   a ``CA`` object from the arguments past to it.

