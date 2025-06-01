# SPDX-License-Identifier: GPL-2.0+

import numpy as np

from .. import utils

from . import procedures


class Expression:
    def __init__(self, expression, *, version):
        self._expression = expression
        self.version = version
        t = self._expression[0]

        map = {
            "OP": ExpOp,
            "FUNCTION": ExpFunction,
            "CONSTANT": ExpConstant,
            "VARIABLE": ExpVariable,
            "SUBSTRING": ExpSubString,
            "STRUCTURE": ExpStructure,
            "ARRAY": ExpArray,
            "NULL": ExpNull,
            "COMPCALL": ExpCompCall,
            "PPC": ExpPPC,
            "UNKNOWN": ExpUnknown,
        }

        self._exp = map[t](
            self.typespec.type,
            self.typespec.kind,
            self._expression,
            version=self.version,
        )

    @property
    def type(self):
        return self._exp

    @property
    def typespec(self):
        return typespec(self._expression[1], version=self.version)

    @property
    def rank(self):
        return int(self._expression[2])

    @property
    def arglist(self):
        if len(self._exp._args) == 7:
            return procedures.actual_arglist(self._exp._args[6])

    @property
    def value(self):
        return self._exp.value

    def __str__(self):
        return self._exp.__str__()

    def __repr__(self):
        return self._exp.__repr__()

    @property
    def len(self):
        return self._exp.len

    @property
    def kind(self):
        return self._exp._kind


class ExpGeneric:
    def __init__(self, type, kind, args, *, version):
        self._args = args
        self.version = version
        self._type = type
        self._kind = kind

    def __str__(self):
        return self._type

    def __repr__(self):
        return self._type

    @property
    def value(self):
        return None

    def __eq__(self, key):
        return self._type == key

    @property
    def kind(self):
        return self._kind


class ExpOp(ExpGeneric):

    @property
    def unary_op(self):
        return self._args[3]

    @property
    def unary_args(self):
        return Expression(self._args[4], version=self.version), Expression(
            self._args[5], version=self.version
        )


class ExpNotImplemented(ExpGeneric):
    @property
    def value(self):
        raise NotImplementedError


class ExpFunction(ExpGeneric):
    @property
    def value(self):
        return self._args[3]

    @property
    def args(self):
        return Expression(self._args[4], version=self.version)


class ExpConstant(ExpGeneric):
    @property
    def value(self):
        if self._type == "REAL":
            return utils.hextofloat(utils.string_clean(self._args[3]), self._kind)
        elif self._type == "INTEGER" or self._type == "UNSIGNED":
            return int(utils.string_clean(self._args[3]))
        elif self._type == "CHARACTER":
            return utils.string_clean(self._args[4])
        elif self._type == "COMPLEX":
            return complex(
                utils.hextofloat(utils.string_clean(self._args[3]), self._kind),
                utils.hextofloat(utils.string_clean(self._args[4]), self._kind),
            )
        elif self._type == "LOGICAL":
            return int(self._args[3]) == 1
        else:
            raise NotImplementedError(f"Type={self._type} args3={self._args[3]}")

    @property
    def len(self):
        if self._type == "CHARACTER":
            return int(self._args[3])

    def __str__(self):
        if self._type == "CHARACTER":
            return f"CHARACTER(kind={self.kind},len={self.len})"
        else:
            return f"{self.type}(kind={self.kind})"

    @property
    def type(self):
        return self._type


class ExpVariable(ExpGeneric):
    @property
    def value(self):
        return self._args[3]

    def __str__(self):
        if self.type == "CHARACTER":
            return f"CHARACTER(kind={self.kind},len={self.len})"
        else:
            return f"{self.type}"


class ExpArray(ExpGeneric):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None

    @property
    def value(self):
        if self._value is None:
            self._value = []
            for i in self._args[3]:
                self._value.append(Expression(i[0], version=self.version))

        value = []

        for v in self._value:
            value.append(v.value)

        return np.array(value, dtype=self.dtype).reshape(self.shape)

    @property
    def shape(self):
        return tuple([int(utils.string_clean(i)) for i in self._args[4]])

    @property
    def dtype(self):
        v = Expression(self._args[3][0][0], version=self.version)
        return utils.dtype(v.type, self.kind, len=v.len)

    def __str__(self):
        v = Expression(self._args[3][0][0], version=self.version)
        if v.type == "CHARACTER":
            return f"CHARACTER(kind={v.kind},len={v.len}),dimension{self.shape}"
        else:
            return f"{v.type},dimension{self.shape}"


class ExpSubString(ExpNotImplemented):
    pass


class ExpStructure(ExpNotImplemented):
    pass


class ExpNull(ExpNotImplemented):
    pass


class ExpCompCall(ExpNotImplemented):
    pass


class ExpPPC(ExpNotImplemented):
    pass


class ExpUnknown(ExpNotImplemented):
    pass


# Need to store this here as we get a cyclic dependency
# between expressions and typespec
class typespec:
    def __init__(self, typespec, *, version):
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
    #             self.charlen = Expression(
    #                 *args[6][0]
    #             )  # TODO: might this need to be iterated for mulit-d strings?
    #     except IndexError:
    #         self.charlen = -1

    @property
    def deferred_cl(self):
        if len(self._typespec) == 8:
            return self._typespec[7] == "DEFERRED_CL"

        return False
