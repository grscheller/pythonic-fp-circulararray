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

"""Pythonic FP - Circular Array

Modules implementing stateful circular array data structures.

**Module: pythonic_fp.circulararray.resizing**

- Class CA

  - O(1) pops either end 
  - O(1) amortized pushes either end 
  - O(1) indexing, fully supports slicing
  - Auto-resizing larger when necessary, manually compatible
  - iterable, can safely mutate while iterators continue iterating over previous state
  - comparisons compare identity before equality, like builtins
  - in boolean context returns true when not empty, false when empty

**Module: pythonic_fp.circulararray.fixed_capacity**

- Class CAFix

  - O(1) pops and pushes either end 
  - O(1) indexing, does not support slicing
  - fixed size
  - iterable, can safely mutate while iterators continue iterating over previous state
  - comparisons compare identity before equality, like builtins
  - in boolean context returns false when either empty or full, otherwise true

"""

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
