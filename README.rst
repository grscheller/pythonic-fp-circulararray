============================
Pythonic FP - Circular Array
============================

PyPI project `pythonic.circular-array <https://pypi.org/project/pythonic-fp.circulararray/>`_
implements a stateful, full featured auto resizing circular array data structure.

- O(1) amortized pushes and pops either end 
- O(1) indexing
- Auto-resizes itself larger if necessary

  - Can be manually compacted if desired

- Iterable

  - safely iterates over cached copies of previous state
  - allowing the data structure to safely mutate

- Fully supports slicing


It is part of of the grscheller
`pythonic-fp namespace projects <https://grscheller.github.io/pythonic-fp/>`_
on PyPI. These projects take a Functional Programming approach to programming yet endeavor to remain
Pythonic.
