=====================================
CHANGELOG: Pythonic FP Circular Array 
=====================================

PyPI pythonic-fp.circulararray project.

- Strict 3 digit semantic versioning (adopted 2025-05-19)

  - MAJOR version for incompatible API changes
  - MINOR version for backward compatible added functionality
  - PATCH version for backward compatible bug fixes

See `Semantic Versioning 2.0.0 <https://semver.org>`_.

Releases and Important Milestones
---------------------------------

Version 5.1.0 - PyPI release date TBD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- switched from pdoc to sphinx for document generation

  - created docs/ directory for document generation
  - no longer source code controlling generated HTML (too wasteful)
  - using sphinx.ext.githubpages extension to publish from this repo

- some formatting changes, but no actual code changes
- made pyproject.toml improvements

  - better tooling configurations
  - removed all version caps from pyproject.toml

    - see `this blog post <https://iscinumpy.dev/post/bound-version-constraints>_.

Version 3.14.0 - PyPI release date 2025-05-10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Made package just a single module.

- dtools.circular_array.ca -> dtools.circular_array
- docstring consolidations/updates

Version 3.13.0 - PyPI release date 2025-05-06
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Version no longer determined dynamically.

  - made all non-splatted method parameters position only
  - version now set in pyproject.toml
  - no longer doing 4 part development versioning
  - version will either denote

    - the current PyPI release - if no substantive changes made
    - the next PyPI release - what development is working toward

Version 3.12.1 - PyPI release date 2025-04-22
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- docstring changes
- pyproject.toml standardization

Version 3.12.0 - PyPI release date 2025-04-07
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

API change. 

- class CA[D] no longer inherits from Sequence[D]
- typing improvements

Version 3.11.0 - PyPI release date 2025-04-06
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Major API change.

- swapped names `ca` and `CA`

  - class name now `CA`
  - factory function taking variable number of arguments is now `ca`

- class initializer still takes `1` or `0` iterables

  - still want this class to behave like a builtin
  - but got tired fighting linters
  - maybe being "Pythonic" means

    - that only builtins should break naming conventions
    - naming conventions being

      - snake_case for functions and method names
      - CamelCase for class names

    - perhaps a visual distinction is useful to tell when you
      - are dealing with user/library Python code
      - C code presenting itself as a Python class

- typing improvements
  
Version 3.10.1 - PyPI release date 2025-04-03
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Major API changes.

- class name still `ca`

  - initializer takes 1 or 0 iterables

    - like Python builtin types `list` or `tuple`

  - factory function `CA` provided to create a `ca` from mult args

    - like `[]` or `{}`

- otherwise, method names are all snake_case compatible

  - examples  

    - popL -> popl
    - pushR -> pushr
    - fractionFilled -> fraction_filled

- updated pyproject.toml
  - to better match other dtools namespace projects

Version 3.9.1 - PyPI release date 2025-02-16
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fixed pdoc issues with new typing notation.

- updated docstrings
- had to add TypeVars

Version 3.9.0 - PyPI release date 2025-01-16
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Final release as dtools.circular-array, - was previously
grscheller.circular-array.

Version 3.8.0 - PyPI release date 2025-01-03
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now circular-array indexing methods fully support slicing, also added
the rotL(n) and rotR(n) methods.

Version 3.7.1 - PyPI release date 2024-11-18
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For internal changes. Mostly for consistency across PyPI namespace projects

Version 3.7.0 - PyPI release date 2024-10-26
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Regenerated docs for PyPI release.

Version 3.6.3.2 - Commit date 2024-10-20
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Preparing for a 3.7.0 PyPI release.

- renamed class ca -> CA
- created factory function for original constructor use case
- generated docs in docs repo

Version 3.6.2 - PyPI release date 2024-10-20
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Removed docs from repo, now docs for all grscheller namespace projects located
[here](https://grscheller.github.io/grscheller-pypi-namespace-docs/).

Version 3.6.1 - PyPI release date 2024-10-18
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Infrastructure and minor docstring changes. Should be compatible with
version 3.6.0.

Version 3.6.0 - PyPI release date 2024-09-21
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

No future changes planned for the foreseeable future

- feature complete
- no external dependencies
- well tested with other grscheller namespace packages
- final API tweaks made
- several more pytest tests added
- made the `compact` method private, now called `_compact_storage_capacity`

Version 3.5.0 - PyPI release date 2024-09-21
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- made the `double` method p- O(1) amortized pushes and pops either end.
- O(1) indexing
- fully supports slicing
- safely mutates over previous staterivate, now called `_double_storage_capacity`
- major docstring improvements
- improved indentation and code alignment, now much more Pythonic

Version 3.4.1 - PyPI release date 2024-08-17
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- updated README.md to reflect name changes of CA methods
- docstring improvements

Version 3.4.0 - PyPI release date 2024-08-15
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Updated `__eq__` comparisons.

- first compare elements by identity before equality

  - I noticed that is what Python builtins do
  - makes dealing with grscheller.fp.nada module easier

- standardizing docstrings across grscheller PyPI projects

Version 3.3.0.1 - commit date 2024-08-05
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- made a paradigm "regression", preparing for a 3.4.0 release
- felt CA was becoming way too complicated
- grscheller.datastructures needed it to fully embrace type annotations

  - but I was shifting too many features back into grscheller.circular-array
  - want ca to be useful for non-functional applications

Changes made:

- removed grscheller.fp dependency
- remove `_sentinel` and `_storable` slots from CA class
- remove copy method, just use `ca2 = CA(*ca1)` to make a shallow copy
- adjust `__repr__` and `__str__` methods
- experimenting with Spinx syntax in docstrings (still using pdoc3)
- changed nomenclature from "left/right" to "front/rear"
- unsafe and safe versions of pop & fold functionality
- left and right folds improvements

  - consolidated `foldL, foldL1, foldR, foldR1` into `foldL` & `foldR`
  - TODO: rename `foldL` to `fold_forward` & `foldR` to `fold_backward`

- tests working

  - basically I changed pops to unsafe pops and added `try except` blocks
  - safe versions tests needed

    - safe pops return multiple values in tuples
    - will take a `default` value to return

      - if only asked to return 1 value and CA is empty
      - seems to work properly from iPython

Version 3.2.0 - PyPI release date 2024-07-26
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The class name was changed CircularArray -> CA

Now takes a "sentinel" or "fallback" value in its initializer formally used None
for this.

Version 3.1.0 - PyPI release date 2024-07-11
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generic typing now being used, first PyPI release where multiplw values can be
pushed on CircularArray.

Version 3.0.0 - commit date 2024-06-28
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CircularArray class now using Generic Type Parameter. new epoch in development,
start of 3.0 series. Now using TypeVars.

API changes:

- ``foldL(self, f: Callable[[T, T], T]) -> T|None``
- ``foldR(self, f: Callable[[T, T], T]) -> T|None``
- ``foldL1(self, f: Callable[[S, T], S], initial: S) -> S``
- ``foldR1(self, f: Callable[[T, S], S], initial: S) -> S``

Version 2.0.0 - PyPI release date 2024-03-08
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- new epoch due to resizing bug fixed on previous commit

  - much improved and cleaned up
  - much better test suite

- method `_double()` made "public" and renamed `double()`
- method `resize(new_size)` now resizes to at least new_size

Version 1.1.0.0 - commit date 2024-03-08
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- NEXT PyPI RELEASE WILL BE 2.0.0 !!!!!!!!!!!
- BUGFIX: Fixed a subtle resizing bug

  - bug probably present in all previous versions

    - not previously identified due to inadequate test coverage

  - test coverage improved vastly

- made some major code API changes

  - upon initialization minimizing size of the CircularArray
  - have some ideas on how to to improve API for resizing CircularArrays
  - need to test my other 2 PyPI projects

    - both use circular-array as a dependency

Version 1.0.1 - PyPI release date 2024-03-01
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Docstring updates to match other grscheller PyPI repos.

Version 1.0.0 - PyPI release date 2024-02-10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First stable release, - dropped minimum Python requirement to 3.10.

Version 0.1.1 - PyPI release date 2024-01-30
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Changed circular-array from a package to just a module, actually a breaking API
change. Version number should have been 0.2.0 Also, gave CircularArray class
`foldL` & `foldR` methods

Version 0.1.0 - PyPI release date 2024-01-28
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- initial PyPI grscheller.circular-array release
- migrated Circulararray class from grscheller.datastructures
- update docstrings to reflect current nomenclature

Version 0.0.3 - commit date 2024-01-28
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- got gh-pages working for the repo

Version 0.0.2 - commit date 2024-01-28
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- pushed repo up to GitHub
- created README.md file for project

Version 0.0.1 - commit date 2024-01-28
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Decided to split Circulararray class out of datastructures, will make it its own
PyPI project. Got working with datastructures locally
