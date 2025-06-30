Pythonic FP - Circular Array
============================

PyPI project `pythonic.circular-array <https://pypi.org/project/pythonic-fp.circulararray/>`_
implements a stateful circular array data structure.

- O(1) pops either end 
- O(1) amortized pushes either end 
- O(1) indexing, fully supports slicing
- Auto-resizing larger when necessary, manually compatible
- Iterable, can safely mutate while iterators continue iterating over previous state

This PyPI project is part of of the grscheller
`pythonic-fp namespace projects <https://grscheller.github.io/pythonic-fp/>`_.

Copyright and License
---------------------

Copyright (c) 2023-2025 Geoffrey R. Scheller

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

`http://www.apache.org/licenses/LICENSE-2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
