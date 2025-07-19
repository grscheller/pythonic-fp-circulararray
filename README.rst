PPythonic FP - Circular Array
=============================

PyPI project
`pythonic-fp.circulararray
<https://pypi.org/project/pythonic-fp.circulararray>`_.

Python module implementing a stateful circular array data structure.

- O(1) pops either end 
- O(1) amortized pushes either end 
- O(1) indexing, fully supports slicing
- Auto-resizing larger when necessary, manually compatible
- iterable, can safely mutate while iterators continue iterating over previous state
- comparisons compare identity before equality, like builtins
- in boolean context returns true when not empty, false when empty

This PyPI project is part of of the grscheller
`pythonic-fp namespace projects
<https://github.com/grscheller/pythonic-fp/blob/main/README.md>`_

Documentation
-------------

Documentation for module
`pythonic_fp.circulararray
<https://grscheller.github.io/pythonic-fp/circulararray/API/development/build/html/releases.html>`_
hosted on GitHub pages.

Copyright and License
---------------------

Copyright (c) 2023-2025 Geoffrey R. Scheller. Licensed under the Apache
License, Version 2.0. See the LICENSE file for details.
