# Copyright 2024-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Modules implementing stateful circular array data structures.

Module **pythonic_fp.circulararray.auto**

``CA`` objects automatically increase their total storage capacity as
needed. They can be manually resized smaller.

- class ``CA``
- factory function ``ca``

Module **pythonic_fp.circulararray.fixed**

The total capacity of ``CAF`` objects is fixed at object instantiation.

- class ``CAF``
- factory function ``caf``

"""

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
