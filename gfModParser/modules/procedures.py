# SPDX-License-Identifier: GPL-2.0+
from packaging.version import Version

from .. import utils
from . import expressions
from . import utils as u


class typebound_proc:
    def __init__(self, proc, *, version: Version) -> None:
        self._proc = proc
        self.version = version

    @property
    def access(self):
        return self._proc[0]

    @property
    def overridable(self):
        return self._proc[1]

    # Also sho deferred here? see mio_typebound_proc

    @property
    def nopass(self) -> bool:
        return self._proc[2] == "NOPASS"

    @property
    def is_generic(self):
        return self._proc[3]

    @property
    def ppc(self):
        return self._proc[4]

    @property
    def pass_arg(self) -> str:
        # argument name
        return utils.string_clean(self._proc[5])

    @property
    def pass_arg_num(self) -> int:
        return int(self._proc[6])

    # # TODO: Handle is_generic
    @property
    def proc_ref(self):
        return int(self._proc[7])


class Arglist(u.ListSymbols):
    pass


class actual_arg:
    """A single named argument in a PDT actual argument list."""

    def __init__(self, arg: list, *, version: Version) -> None:
        self._arg = arg
        self.version = version

    @property
    def name(self) -> str:
        return utils.string_clean(self._arg[0])

    @property
    def expression(self):
        return expressions.Expression(self._arg[1], version=self.version)

    @property
    def flag(self) -> int:
        return int(self._arg[2])


class actual_arglist:
    """PDT actual argument list – maps parameter names to expressions.

    Format of each entry: [name, expression, flag]
    """

    def __init__(self, args: list, *, version: Version) -> None:
        self._args = args
        self.version = version

    def __len__(self) -> int:
        return len(self._args)

    def __iter__(self):
        return (actual_arg(a, version=self.version) for a in self._args)

    def __getitem__(self, key: int) -> actual_arg:
        return actual_arg(self._args[key], version=self.version)

    def keys(self) -> list[str]:
        return [utils.string_clean(a[0]) for a in self._args]

    def __str__(self) -> str:
        return str(self.keys())

    def __repr__(self) -> str:
        return repr(self.keys())
