# SPDX-License-Identifier: GPL-2.0+

from .. import utils


class expression:
    def __init__(self, expression, *, version):
        self._expression = expression
        self.version = version

    @property
    def type(self):
        t = self._expression[0]
        return _map[t](t, self.typespec.kind, self._expression, version=self.version)

    @property
    def typespec(self):
        return typespec(self._expression[1], version=self.version)

    @property
    def rank(self):
        return int(self._expression[2])

    @property
    def arglist(self):
        if len(self._args) == 7:
            return self._args[6]  # actual_arglist


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


class ExpOp(ExpGeneric):

    @property
    def unary_op(self):
        return self._args[3]

    @property
    def unary_args(self):
        return expression(self._args[4], version=self.version), expression(
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
        return expression(self._args[4], version=self.version)


class ExpConstant(ExpGeneric):
    @property
    def value(self):
        if self._type == "REAL":
            return utils.hextofloat(utils.string_clean(self._args[3]), self._kind)
        elif self._type == "INTEGER":
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
            raise NotImplementedError(self._args)

    def len(self):
        if self._type == "CHARACTER":
            return int(self._args[3])


class ExpVariable(ExpGeneric):
    @property
    def value(self):
        return self._args[3]


class ExpArray(ExpGeneric):
    @property
    def value(self):
        value = []
        for i in self._args[3]:
            value.append(expression(i, version=self.version))

        return value


class ExpSubString(ExpNotImplemented):
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


_map = {
    "OP": ExpOp,
    "FUNCTION": ExpFunction,
    "CONSTANT": ExpConstant,
    "VARIABLE": ExpVariable,
    "SUBSTRING": ExpSubString,
    "NULL": ExpNull,
    "COMPCALL": ExpCompCall,
    "PPC": ExpPPC,
    "UNKNOWN": ExpUnknown,
}
