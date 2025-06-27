============================
Pythonic FP - Circular Array
============================

PyPI project `pythonic.circular-array <https://pypi.org/project/pythonic-fp.circulararray/>`_
implements a stateful, full featured, auto resizing, circular array data structure.

- O(1) amortized pushes and pops either end 
- O(1) indexing
- Auto-resizing larger when necessary, can be manually compacted if desired
- Iterable, can safely mutate while iterating over copies of previous state
- Fully supports slicing

This PyPI project is part of of the grscheller
`pythonic-fp namespace projects <https://grscheller.github.io/pythonic-fp/>`_
These projects take a Functional Programming approach to programming yet endeavor to remain
Pythonic.
