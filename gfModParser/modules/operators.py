# SPDX-License-Identifier: GPL-2.0+

import operator
from packaging.version import Version
from functools import cache, cached_property
import abc

from .. import utils
from . import utils as u


_default_ops = {
    "UPLUS": operator.__add__,
    "UMINUS": operator.__sub__,
    "PLUS": operator.__add__,
    "MINUS": operator.__sub__,
    "TIMES": operator.__mul__,
    "DIVIDE": operator.__truediv__,
    "POWER": operator.__pow__,
    "CONCAT": operator.__add__,  # Only for strings
    "AND": operator.__and__,
    "OR": operator.__or__,
    "EQV": operator.__eq__,
    "NEQV": operator.__ne__,
    "EQ_SIGN": operator.__eq__,
    "EQ": operator.__eq__,
    "NE_SIGN": operator.__ne__,
    "NE": operator.__ne__,
    "GT_SIGN": operator.__gt__,
    "GT": operator.__gt__,
    "GE_SIGN": operator.__ge__,
    "GE": operator.__ge__,
    "LT_SIGN": operator.__le__,
    "LT": operator.__le__,
    "LE_SIGN": operator.__le__,
    "LE": operator.__le__,
    "NOT": operator.__not__,
    "PARENTHESES": None,
    "USER": None,
    "NULL": None,
}


class base_interface(abc.ABC):
    def __init__(self, symbols, *, version: Version) -> None:
        self._raw = symbols
        self.version = version

    @abc.abstractmethod
    def extract(self) -> dict[str, u.ListSymbols]:
        raise NotImplementedError

    def keys(self):
        return self.extract().keys()

    def __getitem__(self, key: str) -> u.ListSymbols:
        return self.extract()[key]

    def values(self):
        return self.extract().values()

    def items(self):
        return self.extract().items()


class Interfaces(base_interface):
    """
    For overriding inbuilt functions (like +,*,-,/ etc)
    """

    @cache
    def extract(self):
        res = {}
        face = utils.bracket_split(self._raw)[0]

        for index, value in enumerate(face):
            if len(value):
                key = list(_default_ops.keys())[index]
                res[key] = u.ListSymbols(value, version=self.version)
        return res

    def op(self, key):
        return _default_ops[key]


class Generics(base_interface):
    """
    Provides generic interfaces (type overloading)
    """

    @cache
    def extract(self):
        res = {}
        face = utils.bracket_split(self._raw)[0]

        for value in face:
            (name, _, *num) = value
            name = utils.string_clean(name)
            res[name] = u.ListSymbols(num, version=self.version)
        return res


class Operators(Generics):
    """
    Provides custom operators like .my_op.
    """

    pass
