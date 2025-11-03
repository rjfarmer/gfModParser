# SPDX-License-Identifier: GPL-2.0+

import numpy as np
from packaging.version import Version
from functools import cached_property

from . import expressions


class arrayspec:
    def __init__(self, array, *, version: Version) -> None:
        self._array = array
        self.version = version

    def __bool__(self) -> bool:
        return self.is_array

    @property
    def is_array(self) -> bool:
        return len(self._array) > 0

    @property
    def ndims(self) -> int:
        if self.is_array:
            return self.rank
        return -1

    @property
    def rank(self) -> int:
        if self.is_array:
            return int(self._array[0])
        return -1

    @property
    def corank(self) -> int:
        if self.is_array:
            return int(self._array[1])
        return -1

    @property
    def type(self) -> str:
        if self.is_array:
            return self._array[2]
        return ""

    @property
    def is_deferred(self) -> bool:
        """
        Deferred arrays (like allocatable) do not have compile time bounds, but do have
        compile time rank
        """
        if self.is_array:
            return self.type == "DEFERRED" or self.type == "ASSUMED_SHAPE"
        return False

    @property
    def is_explicit(self) -> bool:
        if self.is_array:
            return self.type == "EXPLICIT"
        return False

    @cached_property
    def lower(self) -> tuple[expressions.Expression, ...]:
        low = []
        if self.is_array:
            for i in range(self.rank + self.corank):
                if len(self._array[3 + i * 2]):
                    low.append(
                        expressions.Expression(
                            self._array[3 + i * 2], version=self.version
                        )
                    )

            return tuple(low)
        return ()

    @cached_property
    def upper(self) -> tuple[expressions.Expression, ...]:
        up = []
        if self.is_array:
            for i in range(self.rank + self.corank):
                if len(self._array[4 + i * 2]):
                    up.append(
                        expressions.Expression(
                            self._array[4 + i * 2], version=self.version
                        )
                    )

            return tuple(up)
        return ()

    @property
    def fshape(self) -> tuple[tuple[int, int], ...]:
        """
        Returns the array shape as a tuple of Fortran bounds ((lower, upper),..)
        """
        if self.is_array:
            res = []
            for l, u in zip(self.lower, self.upper):
                res.append((l.value, u.value))

            return tuple(res)
        return ()

    @property
    def pyshape(self) -> tuple[int, ...]:
        """
        Returns the array shape as a tuple of Python bounds (ndim1,ndim2,..)
        """
        if self.is_array:
            res = []
            for l, u in zip(self.lower, self.upper):
                res.append(u.value - l.value + 1)

            return tuple(res)
        return ()

    @property
    def size(self) -> np.int64:
        if self.is_array:
            if not self.is_deferred:
                return np.prod(self.pyshape)

        return np.int64(-1)
