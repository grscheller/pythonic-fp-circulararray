..
   Pythonic FP - Circular Array documentation master file. To regenerate the sphinx
   documentation do: ``$ make html`` from the ``docs/`` directory.

Pythonic FP - Circular Array
============================

PyPI project
`pythonic.circular-array <https://pypi.org/project/pythonic-fp.circulararray/>`_
implements a full featured, generic, stateful circular array data structure.

- O(1) amortized pushes and pops either end 
- O(1) indexing
- Auto-resizing larger when necessary, can be manually compacted if desired
- Iterable, can safely be mutated while iterators continue iterating over previous state
- Fully supports slicing

Part of of the
`pythonic-fp namespace projects <https://github.com/grscheller/pythonic-fp/blob/main/README.md>`_.

Documentation
-------------

:doc:`installing`
    Installing and importing the module.

:doc:`api_pypi`
    PyPI release documentation.

Development
-----------

:doc:`Current Development API <api_devel>`
    Development environment API documentation.

:doc:`changelog`
    For the current and predecessor projects.

.. toctree::
   :caption: Documentation
   :maxdepth: 2
   :hidden:

   installing
   api_pypi
   api_devel

.. toctree::
   :caption: Development
   :maxdepth: 1
   :hidden:

   changelog

.. toctree::
   :caption: Back to start
   :maxdepth: 1
   :hidden:

   self
