# SPDX-License-Identifier: GPL-2.0+


class namelist:
    def __init__(self, args, *, version):
        self._args = args
        self.version = version

    def __bool__(self):
        return len(self._args) > 0

    @property
    def sym_ref(self):
        sym_ref = []
        if self:
            for i in self._args:
                sym_ref.append(int(i))

        return sym_ref
