# SPDX-License-Identifier: GPL-2.0+

import numpy as np

from . import expressions


class arrayspec:
    def __init__(self, array, *, version):
        self._array = array
        self.version = version

        self._low = []
        self._up = []

    def __bool__(self):
        return self.is_array

    @property
    def is_array(self):
        return len(self._array) > 0

    @property
    def ndims(self):
        if self.is_array:
            return self.rank

    @property
    def rank(self):
        if self.is_array:
            return int(self._array[0])

    @property
    def corank(self):
        if self.is_array:
            return int(self._array[1])

    @property
    def type(self):
        if self.is_array:
            return self._array[2]

    @property
    def is_defered(self):
        """
        Defered arrays (like allocatable) do not have compile time bounds, but do have
        compile time rank
        """
        if self.is_array:
            return self.type == "DEFERRED"

    @property
    def lower(self):
        if self.is_array:
            if len(self._low) == 0:
                for i in range(self.rank + self.corank):
                    if len(self._array[3 + i * 2]):
                        self._low.append(
                            expressions.Expression(
                                self._array[3 + i * 2], version=self.version
                            )
                        )

            return self._low

    @property
    def upper(self):
        if self.is_array:
            if len(self._up) == 0:
                for i in range(self.rank + self.corank):
                    if len(self._array[4 + i * 2]):
                        self._up.append(
                            expressions.Expression(
                                self._array[4 + i * 2], version=self.version
                            )
                        )

            return self._up

    @property
    def fshape(self):
        """
        Returns the array shape as a tuple of Fortran bounds ((lower, upper),..)
        """
        if self.is_array:
            res = []
            for l, u in zip(self.lower, self.upper):
                res.append((l.value, u.value))

            return tuple(res)

    @property
    def pyshape(self):
        """
        Returns the array shape as a tuple of Python bounds (ndim1,ndim2,..)
        """
        if self.is_array:
            res = []
            for l, u in zip(self.lower, self.upper):
                res.append(u.value - l.value + 1)

            return tuple(res)

    @property
    def size(self):
        if self.is_array:
            if not self.is_defered:
                return np.prod(self.pyshape)
