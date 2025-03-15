# SPDX-License-Identifier: GPL-2.0+

from .. import utils


class expression:
    def __init__(self, expression, version):
        self._expression = expression
        self.version = version

    @property
    def type(self):
        return self._expression[0]

    @property
    def typespec(self):
        return self._expression[1]

    @property
    def rank(self):
        return int(self._expression[2])


# class expression:
#     exp_type: str = ""
#     ts: typespec = None
#     rank: int = -1
#     _saved_value: t.Any = None
#     _value: t.Any = None
#     _resolved_value: t.Any = (
#         None  # value may by a symbol_ref, so this is the value after resolving the reference
#     )
#     arglist: actual_arglist = None  # PDT's?
#     charlen: int = -1
#     unary_op: str = ""
#     unary_args: t.Any = None
#     args: t.Any = None

#     def __init__(self, *args):
#         self.raw = args
#         self._resolved_value = None
#         if not len(args):
#             return
#         self.exp_type = args[0]
#         self.ts = typespec(*args[1])
#         self.rank = int(args[2])

#         if self.exp_type == "OP":
#             self._value = None
#             self.unary_op = args[3]
#             self.unary_args = [expression(*args[4]), expression(*args[5])]
#         elif self.exp_type == "FUNCTION":
#             self._value = symbol_ref(args[3])
#             self.args = expression(*args[4][0][1])
#         elif self.exp_type == "CONSTANT":
#             if self.ts.type == "REAL":
#                 self._value = hextofloat(string_clean(args[3]), self.ts.kind)
#             elif self.ts.type == "INTEGER":
#                 self._value = int(string_clean(args[3]))
#             elif self.ts.type == "CHARACTER":
#                 self.charlen = int(args[3])
#                 self._value = string_clean(args[4])
#             elif self.ts.type == "COMPLEX":
#                 self._value = complex(
#                     hextofloat(string_clean(args[3]), self.ts.kind),
#                     hextofloat(string_clean(args[4]), self.ts.kind),
#                 )
#             elif self.ts.type == "LOGICAL":
#                 self._value = int(args[3]) == 1
#             else:
#                 raise NotImplementedError(args)
#         elif self.exp_type == "VARIABLE":
#             self._value = symbol_ref(args[3])
#         elif self.exp_type == "SUBSTRING":
#             raise NotImplementedError(args)
#         elif self.exp_type == "ARRAY" or self.exp_type == "STRUCTURE":
#             self._value = []
#             for i in args[3]:
#                 self._value.append(
#                     expression(*i[0]).value
#                 )  # Wheres the extra component comming from?
#         elif self.exp_type == "NULL":
#             self._value = args[3]
#         elif self.exp_type == "COMPCALL":
#             raise NotImplementedError(args)
#         elif self.exp_type == "PPC":
#             raise NotImplementedError(args)
#         elif self.exp_type == "UNKNOWN":
#             raise NotImplementedError(args)
#         else:
#             raise AttributeError(f"Can't match {self.exp_type}")

#         try:
#             self.arglist = actual_arglist(*args[6])
#         except IndexError:
#             self.arglist = []

#         self._saved_value = self._value

#     @property
#     def value(self):
#         if self._resolved_value is not None:
#             return self._resolved_value
#         else:
#             return self._value

#     @value.setter
#     def value(self, value):
#         self._resolved_value = value


# Need to store this here as we get a cyclic dependency
# between expressions and typespec
class typespec:
    def __init__(self, typespec, version):
        self._typespec = typespec
        self.version = version

    @property
    def type(self):
        return self._typespec[0]

    def _isclass(self):
        return self.type == "CLASS" or self.type == "DERIVED"

    @property
    def kind(self):
        if not self._isclass():
            return int(self._typespec[1])

    @property
    def class_ref(self):
        if self._isclass():
            return int(self._typespec[1])

    @property
    def interface(self):
        return self._typespec[2]

    @property
    def is_c_interop(self):
        return int(self._typespec[3]) == 1

    @property
    def is_iso_c(self):
        return int(self._typespec[4]) == 1

    @property
    def type2(self):
        # Whats this?
        return self._typespec[5]

    @property
    def charlen(self):
        return self._typespec[6]

    #     try:
    #         if not args[6][0]:
    #             self.charlen = -1
    #         else:
    #             self.charlen = expression(
    #                 *args[6][0]
    #             )  # TODO: might this need to be iterated for mulit-d strings?
    #     except IndexError:
    #         self.charlen = -1

    @property
    def deferred_cl(self):
        if len(self._typespec) == 8:
            return self._typespec[7] == "DEFERRED_CL"

        return False
