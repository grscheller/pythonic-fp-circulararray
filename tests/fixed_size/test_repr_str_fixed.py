# Copyright 2023-2025 Geoffrey R. Scheller
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

from __future__ import annotations

from pythonic_fp.circulararray.fixed_capacity import ca_fix, CAFix

class TestReprFixed:
    """Functionality testing"""
    def test_repr(self) -> None:
        """Functionality test"""
        ca0: CAFix[int] = CAFix()
        assert repr(ca0) == 'ca_fix()'
        foo: CAFix[int] = eval('ca_fix()')
        bar: CAFix[int] = eval(repr(ca0))
        assert foo == bar

        ca1: CAFix[str|int] = CAFix(capacity=10)
        assert repr(ca1) == 'ca_fix()'
        ca2: CAFix[int|str] = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        ca1.pushr(1)
        ca1.pushl('foo')
        assert repr(ca1) == "ca_fix('foo', 1)"
        ca2 = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        assert ca1.popld('bar') == 'foo'
        ca1.pushr(2)
        ca1.pushr(3)
        ca1.pushr(4)
        ca1.pushr(5)
        assert ca1.popl() == 1
        ca1.pushl(42)
        ca1.popr()
        assert repr(ca1) == 'ca_fix(42, 2, 3, 4)'
        ca2 = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        ca3: CAFix[int] = ca_fix(1, 10, 0, 42, capacity=10)
        ca3.pushr(2)
        ca3.pushr(100)
        ca3.pushr(3)
        assert ca3.popl() == 1
        assert ca3.popr() == 3
        ca3.pushl(9)
        ca3.pushl(8)
        assert ca3.poprt(2) == (100, 2)
        ca3.pushr(1)
        ca3.pushr(2)
        ca3.pushr(3)
        assert repr(ca3) == 'ca_fix(8, 9, 10, 0, 42, 1, 2, 3)'

        ca4: CAFix[int] = CAFix([1, 10, 0, 42], capacity=100)
        ca4.pushr(2)
        ca4.pushr(100)
        ca4.pushr(3)
        assert ca4.popl() == 1
        assert ca4.popr() == 3
        ca4.pushl(9)
        ca4.pushl(8)
        assert ca4.poprt(2) == (100, 2)
        ca4.pushr(1)
        ca4.pushr(2)
        ca4.pushr(3)
        assert repr(ca4) == 'ca_fix(8, 9, 10, 0, 42, 1, 2, 3)'
