# SPDX-License-Identifier: GPL-2.0+
from packaging.version import Version

from .. import utils


class generics:
    def __init__(self, generics, *, version: Version) -> None:
        self._generic = generics
        self.version = version

    @property
    def name(self) -> str:
        return utils.string_clean(self._generic[0])

    @property
    def module(self) -> str:
        return utils.string_clean(self._generic[1])

    @property
    def ids(self) -> list[int]:
        return [int(i) for i in self._generic[2:]]
