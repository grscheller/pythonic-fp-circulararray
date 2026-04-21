usage
=====

How to installing the package
-----------------------------

Install the project into your Python environment:

.. code:: console

   $ pip install pythonic-fp.circulararray

Importing the package
---------------------

Import the circulararray classes and "factory functions" into your code.

.. code:: python

    from pythonic_fp.circulararray.auto import CA, ca
    from pythonic_fp.circulararray.fixed import CAF, caf

.. note::

    The behaviors of the ``CA`` and ``CAF`` classes were modeled after the Python ``list`` builtin.

    - they can be instantiated with data by supplying an iterable
    - with no unnamed arguments they are instantiated empty
    - methods which modify the objects return no values
    - their corresponding factory functions ``ca`` and ``caf`` behave like Python's ``[]`` syntax.

      - each creates its corresponding circulararray object from the arguments passed to it
