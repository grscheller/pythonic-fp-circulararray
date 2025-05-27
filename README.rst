============================
Pythonic FP - Circular Array
============================

A stateful circular array data structure, part of the
`PyPI pythonic-fp Namespace Projects <https://github.com/grscheller/pythonic-fp/blob/main/README.md>`_.

Features
--------

Full featured auto resizing circular array data structure. Double sided,
indexable, sliceable, and iterable. When iterated, uses cached copies of its
present state so that the circular array itself can safely be mutated.

- O(1) amortized pushes and pops either end.
- O(1) indexing
- fully supports slicing
- safely mutates over previous state

Useful either if used directly like a Python list, or in a "has-a"
relationship when implementing other data structures.

Repositories
^^^^^^^^^^^^

- `pythonic-fp.circulararray <https://pypi.org/project/pythonic-fp.circulararray>`_ project on *PyPI*
- `Source code <https://github.com/grscheller/pythonic-fp-circulararray>`_ on *GitHub*.

Detailed documentation
^^^^^^^^^^^^^^^^^^^^^^

Detailed API
`documentation <https://grscheller.github.io/pythonic-fp/maintained/circulararray>`_
on *GH-Pages*.

Usage
-----

| from pythonic_fp.circulararray import CA, ca
|
| ca1 = ca(1, 2, 3)
| assert ca1.popl() == 1
| assert ca1.popr() == 3
| ca1.pushr(42, 0)
| ca1.pushl(0, 1)
| assert repr(ca1) == 'ca(1, 0, 2, 42, 0)'
| assert str(ca1) == '(|1, 0, 2, 42, 0|)'
|
| ca2 = CA(range(1,11))
| assert repr(ca2) == 'ca(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)'
| assert str(ca2) == '(|1, 2, 3, 4, 5, 6, 7, 8, 9, 10|)'
| assert len(ca2) == 10
| tup3 = ca2.poplt(3)
| tup4 = ca2.poprt(4)
| assert tup3 == (1, 2, 3)
| assert tup4 == (10, 9, 8, 7)
| assert ca2 == ca(4, 5, 6)
| four, *rest = ca2.poplt(1000)
| assert four == 4
| assert rest == [5, 6]
| assert len(ca2) == 0
|
| ca3 = CA([1, 2, 3])
| assert ca3.popld(42) == 1
| assert ca3.poprd(42) == 3
| assert ca3.popld(42) == 2
| assert ca3.poprd(42) == 42
| assert ca3.popld(42) == 42
| assert len(ca2) == 0

Installation
------------

| $ pip install pythonic-fp.circulararray

Support
-------

If you have any questions or issues with the software, feel free to reach out
to the maintainer at geoffrey@scheller.com, or submit an issue on GitHub's issue
tracker.

Contribute
^^^^^^^^^^

- Issue Tracker: https://github.com/grscheller/pythonic-fp-circulararray/issues
- Pull Requests: https://github.com/grscheller/pythonic-fp-circulararray/pulls

Contributers
^^^^^^^^^^^^

- `@grscheller <https://github.com/grscheller>`_ (Geoffrey R. Scheller - maintainer)

CHANGELOG
^^^^^^^^^

See the `CHANGELOG <https://github.com/grscheller/pythonic-fp-circulararray/blob/main/CHANGELOG.rst>`_

License
-------

This project is licensed under the Apache License Version 2.0, January 2004.
See the `LICENCE file <https://github.com/grscheller/pythonic-fp-circulararray/blob/main/LICENSE>`_
for details.
