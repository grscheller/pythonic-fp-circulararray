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

"""Fixed Capacity Circular Array

- O(1) pops and pushes either end 
- O(1) indexing, does not support slicing
- fixed capacity
- iterable, can safely mutate while iterators continue iterating over previous state
- comparisons compare identity before equality, like builtins
- in boolean context returns false when either empty or full, otherwise true

"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import cast, Final, Never, TypeVar

__all__ = ['CAF', 'caf']

D = TypeVar('D')  # needed by Sphinx autodoc


class CAF[D]():
    """Fixed sized circular array data structure."""

    __slots__ = '_data', '_cnt', '_cap', '_front', '_rear'

    def __init__(
            self,
            data: Iterable[D] | None = None,
            capacity: int = 2
        ) -> None:
        """Initialize fixed sized circular.

        .. code:: python

            CA[D](data: Iterable[D] | None, capacity: int = 2)

        :param ds: optional iterable to initial populate circular array.
        :raises TypeError: if ds is not Iterable.

        """
        capacity = max(2, capacity)
        if data is None:
            self._data: list[D | None] = [None]*capacity
            count = 0
        else:
            ds: list[D | None] = list(data)
            count = len(ds)
            capacity = max(count, capacity)
            self._data = ds + [None]*(capacity - count)
        self._cap: Final[int] = capacity
        self._cnt = count
        if count == 0:
            self._front = 0
            self._rear = capacity - 1
        else:
            self._front = 0
            self._rear = count - 1

    def __iter__(self) -> Iterator[D]:
        if self._cnt > 0:
            (
                    capacity,
                    rear,
                    position,
                    current_state,
            ) = (
                    self._cap,
                    self._rear,
                    self._front,
                    self._data.copy(),
                )

            while position != rear:
                yield cast(D, current_state[position])
                position = (position + 1) % capacity
            yield cast(D, current_state[position])

    def __reversed__(self) -> Iterator[D]:
        if self._cnt > 0:
            (
                    capacity,
                    front,
                    position,
                    current_state,
            ) = (
                    self._cap,
                    self._front,
                    self._rear,
                    self._data.copy(),
                )

            while position != front:
                yield cast(D, current_state[position])
                position = (position - 1) % capacity
            yield cast(D, current_state[position])

    def __repr__(self) -> str:
        return 'caf(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        return '(|' + ', '.join(map(str, self)) + '|)'

    def __bool__(self) -> bool:
        return 0 < self._cnt < self._cap

    def __len__(self) -> int:
        return self._cnt

    def __getitem__(self, idx: int) -> D:
        cnt = self._cnt
        if 0 <= idx < cnt:
            return cast(D, self._data[(self._front + idx) % self._cap])

        if -cnt <= idx < 0:
            return cast(D, self._data[(self._front + cnt + idx) % self._cap])

        if cnt == 0:
            msg0 = 'Trying to get a value from an empty CAF.'
            raise IndexError(msg0)

        msg1 = 'Out of bounds: '
        msg2 = f'index = {idx} not between {-cnt} and {cnt - 1} '
        msg3 = 'while getting value from a CAF.'
        raise IndexError(msg1 + msg2 + msg3)

    def __setitem__(self, idx: int, val: D) -> None:
        cnt = self._cnt
        if 0 <= idx < cnt:
            self._data[(self._front + idx) % self._cap] = val
        elif -cnt <= idx < 0:
            self._data[(self._front + cnt + idx) % self._cap] = val
        else:
            if cnt < 1:
                msg0 = 'Trying to index into an empty CAF.'
                raise IndexError(msg0)
            msg1 = 'Out of bounds: '
            msg2 = f'index = {idx} not between {-cnt} and {cnt - 1} '
            msg3 = 'while setting value from a CAF.'
            raise IndexError(msg1 + msg2 + msg3)

    def __delitem__(self, idx: int) -> None:
        data = list(self)
        del data[idx]
        _ca = CAF(data, self._cap)
        (
                self._data,
                self._cnt,
                self._front,
                self._rear,
        ) = (
                _ca._data,
                _ca._cnt,
                _ca._front,
                _ca._rear,
            )

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False

        (
                front1,
                count1,
                capacity1,
                front2,
                count2,
                capacity2,
        ) = (
                self._front,
                self._cnt,
                self._cap,
                other._front,
                other._cnt,
                other._cap,
            )

        if count1 != count2:
            return False

        for nn in range(count1):
            if self._data[(front1 + nn) % capacity1] is other._data[(front2 + nn) % capacity2]:
                continue
            if self._data[(front1 + nn) % capacity1] != other._data[(front2 + nn) % capacity2]:
                return False
        return True

    def pushl(self, d: D) -> None:
        """Push left.

        .. code:: python

            def pushl(self, d: D) -> None

        :param d: data pushed onto circular array from left
        :raises ValueError: when called on a full CAF

        """
        if self._cnt == self._cap:
            msg = 'Method pushl called on a full CAF'
            raise ValueError(msg)

        (
                self._front,
                self._data[self._front],
                self._cnt,
        ) = (
                (self._front - 1) % self._cap,
                d,
                self._cnt + 1,
            )

    def pushr(self, d: D) -> None:
        """Push right.

        .. code:: python

            def pushr(self, d: D) -> None

        :param d data item to push onto circular array from right
        :raises ValueError: when called on a full CAF.

        """
        if self._cnt == self._cap:
            msg = 'Method pushr called on a full CAF'
            raise ValueError(msg)

        (
                self._rear,
                self._data[self._rear],
                self._cnt,
        ) = (
                (self._rear + 1) % self._cap,
                d,
                self._cnt + 1,
            )

    def popl(self) -> D | Never:
        """Pop left.

        .. code:: python

            def popl(self) -> D | Never

        :return: value popped from left side of circular array
        :raises ValueError: when called on an empty circular array

        """
        if self._cnt > 1:
            (
                    d,
                    self._data[self._front],
                    self._front,
                    self._cnt,
            ) = (
                    self._data[self._front],
                    None,
                    (self._front + 1) % self._cap,
                    self._cnt - 1,
                )
        elif self._cnt == 1:
            (
                    d,
                    self._data[self._front],
                    self._cnt,
                    self._front,
                    self._rear,
            ) = (
                    self._data[self._front],
                    None,
                    0,
                    0,
                    self._cap - 1,
                )
        else:
            msg = 'Method popl called on an empty CAF'
            raise ValueError(msg)
        return cast(D, d)

    def popr(self) -> D | Never:
        """Pop right.

        .. code:: python

            def popr(self) -> D | Never

        :return: value popped from right side of circular array
        :raises ValueError: when called on an empty circular array

        """
        if self._cnt > 1:
            (
                    d,
                    self._data[self._rear],
                    self._rear,
                    self._cnt,
            ) = (
                    self._data[self._rear],
                    None,
                    (self._rear - 1) % self._cap,
                    self._cnt - 1,
                )
        elif self._cnt == 1:
            (
                    d,
                    self._data[self._front],
                    self._cnt,
                    self._front,
                    self._rear,
            ) = (
                    self._data[self._front],
                    None,
                    0,
                    0,
                    self._cap - 1,
                )
        else:
            msg = 'Method popr called on an empty CAF'
            raise ValueError(msg)
        return cast(D, d)

    def popld(self, default: D) -> D:
        """Pop one value from left side of the circular array, provide a
        mandatory default value. "Safe" version of popl.

        .. code:: python

            def popld(self, default: D) -> D

        :param default: value returned if circular array is empty
        :return: value popped from left side

        """
        try:
            return self.popl()
        except ValueError:
            return default

    def poprd(self, default: D) -> D:
        """Pop one value from right side of the circular array, provide a
        mandatory default value. "Safe" version of popr.

        .. code:: python

            def poprd(self, default: D) -> D

        :param default: value returned if circular array is empty
        :return: value popped from right side

        """
        try:
            return self.popr()
        except ValueError:
            return default

    def poplt(self, maximum: int) -> tuple[D, ...]:
        """Pop multiple values from left side of circular array.

        .. code:: python

            def poplt(self, maximum: int) -> tuple[D, ...]

        :param maximum: maximum number of values to be popped
        :return: tuple of popped values in the order popped, left to right

        """
        ds: list[D] = []

        while maximum > 0:
            try:
                ds.append(self.popl())
            except ValueError:
                break
            else:
                maximum -= 1

        return tuple(ds)

    def poprt(self, maximum: int) -> tuple[D, ...]:
        """Pop multiple values from right side of circular array.

        .. code:: python

            def poprt(self, maximum: int) -> tuple[D, ...]

        :param maximum: maximum number of values to be popped
        :return: tuple of popped values in the order popped, right to left

        """
        ds: list[D] = []
        while maximum > 0:
            try:
                ds.append(self.popr())
            except ValueError:
                break
            else:
                maximum -= 1
        return tuple(ds)

    def rotl(self, n: int = 1) -> None:
        """Rotate circular array elements left.

        .. code:: python

            def rotl(self, n: int) -> None

        :param n: number of times to shift elements to the left

        """
        if self._cnt < 2:
            return
        for _ in range(n, 0, -1):
            self.pushr(self.popl())

    def rotr(self, n: int = 1) -> None:
        """Rotate circular array elements right.

        .. code:: python

            def rotr(self, n: int) -> None

        :param n: number of times to shift elements to the right

        """
        if self._cnt < 2:
            return
        for _ in range(n, 0, -1):
            self.pushl(self.popr())

    def map[U](self, f: Callable[[D], U]) -> CAF[U]:
        """Apply function f over the fixed circular array's contents,

        .. code:: python

            def map(self, f: Callable[[D], U]) -> CAF[U]

        :param f: function from type D to type U
        :return: new fixed circular array instance

        """
        return CAF(map(f, self), self._cap)

    def foldl[L](self, f: Callable[[L, D], L], initial: L | None = None) -> L:
        """Fold left with a function and optional initial value.

        .. code:: python

            def foldl(self, f: Callable[[L, D], L], initial: L | None) -> L | None

        :param f: first argument to f is for the accumulated value
        :param initial: optional initial value
        :raises ValueError: when circular array empty and no initial value given

        """
        if self._cnt == 0:
            if initial is None:
                msg = 'Method foldl called on an empty CAF without an initial value.'
                raise ValueError(msg)
            return initial

        if initial is None:
            acc = cast(L, self[0])  # in this case D = L
            for idx in range(1, self._cnt):
                acc = f(acc, self[idx])
            return acc

        acc = initial
        for d in self:
            acc = f(acc, d)
        return acc

    def foldr[R](self, f: Callable[[D, R], R], initial: R | None = None) -> R:
        """Fold right with a function and an optional initial value.

        .. code:: python

            def foldr(self, f: Callable[[D, R], R], initial: R | None) -> L | None

        :param f: second argument to `f` is for the accumulated value
        :param initial: optional initial value
        :raises ValueError: when circular array empty and no initial value given

        """
        if self._cnt == 0:
            if initial is None:
                msg = 'Method foldr called on empty CAF without initial value.'
                raise ValueError(msg)
            return initial

        if initial is None:
            acc = cast(R, self[-1])  # in this case D = R
            for idx in range(self._cnt - 2, -1, -1):
                acc = f(self[idx], acc)
            return acc

        acc = initial
        for d in reversed(self):
            acc = f(d, acc)
        return acc

    def capacity(self) -> int:
        """Return the capacity of the fixed circular array.

        .. code:: python

            def capacity(self) -> int

        :return: current capacity of the fixed circular array

        """
        return self._cap

    def empty(self) -> None:
        """Empty the circular array, keep current capacity.

        .. code:: python

            def empty(self) -> None

        """
        (
                self._data,
                self._front,
                self._rear,
                self._cnt,
        ) = (
                [None] * self._cap,
                0,
                self._cap - 1,
                0,
            )

    def fraction_filled(self) -> float:
        """
        .. code:: python

            def fraction_filled(self) -> float

        Find fraction of capacity filled.

        :return: the ratio count/capacity

        """
        return self._cnt / self._cap


def caf[T](*ts: T, capacity: int = 2) -> CAF[T]:
    """
    .. code:: python

        def caf(*ts: T) -> CAF[T]

    Function to produce a circular array from a variable number of arguments.

    :param ts: initial values for the new circular array

    """
    return CAF(ts, capacity = capacity)
