# SPDX-License-Identifier: GPL-2.0+


class ListSymbols:
    def __init__(self, args, *, version):
        self._args = [int(i) for i in args]
        self.version = version

    def __len__(self):
        return len(self._args)

    def __iter__(self):
        return iter(self._args)

    @property
    def values(self):
        return self._args

    def __str__(self):
        return str(self._args)

    def __repr__(self):
        return repr(self._args)

    def __contains__(self, key):
        return key in self._args

    def __getitem__(self, key):
        return self._args[key]
