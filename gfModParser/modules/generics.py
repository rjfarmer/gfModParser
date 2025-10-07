# SPDX-License-Identifier: GPL-2.0+

from typing import List

from .. import utils


class generics:
    name: str = ""
    module: str = ""
    id: t.List[int] = -1

    def __init__(self, generics, *, version):
        self._generic = generics
        self.version = version

    @property
    def name(self) -> str:
        return utils.string_clean(self._generics[0])

    @property
    def module(self) -> str:
        return utils.string_clean(self._generics[1])

    @property
    def ids(self) -> List[int]:
        return [int(i) for i in self._generics[2:]]
