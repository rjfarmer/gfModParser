import operator
import pyparsing

from .. import utils
from . import utils as u


class Interfaces:

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

    def __init__(self, interfaces, *, version):
        """
        For overriding inbuilt functions (like +,*,-,/ etc)
        """
        self._raw = interfaces
        self._interfaces = None
        self.version = version

    def _load(self):
        self._interfaces = {}
        face = pyparsing.OneOrMore(pyparsing.nestedExpr()).parseString(self._raw)[0]

        for index, value in enumerate(face):
            if len(value):
                key = list(self._default_ops.keys())[index]
                self._interfaces[key] = u.ListSymbols(value, version=self.version)

    def keys(self):
        if self._interfaces is None:
            self._load()

        return self._interfaces.keys()

    def __getitem__(self, key):
        if self._interfaces is None:
            self._load()

        return self._interfaces[key]

    def op(self, key):
        return self._default_ops[key]


class Operators:
    def __init__(self, operators, *, version):
        """
        Provides custom operators like .my_op.
        """
        self._raw = operators
        self._operators = None
        self.version = version

    def _load(self):
        self._operators = {}
        face = pyparsing.OneOrMore(pyparsing.nestedExpr()).parseString(self._raw)[0]

        for value in face:
            (name, _, *num) = value
            name = utils.string_clean(name)
            self._operators[name] = u.ListSymbols(num, version=self.version)

    def keys(self):
        if self._operators is None:
            self._load()

        return self._operators.keys()

    def __getitem__(self, key):
        if self._operators is None:
            self._load()

        return self._operators[key]


class Generics:
    def __init__(self, generics, *, version):
        """
        Provides generic interfaces (type overloading)
        """
        self._raw = generics
        self._generics = None
        self.version = version

    def _load(self):
        self._generics = {}
        face = pyparsing.OneOrMore(pyparsing.nestedExpr()).parseString(self._raw)[0]

        for value in face:
            (name, _, *num) = value
            name = utils.string_clean(name)
            self._generics[name] = u.ListSymbols(num, version=self.version)

    def keys(self):
        if self._generics is None:
            self._load()

        return self._generics.keys()

    def __getitem__(self, key):
        if self._generics is None:
            self._load()

        return self._generics[key]
