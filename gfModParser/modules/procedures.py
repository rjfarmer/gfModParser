# SPDX-License-Identifier: GPL-2.0+

from .. import utils


# @dataclass_json
# @dataclass(init=False)
# class formal_arglist:
#     symbol: t.List[symbol_ref] = None

#     def __init__(self, *args):
#         self.symbol = []
#         for i in args:
#             self.symbol.append(symbol_ref(i))

#         self.raw = args

#     def __len__(self):
#         return len(self.symbol)

#     def __iter__(self):
#         return iter(self.symbol)


class typebound_proc:
    def __init__(self, proc, version):
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
    # self.proc_ref = symbol_ref(args[0][1][7][0])


# @dataclass_json
# @dataclass(init=False)
# class actual_arglist:
#     def __init__(self, *args, **kwargs):
#         self.raw = args
#         self.kwargs = kwargs
