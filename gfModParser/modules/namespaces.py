# SPDX-License-Identifier: GPL-2.0+

from . import procedures


class namespace:
    def __init__(self, namespace, *, version):
        self._namespace = namespace
        self.version = version

    @property
    def ref(self):
        return int(self._namespace)


class derived_ns:
    def __init__(self, derives_ns, *, version):
        self._dns = derives_ns
        self.version = version

        self._proc = None

    def __bool__(self):
        return len(self._dns) > 0

    @property
    def unknown(self):
        return self._dns[0]

    @property
    def proc(self):
        if self._proc is None and self:
            self._proc = []
            for i in self._dns[1:]:
                self._proc.append(procedures.typebound_proc(i, version=self.version))

        return self._proc
