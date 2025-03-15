# SPDX-License-Identifier: GPL-2.0+

import numpy as np

from . import expressions


class arrayspec:
    def __init__(self, array, *, version):
        self._array = array
        self.version = version

    def __bool__(self):
        return len(self._array) > 0

    @property
    def rank(self):
        return int(self._array[0])

    @property
    def corank(self):
        return int(self._array[1])

    @property
    def type(self):
        return self._array[2]

    @property
    def lower(self):
        lower = []
        for i in range(self.rank + self.corank):
            if len(self._array[3 + i * 2]):
                lower.append(
                    expressions.expression(self._array[3 + i * 2], version=self.version)
                )

        return lower

    @property
    def upper(self):
        upper = []
        for i in range(self.rank + self.corank):
            if len(self._array[4 + i * 2]):
                upper.append(
                    expressions.expression(self._array[4 + i * 2], version=self.version)
                )

        return upper

    @property
    def fshape(self):
        res = []
        for l, u in zip(self.lower, self.upper):
            res.append([l.value, u.value])

        return res

    @property
    def pyshape(self):
        res = []
        if self.lower is None:
            return []

        for l, u in zip(self.lower, self.upper):
            res.append(u.value - l.value + 1)

        return res

    @property
    def size(self):
        return np.prod(self.pyshape)
