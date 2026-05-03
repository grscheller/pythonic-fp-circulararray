# Copyright 2023-2026 Geoffrey R. Scheller
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

from collections.abc import Callable, Iterable, Iterator
from typing import cast, Final, overload
from pythonic_fp.gadgets.sentinels.novalue import NoValue

__all__ = ['CAF', 'caf']

nada: Final[NoValue] = NoValue()


class CAF[X]:

    """
    .. admonition:: Fixed storage capacity circular array CAF

        - O(1) pops and pushes either end
        - O(1) indexing, does not support slicing
        - fixed total storage capacity
        - iterable but not threadsafe
        - comparisons compare identity before equality, like builtins
        - in boolean context, falsy when either empty or full, otherwise truthy
        - function ``caf`` produces fixed capacity circular array from arguments

    """
    __slots__ = '_xs', '_cnt', '_cap', '_front', '_rear'

    def __init__(self, *xs: Iterable[X], cap: int = 2) -> None:
        """
        :param xs: Takes 0 or 1 iterable parameters to initially
                   populate the ``CAF`` left (front) to right (back).
        :param cap: Minimum fixed storage capacity of circular array.
        :raises ValueError: When more than one iterable is provided.
        :raises TypeError: When passed a non-iterable positional parameter.

        """
        cap = max(2, cap)
        if (size := len(xs)) > 1:
            msg = f'CAF expects at most 1 iterable, got {size}'
            raise ValueError(msg)
        if size:
            values: list[X | NoValue] = list(cast(Iterable[X | NoValue], xs[0]))
            cnt = len(values)
            cap = max(cnt, cap)
            self._xs = values + [nada] * (cap - cnt)
        else:
            self._xs = [nada] * cap
            cnt = 0
        self._cap: Final[int] = cap
        self._cnt = cnt
        if cnt == 0:
            self._front = 0
            self._rear = cap - 1
        else:
            self._front = 0
            self._rear = cnt - 1

    def __bool__(self) -> bool:
        return 0 < self._cnt < self._cap

    def __len__(self) -> int:
        return self._cnt

    def __eq__(self, other: object) -> bool:
        """
        .. admonition:: Equality comparison

            Efficiently compare ``CAF`` to another object.

        :param other: The object to be compared.
        :returns: ``True`` if ``other`` is another ``CAF`` whose
                  contents compare as equal to the corresponding
                  contents of the ``CAF``, otherwise ``False``.

        """
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False

        (
            front1,
            cnt1,
            cap1,
            front2,
            cnt2,
            cap2,
        ) = (
            self._front,
            self._cnt,
            self._cap,
            other._front,
            other._cnt,
            other._cap,
        )

        if cnt1 != cnt2:
            return False

        for nn in range(cnt1):
            if (
                self._xs[(front1 + nn) % cap1]
                is other._xs[(front2 + nn) % cap2]
            ):
                continue
            if (
                self._xs[(front1 + nn) % cap1]
                != other._xs[(front2 + nn) % cap2]
            ):
                return False
        return True

    def __iter__(self) -> Iterator[X]:
        if self._cnt > 0:
            (
                cap,
                rear,
                position,
                current_state,
            ) = (
                self._cap,
                self._rear,
                self._front,
                self._xs.copy(),
            )

            while position != rear:
                yield cast(X, current_state[position])
                position = (position + 1) % cap
            yield cast(X, current_state[position])

    def __reversed__(self) -> Iterator[X]:
        if self._cnt > 0:
            (
                cap,
                front,
                position,
                current_state,
            ) = (
                self._cap,
                self._front,
                self._rear,
                self._xs.copy(),
            )

            while position != front:
                yield cast(X, current_state[position])
                position = (position - 1) % cap
            yield cast(X, current_state[position])

    def __getitem__(self, idx: int) -> X:
        cnt = self._cnt
        if 0 <= idx < cnt:
            return cast(X, self._xs[(self._front + idx) % self._cap])

        if -cnt <= idx < 0:
            return cast(X, self._xs[(self._front + cnt + idx) % self._cap])

        if cnt == 0:
            msg0 = 'Trying to get a value from an empty CAF.'
            raise IndexError(msg0)

        msg1 = 'Out of bounds: '
        msg2 = f'index = {idx} not between {-cnt} and {cnt - 1} '
        msg3 = 'while getting value from a CAF.'
        raise IndexError(msg1 + msg2 + msg3)

    def __setitem__(self, idx: int, val: X) -> None:
        cnt = self._cnt
        if 0 <= idx < cnt:
            self._xs[(self._front + idx) % self._cap] = val
        elif -cnt <= idx < 0:
            self._xs[(self._front + cnt + idx) % self._cap] = val
        else:
            if cnt < 1:
                msg0 = 'Trying to index into an empty CAF.'
                raise IndexError(msg0)
            msg1 = 'Out of bounds: '
            msg2 = f'index = {idx} not between {-cnt} and {cnt - 1} '
            msg3 = 'while setting value from a CAF.'
            raise IndexError(msg1 + msg2 + msg3)

    def __delitem__(self, idx: int) -> None:
        item_list = list(self)
        del item_list[idx]
        _ca = CAF(item_list, cap = self._cap)
        (
            self._xs,
            self._cnt,
            self._front,
            self._rear,
        ) = (
            _ca._xs,
            _ca._cnt,
            _ca._front,
            _ca._rear,
        )
        del _ca

    def __repr__(self) -> str:
        """
        .. admonition:: String representation

            Construct a string to reproduce the ``CAF``. 

        :returns: The string 'CAF(repr(x1), repr(x2), ..., repr(xn))'
                  where x1, x2, ..., xn are the circular array's
                  contents.

        """
        return 'caf(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        """
        .. admonition:: User string

            Construct a string meaningful to an end user.

        :returns: The string '(|x1, x2, ..., xn|)'
                  where x1, x2, ..., xn are the circular array's
                  contents.

        """
        return '(|' + ', '.join(map(str, self)) + '|)'

    def pushl(self, x: X) -> None:
        """
        .. admonition:: Push left

            Push single item from the left onto the ``CAF``.

        :param x: Single item to be pushed onto the front of the circular array from the left.
        :raises ValueError: When called on a full fixed storage capacity circular array.

        """
        if self._cnt == self._cap:
            msg = 'Method pushl called on a full CAF'
            raise ValueError(msg)

        (
            self._front,
            self._xs[self._front],
            self._cnt,
        ) = (
            (self._front - 1) % self._cap,
            x,
            self._cnt + 1,
        )

    def pushr(self, x: X) -> None:
        """
        .. admonition:: Push right

            Push single item from the right onto the ``CAF``.

        :param x: Single item to be pushed onto the rear of the circular array from the right.
        :raises ValueError: When called on a full fixed storage capacity circular array.

        """
        if self._cnt == self._cap:
            msg = 'Method pushr called on a full CAF'
            raise ValueError(msg)

        (
            self._rear,
            self._xs[self._rear],
            self._cnt,
        ) = (
            (self._rear + 1) % self._cap,
            x,
            self._cnt + 1,
        )

    def popl(self) -> X:
        """
        .. admonition:: Pop left

            Pop a single items off the left side of the ``CAF``.

        :returns: Item popped from left side (front) of circular array.
        :raises ValueError: When called on an empty circular array.

        """
        if self._cnt > 1:
            (
                x,
                self._xs[self._front],
                self._front,
                self._cnt,
            ) = (
                self._xs[self._front],
                nada,
                (self._front + 1) % self._cap,
                self._cnt - 1,
            )
        elif self._cnt == 1:
            (
                x,
                self._xs[self._front],
                self._cnt,
                self._front,
                self._rear,
            ) = (
                self._xs[self._front],
                nada,
                0,
                0,
                self._cap - 1,
            )
        else:
            msg = 'Method popl called on an empty CAF'
            raise ValueError(msg)
        return cast(X, x)

    def popr(self) -> X:
        """
        .. admonition:: Pop right

            Pop a single items off the right side of the ``CAF``.

        :returns: Item popped from right side (rear) of circular array.
        :raises ValueError: When called on an empty circular array.

        """
        if self._cnt > 1:
            (
                x,
                self._xs[self._rear],
                self._rear,
                self._cnt,
            ) = (
                self._xs[self._rear],
                nada,
                (self._rear - 1) % self._cap,
                self._cnt - 1,
            )
        elif self._cnt == 1:
            (
                x,
                self._xs[self._front],
                self._cnt,
                self._front,
                self._rear,
            ) = (
                self._xs[self._front],
                nada,
                0,
                0,
                self._cap - 1,
            )
        else:
            msg = 'Method popr called on an empty CAF'
            raise ValueError(msg)
        return cast(X, x)

    def popld(self, default: X) -> X:
        """
        .. admonition:: Pop Left with default

            Pop a single items off the left side of the ``CAF``.

        :param default: Default value to return if ``CAF`` is empty.
        :returns: Item popped from left side (front) of circular array
                  if not empty, otherwise return the provided default
                  value.

        """
        try:
            return self.popl()
        except ValueError:
            return default

    def poprd(self, default: X) -> X:
        """
        .. admonition:: Pop Right with default

            Pop a single items off the right side of the ``CAF``.

        :param default: Default value to return if ``CAF`` is empty.
        :returns: Item popped from right side (rear) of circular array
                  if not empty, otherwise return the provided default
                  value.

        """
        try:
            return self.popr()
        except ValueError:
            return default

    def poplt(self, maximum: int) -> tuple[X, ...]:
        """
        .. admonition:: Pop multiple items from left

            Pop items off the left side of the ``CAF``.

        :param maximum: Maximum number of items to pop, may pop less if not enough items in ``CAF``.
        :returns: A ``tuple`` of the items popped, left to right.

        """
        xs: list[X] = []

        while maximum > 0:
            try:
                xs.append(self.popl())
            except ValueError:
                break
            else:
                maximum -= 1

        return tuple(xs)

    def poprt(self, maximum: int) -> tuple[X, ...]:
        """
        .. admonition:: Pop multiple items from right

            Pop items off the right side of the ``CAF``.

        :param maximum: Maximum number of items to pop, may pop less if not enough items in ``CAF``.
        :returns: A ``tuple`` of the items popped, right to left.

        """
        xs: list[X] = []
        while maximum > 0:
            try:
                xs.append(self.popr())
            except ValueError:
                break
            else:
                maximum -= 1
        return tuple(xs)

    def rotl(self, n: int = 1) -> None:
        """
        .. admonition:: Rotate left

            Rotate contents of ``CAF`` to the left putting first
            item onto rear.

        :param n: Number of times to shift items left. Default 1 time.

        """
        if self._cnt < 2:
            return
        for _ in range(n, 0, -1):
            self.pushr(self.popl())

    def rotr(self, n: int = 1) -> None:
        """
        .. admonition:: Rotate right

            Rotate contents of ``CAF`` to the right putting last
            item onto front.

        :param n: Number of times to shift items right. Default 1 time.

        """
        if self._cnt < 2:
            return
        for _ in range(n, 0, -1):
            self.pushl(self.popr())

    def map[Y](self, f: Callable[[X], Y]) -> 'CAF[Y]':
        """
        .. admonition:: Map function over the CAF

            Apply function ``f`` over the circular array's contents.

        :param f: Callable from type ``X`` to type ``Y``.
        :returns: New fixed capacity circular array instance.

        """
        return CAF(map(f, self), cap = self._cap)

    @overload
    def foldl[L](self, f: Callable[[X, X], X]) -> X: ...
    @overload
    def foldl[L](self, f: Callable[[L, X], L], start: L) -> L: ...

    def foldl[L](self, f: Callable[[L, X], L], start: L | NoValue = nada) -> L:
        """
        .. admonition:: Fold left

            Fold ``CAF`` left with a function and optional starting item.

        :param f: Folding function, first argument to ``f`` is for the accumulator.
        :param start: Optional starting item.
        :returns: Reduced value produced by the left fold.
        :raises ValueError: When circular array empty and ``start`` not given.

        """
        if self._cnt == 0:
            if start is nada:
                msg = 'Method foldl called on an empty CAF without a start item.'
                raise ValueError(msg)
            return cast(L, start)

        if start is nada:
            acc = cast(L, self[0])  # in this case D = L
            for idx in range(1, self._cnt):
                acc = f(acc, self[idx])
            return acc

        acc = cast(L, start)
        for x in self:
            acc = f(acc, x)
        return acc

    @overload
    def foldr[R](self, f: Callable[[X, X], X]) -> X: ...
    @overload
    def foldr[R](self, f: Callable[[X, R], R], start: R) -> R: ...

    def foldr[R](self, f: Callable[[X, R], R], start: R | NoValue = nada) -> R:
        """
        .. admonition:: Fold right

            Fold ``CAF`` right left with a function and optional starting item.

        :param f: Folding function, second argument to ``f`` is for the accumulator.
        :param start: Optional starting item.
        :returns: Reduced value produced by the right fold.
        :raises ValueError: When circular array empty and ``start`` not given.

        """
        if self._cnt == 0:
            if start is nada:
                msg = 'Method foldr called on empty CAF without initial value.'
                raise ValueError(msg)
            return cast(R, start)

        if start is nada:
            acc = cast(R, self[-1])  # in this case D = R
            for idx in range(self._cnt - 2, -1, -1):
                acc = f(self[idx], acc)
            return acc

        acc = cast(R, start)
        for x in reversed(self):
            acc = f(x, acc)
        return acc

    def capacity(self) -> int:
        """
        .. admonition:: Get capacity

            Get the fixed storage capacity of the circular array.


        :returns: Fixed storage capacity.

        """
        return self._cap

    def empty(self) -> None:
        """
        .. admonition:: Empty circular array

            Empty the circular array, keep current storage capacity.

        """
        (
            self._xs,
            self._front,
            self._rear,
            self._cnt,
        ) = (
            [nada] * self._cap,
            0,
            self._cap - 1,
            0,
        )

    def fraction_filled(self) -> float:
        """
        .. admonition:: Get fraction filled

            Find fraction of the storage capacity which is filled.

        :returns: The ratio count/capacity.

        """
        return self._cnt / self._cap


def caf[T](*ts: T, cap: int = 2) -> CAF[T]:
    """
    .. admonition:: Circular array factory function

        Produce a circular array from a variable number of arguments.

    :param ts: Initial items for a new fixed capacity circular array.
    :param cap: The minimum storage capacity to set.
    :returns: New fixed storage capacity circular array.

    """
    return CAF(ts, cap=cap)
