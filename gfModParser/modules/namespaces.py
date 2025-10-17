# SPDX-License-Identifier: GPL-2.0+
from packaging.version import Version

from . import procedures


class namespace:
    def __init__(self, namespace, *, version: Version) -> None:
        self._namespace = namespace
        self.version = version

    @property
    def ref(self) -> int:
        return int(self._namespace)


class derived_ns:
    def __init__(self, derives_ns, *, version: Version) -> None:
        self._dns = derives_ns
        self.version = version

        self._proc: list[procedures.typebound_proc] = []

    def __bool__(self) -> bool:
        return len(self._dns) > 0

    @property
    def unknown(self):
        return self._dns[0]

    @property
    def proc(self) -> list[procedures.typebound_proc]:
        if not len(self._proc) and self:
            self._proc = []
            for i in self._dns[1:]:
                self._proc.append(procedures.typebound_proc(i, version=self.version))

        return self._proc
