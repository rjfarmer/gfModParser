# SPDX-License-Identifier: GPL-2.0+
from packaging.version import Version

import numpy as np

from .. import utils

from . import procedures


class ExpGeneric:
    def __init__(self, type, kind, args, *, version: Version) -> None:
        self._args = args
        self.version = version
        self._type = type
        self.kind = kind

    def __str__(self):
        return self._type

    def __repr__(self):
        return self._type

    @property
    def value(self):
        return None

    def __eq__(self, key) -> bool:
        return self._type == key


class Expression:
    def __init__(self, expression, *, version: Version) -> None:
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
            "CONDITIONAL": ExpConditional,
            "UNKNOWN": ExpUnknown,
        }

        self._exp = map[t](
            self.typespec.type,
            self.typespec.kind,
            self._expression,
            version=self.version,
        )

    @property
    def type(self) -> ExpGeneric:
        return self._exp

    @property
    def typespec(self) -> "typespec":
        return typespec(self._expression[1], version=self.version)

    @property
    def rank(self) -> int:
        return int(self._expression[2])

    @property
    def arglist(self) -> list:
        raise NotImplementedError
        # if len(self._exp._args) == 7:
        #     return procedures.actual_arglist(self._exp._args[6])
        # return []

    @property
    def value(self):
        return self._exp.value

    def __str__(self):
        return self._exp.__str__()

    def __repr__(self):
        return self._exp.__repr__()

    @property
    def len(self) -> int:
        return self._exp.len

    @property
    def kind(self) -> int:
        return self.typespec.kind


class ExpOp(ExpGeneric):

    @property
    def unary_op(self):
        return self._args[3]

    @property
    def unary_args(self) -> tuple[Expression, Expression]:
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
            return utils.hextofloat(utils.string_clean(self._args[3]), self.kind)
        elif self._type == "INTEGER" or self._type == "UNSIGNED":
            return int(utils.string_clean(self._args[3]))
        elif self._type == "CHARACTER":
            v = utils.string_clean(self._args[4])
            if self.kind == 4:
                return (
                    v.encode("latin1")
                    .decode("unicode_escape")
                    .encode("latin1")
                    .decode("utf8")
                )
            else:
                return v
        elif self._type == "COMPLEX":
            return complex(
                utils.hextofloat(utils.string_clean(self._args[3]), self.kind),
                utils.hextofloat(utils.string_clean(self._args[4]), self.kind),
            )
        elif self._type == "LOGICAL":
            return int(self._args[3]) == 1
        else:
            raise NotImplementedError(f"Type={self._type} args3={self._args[3]}")

    @property
    def len(self) -> int:
        if self._type == "CHARACTER":
            return int(self._args[3])
        return -1

    def __str__(self):
        if self._type == "CHARACTER":
            return f"CHARACTER(kind={self.kind},len={self.len})"
        else:
            return f"{self.type}(kind={self.kind})"

    @property
    def type(self) -> str:
        return self._type

    @property
    def raw(self) -> str:
        return utils.string_clean(self._args[3])


class ExpVariable(ExpGeneric):
    @property
    def value(self):
        return self._args[3]

    def __str__(self):
        if self._type == "CHARACTER":
            return f"CHARACTER(kind={self.kind},len={self.len})"
        else:
            return f"{self._type}"


class ExpArray(ExpGeneric):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None

    @property
    def value(self) -> np.ndarray:
        if self._value is None:
            self._value = []
            for i in self._args[3]:
                self._value.append(Expression(i[0], version=self.version))

        value = []

        for v in self._value:
            value.append(v.value)

        return np.array(value, dtype=self.dtype).reshape(self.shape)

    @property
    def shape(self) -> tuple[int, ...]:
        return tuple([int(utils.string_clean(i)) for i in self._args[4]])

    @property
    def dtype(self) -> np.dtype:
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


class ExpConditional(ExpNotImplemented):
    pass


class ExpUnknown(ExpNotImplemented):
    pass


# Need to store this here as we get a cyclic dependency
# between expressions and typespec
class typespec:
    def __init__(self, typespec, *, version: Version) -> None:
        self._typespec = typespec
        self.version = version

    @property
    def type(self) -> str:
        return self._typespec[0]

    def _isclass(self) -> bool:
        return self.type == "CLASS" or self.is_dt

    @property
    def is_dt(self) -> bool:
        return self.type == "DERIVED"

    @property
    def kind(self) -> int:
        if not self._isclass():
            return int(self._typespec[1])
        return -1

    @property
    def class_ref(self) -> int:
        if self._isclass():
            return int(self._typespec[1])
        return -1

    @property
    def interface(self):
        return self._typespec[2]

    @property
    def is_c_interop(self) -> bool:
        return int(self._typespec[3]) == 1

    @property
    def is_iso_c(self) -> bool:
        return int(self._typespec[4]) == 1

    @property
    def type2(self):
        # Whats this?
        return self._typespec[5]

    @property
    def charlen(self) -> Expression:
        if len(self._typespec[6]):
            if len(self._typespec[6][0]) == 0:
                # Fake a negative string length for defered length chars
                t = [
                    "CONSTANT",
                    ["INTEGER", "4", "0", "0", "0", "INTEGER", []],
                    "0",
                    "-1",
                    [],
                ]
            else:
                t = self._typespec[6][0]

            return Expression(t, version=self.version)
        raise AttributeError("Object does not have a character length")

    @property
    def deferred_cl(self) -> bool:
        if len(self._typespec) == 8:
            return self._typespec[7] == "DEFERRED_CL"

        return False
