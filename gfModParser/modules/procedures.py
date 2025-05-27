# SPDX-License-Identifier: GPL-2.0+

from .. import utils


class typebound_proc:
    def __init__(self, proc, *, version):
        self._proc = proc
        self.version = version

    @property
    def access(self):
        return self._proc[0]

    @property
    def overridable(self):
        return self._proc[1]

    # Also sho defered here? see mio_typebound_proc

    @property
    def nopass(self):
        return self._proc[2] == "NOPASS"

    @property
    def is_generic(self):
        return self._proc[3]

    @property
    def ppc(self):
        return self._proc[4]

    @property
    def pass_arg(self):
        # argument name
        return utils.string_clean(self._proc[5])

    @property
    def pass_arg_num(self):
        return int(self._proc[6])

    # # TODO: Handle is_generic
    @property
    def proc_ref(self):
        return int(self._proc[7])


class arglist:
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
