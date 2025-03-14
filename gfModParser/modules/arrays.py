# SPDX-License-Identifier: GPL-2.0+

from .. import utils


class arrayspec:
    def __init__(self, array, version):
        self._raw = array
        self.version = version

    #     if not len(args):
    #         return

    #     self.rank = int(args[0])
    #     self.corank = int(args[1])
    #     self.array_type = args[2]
    #     self.lower = []
    #     self.upper = []
    #     for i in range(self.rank + self.corank):
    #         if len(args[3 + i * 2]):
    #             self.lower.append(expression(*args[3 + i * 2]))
    #         if len(args[4 + i * 2]):
    #             self.upper.append(expression(*args[4 + i * 2]))

    # @property
    # def fshape(self):
    #     res = []
    #     for l, u in zip(self.lower, self.upper):
    #         res.append([l.value, u.value])

    #     return res

    # @property
    # def pyshape(self):
    #     res = []
    #     if self.lower is None:
    #         return []

    #     for l, u in zip(self.lower, self.upper):
    #         res.append(u.value - l.value + 1)

    #     return res

    # @property
    # def size(self):
    #     return np.prod(self.pyshape)
