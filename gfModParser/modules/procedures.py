# SPDX-License-Identifier: GPL-2.0+

from .. import utils

from . import utils as u


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


class Arglist(u.ListSymbols):
    pass
