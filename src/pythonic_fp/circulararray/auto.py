# Copyright 2023-202 Geoffrey R. Scheller
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

"""Auto-resizing circular array.

- O(1) pops either end 
- O(1) amortized pushes either end 
- O(1) indexing, fully supports slicing
- Auto-resizing more storage capacity when necessary, manually compactable
- iterable, can safely mutate while iterators continue iterating over previous state
- comparisons compare identity before equality, like builtins
- in boolean context, falsy when empty, otherwise truthy

"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import cast, Never, overload, TypeVar

__all__ = ['CA', 'ca']

D = TypeVar('D')  # needed by Sphinx autodoc


class CA[D]():
    """Circular array data structure."""

    __slots__ = '_data', '_cnt', '_cap', '_front', '_rear'

    def __init__(
            self,
            data: Iterable[D] | None = None
        ) -> None:
        """
        .. code:: python

            CA[D](data: Iterable[D] | None)

        Initialize circular array with optional initial values.

        :param data: optional iterable to initial populate circular array
        :raises TypeError: if data is not Iterable

        """
        if data is None:
            self._data: list[D | None] = [None, None]
        else:
            self._data = [None] + list(data) + [None]
        self._cap = cap = len(self._data)
        self._cnt = cap - 2
        if cap == 2:
            self._front = 0
            self._rear = 1
        else:
            self._front = 1
            self._rear = cap - 2

    def _double_storage_capacity(self) -> None:
        if self._front <= self._rear:
            (
                    self._data,
                    self._cap,
            ) = (
                    self._data + [None] * self._cap,
                    self._cap * 2,
                )
        else:
            (
                    self._data,
                    self._front,
                    self._cap,
            ) = (
                    self._data[: self._front] + [None]*self._cap + self._data[self._front:],
                    self._front + self._cap,
                    2*self._cap,
                )

    def _compact_storage_capacity(self) -> None:
        match self._cnt:
            case 0:
                (
                        self._cap,
                        self._front,
                        self._rear,
                        self._data,
                ) = (
                        2,
                        0,
                        1,
                        [None, None],
                    )
            case 1:
                (
                        self._cap,
                        self._front,
                        self._rear,
                        self._data,
                ) = (
                        3,
                        1,
                        1,
                        [None, self._data[self._front], None],
                    )
            case _:
                if self._front <= self._rear:
                    ( 
                            self._cap,
                            self._front,
                            self._rear,
                            self._data,
                    ) = (
                            self._cnt + 2,
                            1,
                            self._cnt,
                            [None] + self._data[self._front : self._rear + 1] + [None],
                        )
                else:
                    (
                            self._cap,
                            self._front,
                            self._rear,
                            self._data,
                    ) = (
                            self._cnt + 2,
                            1,
                            self._cnt,
                            [None] + self._data[self._front :] + self._data[: self._rear + 1] + [None],
                        )

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
        return 'ca(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        return '(|' + ', '.join(map(str, self)) + '|)'

    def __bool__(self) -> bool:
        return self._cnt > 0

    def __len__(self) -> int:
        return self._cnt

    @overload
    def __getitem__(self, idx: int) -> D: ...
    @overload
    def __getitem__(self, idx: slice) -> CA[D]: ...

    def __getitem__(self, idx: int | slice) -> D | CA[D]:
        if isinstance(idx, slice):
            return CA(list(self)[idx])

        cnt = self._cnt
        if 0 <= idx < cnt:
            return cast(D, self._data[(self._front + idx) % self._cap])

        if -cnt <= idx < 0:
            return cast(D, self._data[(self._front + cnt + idx) % self._cap])

        if cnt == 0:
            msg0 = 'Trying to get a value from an empty CA.'
            raise IndexError(msg0)

        msg1 = 'Out of bounds: '
        msg2 = f'index = {idx} not between {-cnt} and {cnt - 1} '
        msg3 = 'while getting value from a CA.'
        raise IndexError(msg1 + msg2 + msg3)

    @overload
    def __setitem__(self, idx: int, vals: D) -> None: ...
    @overload
    def __setitem__(self, idx: slice, vals: Iterable[D]) -> None: ...

    def __setitem__(self, idx: int | slice, vals: D | Iterable[D]) -> None:
        if isinstance(idx, slice):
            if isinstance(vals, Iterable):
                data = list(self)
                data[idx] = vals
                _ca = CA(data)
                (
                        self._data,
                        self._cnt,
                        self._cap,
                        self._front,
                        self._rear,
                ) = (
                        _ca._data,
                        _ca._cnt,
                        _ca._cap,
                        _ca._front,
                        _ca._rear,
                    )
                return

            msg = 'must assign iterable to extended slice'
            raise TypeError(msg)

        cnt = self._cnt
        if 0 <= idx < cnt:
            self._data[(self._front + idx) % self._cap] = cast(D, vals)
        elif -cnt <= idx < 0:
            self._data[(self._front + cnt + idx) % self._cap] = cast(D, vals)
        else:
            if cnt < 1:
                msg0 = 'Trying to index into an empty CA.'
                raise IndexError(msg0)
            msg1 = 'Out of bounds: '
            msg2 = f'index = {idx} not between {-cnt} and {cnt - 1} '
            msg3 = 'while setting value from a CA.'
            raise IndexError(msg1 + msg2 + msg3)

    @overload
    def __delitem__(self, idx: int) -> None: ...
    @overload
    def __delitem__(self, idx: slice) -> None: ...

    def __delitem__(self, idx: int | slice) -> None:
        data = list(self)
        del data[idx]
        _ca = CA(data)
        (
                self._data,
                self._cnt,
                self._cap,
                self._front,
                self._rear,
        ) = (
                _ca._data,
                _ca._cnt,
                _ca._cap,
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

    def pushl(self, *data: D) -> None:
        """
        .. code:: python

            def pushl(self, *ds: D) -> None

        :param data: items pushed onto circular array from left

        """
        for d in data:
            if self._cnt == self._cap:
                self._double_storage_capacity()
            (
                    self._front,
                    self._data[self._front],
                    self._cnt,
            ) = (
                    (self._front - 1) % self._cap,
                    d,
                    self._cnt + 1,
                )

    def pushr(self, *data: D) -> None:
        """
        .. code:: python

            def pushr(self, *ds: D) -> None

        :param data: items pushed onto circular array from right

        """
        for d in data:
            if self._cnt == self._cap:
                self._double_storage_capacity()
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
        """
        .. code:: python

            def popl(self) -> D | Never

        :return: item popped from left side of circular array
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
            msg = 'Method popl called on an empty CA'
            raise ValueError(msg)
        return cast(D, d)

    def popr(self) -> D | Never:
        """
        .. code:: python

            def popr(self) -> D | Never

        :return: item popped from right side of circular array
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
            msg = 'Method popr called on an empty CA'
            raise ValueError(msg)
        return cast(D, d)

    def popld(self, default: D) -> D:
        """
        .. code:: python

            def popld(self, default: D) -> D

        Pop one item from left side of the circular array, provide
        a mandatory default value. "Safe" version of popl.

        :param default: item returned if circular array is empty
        :return: item popped from left side or default item if empty

        """
        try:
            return self.popl()
        except ValueError:
            return default

    def poprd(self, default: D) -> D:
        """
        .. code:: python

            def poprd(self, default: D) -> D

        Pop one item from right side of the circular array, provide
        a mandatory default value. "Safe" version of popr.

        :param default: item returned if circular array is empty
        :return: item popped from right side or default item if empty

        """
        try:
            return self.popr()
        except ValueError:
            return default

    def poplt(self, maximum: int) -> tuple[D, ...]:
        """
        .. code:: python

            def poplt(self, maximum: int) -> tuple[D, ...]

        Pop multiple items from left side of circular array.

        :param maximum: maximum number of values to pop
        :return: tuple of popped items in the order popped, left to right

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
        """
        .. code:: python

            def poprt(self, maximum: int) -> tuple[D, ...]

        Pop multiple items from right side of circular array.

        :param maximum: maximum number of items to pop
        :return: tuple of popped items in the order popped, right to left

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
        """
        .. code:: python

            def rotl(self, n: int) -> None

        Rotate items left.

        :param n: number of times to shift elements to the left

        """
        if self._cnt < 2:
            return
        for _ in range(n, 0, -1):
            self.pushr(self.popl())

    def rotr(self, n: int = 1) -> None:
        """
        .. code:: python

            def rotr(self, n: int) -> None

        Rotate items right.

        :param n: number of times to shift elements to the right

        """
        if self._cnt < 2:
            return
        for _ in range(n, 0, -1):
            self.pushl(self.popr())

    def map[U](self, f: Callable[[D], U]) -> CA[U]:
        """
        .. code:: python

            def map(self, f: Callable[[D], U]) -> CA[U]

        Apply function f over the circular array's contents,

        :param f: callable from type D to type U
        :return: new circular array instance

        """
        return CA(map(f, self))

    def foldl[L](self, f: Callable[[L, D], L], start: L | None = None) -> L | Never:
        """
        .. code:: python

            def foldl(self, f: Callable[[L, D], L], start: L | None) -> L | Never

        Fold left with a function and optional starting item.

        :param f: first argument to f is for the accumulator
        :param start: optional starting item
        :return: reduced value produced by the left fold
        :raises ValueError: when circular array empty and no starting item given

        """
        if self._cnt == 0:
            if start is None:
                msg = 'Method foldl called on an empty CA without a start item.'
                raise ValueError(msg)
            return start

        if start is None:
            acc = cast(L, self[0])  # in this case D = L
            for idx in range(1, self._cnt):
                acc = f(acc, self[idx])
            return acc

        acc = start
        for d in self:
            acc = f(acc, d)
        return acc

    def foldr[R](self, f: Callable[[D, R], R], start: R | None = None) -> R | Never:
        """
        .. code:: python

            def foldr(self, f: Callable[[D, R], R], start: R | None) -> R | Never

        Fold right with a function and an optional starting item.

        :param f: second argument to f is for the accumulator
        :param start: optional starting item
        :return: reduced value produced by the right fold
        :raises ValueError: when circular array empty and no starting item given

        """
        if self._cnt == 0:
            if start is None:
                msg = 'Method foldr called on empty CA without initial value.'
                raise ValueError(msg)
            return start

        if start is None:
            acc = cast(R, self[-1])  # in this case D = R
            for idx in range(self._cnt - 2, -1, -1):
                acc = f(self[idx], acc)
            return acc

        acc = start
        for d in reversed(self):
            acc = f(d, acc)
        return acc

    def capacity(self) -> int:
        """
        .. code:: python

            def capacity(self) -> int

        Return current storage capacity of the circular array.

        :return: current storage capacity

        """
        return self._cap

    def empty(self) -> None:
        """
        .. code:: python

            def empty(self) -> None

        Empty the circular array, keep current storage capacity.

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

        Find fraction of the storage capacity which is filled.

        :return: the ratio cnt/capacity

        """
        return self._cnt / self._cap

    def resize(self, minimum_capacity: int = 2) -> None:
        """
        .. code:: python

            def resize(self, minimum_capacity) -> None

        Compact circular array and, if necessary, resize to a minimum
        capacity. To just compact the circular array, do not provide
        a minimum capacity.

        :param minimum_capacity: minimum capacity to compact the circular array

        """
        self._compact_storage_capacity()
        if (min_cap := minimum_capacity) > self._cap:
            (
                    self._cap,
                    self._data,
            ) = (
                    min_cap,
                    self._data + [None] * (min_cap - self._cap),
                )
            if self._cnt == 0:
                self._front, self._rear = 0, self._cap - 1


def ca[T](*items: T) -> CA[T]:
    """
    .. code:: python

        def ca(*items: T) -> CA[T]

    Function to produce a circular array from a variable number of arguments.

    :param items: initial items for a new circular array
    :return: new auto-resizing circular array

    """
    return CA(items)
