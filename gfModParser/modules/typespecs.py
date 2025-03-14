# SPDX-License-Identifier: GPL-2.0+

from .. import utils


class typespec:
    def __init__(self, typespec, version):
        self._raw = typespec
        self.version = version

    # type: str = ""
    # kind: int = -1  # If class symbol_ref else kind
    # class_ref: symbol_ref = None  # If class/derived type symbol_ref else kind
    # interface: symbol_ref = None
    # is_c_interop: int = -1
    # is_iso_c: int = -1
    # type2: str = ""  # Repeat of type
    # charlen: int = -1  # If character
    # deferred_cl: bool = False  # if character and deferred length

    # def __init__(self, *args):
    #     self.raw = args
    #     self.type = args[0]
    #     if self.type == "CLASS" or self.type == "DERIVED":
    #         self.class_ref = symbol_ref(args[1])
    #     else:
    #         self.kind = int(args[1])

    #     if len(args[2]):
    #         self.interface = symbol_ref(args[2])

    #     self.is_c_interop = bool(int(args[3]))
    #     self.is_iso_c = bool(int(args[4]))
    #     self.type2 = args[5]
    #     try:
    #         if not args[6][0]:
    #             self.charlen = -1
    #         else:
    #             self.charlen = expression(
    #                 *args[6][0]
    #             )  # TODO: might this need to be iterated for mulit-d strings?
    #     except IndexError:
    #         self.charlen = -1

    #     try:
    #         self.deferred_cl = args[7] == "DEFERRED_CL"
    #     except (TypeError, IndexError):
    #         self.deferred_cl = False
