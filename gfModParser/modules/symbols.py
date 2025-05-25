# SPDX-License-Identifier: GPL-2.0+
import re

from .. import utils
from . import properties


class Symbols:
    """
    Holds all variables/procedures/arguments in module
    """

    def __init__(self, symbols, *, version):
        self._raw = symbols
        self.version = version
        self.symbols = symbols
        self._split = None

    def __contains__(self, key):
        if self._split is None:
            self._split_symbols()
        return key in self._split

    def __getitem__(self, key):
        if self._split is None:
            self._split_symbols()

        return self._split[key]

    def _split_symbols(self):

        # Remove initial '(' and final ')\n')
        self.symbols = self.symbols[1:-2]

        # Remove line breaks
        self.symbols = self.symbols.replace("\n", " ")

        # Split data up into groups
        # intrinsic procedures, have brackets in their module name
        matches = re.split(r"(\d+ '\w*' '[\(\)\w]*' '\w*' \d+ )", self.symbols)

        self._split = {}
        # Ignore first match which is empty and take
        # pairs of elements as we get (id,data) from the regex
        for i in range(1, len(matches), 2):
            id = int(matches[i].split(" ")[0].strip())
            data = matches[i] + matches[i + 1]
            # Remove starting \n and ending
            self._split[id] = Symbol(id, data[1:], version=self.version)

    def keys(self):
        if self._split is None:
            self._split_symbols()

        return self._split.keys()

    def items(self):
        if self._split is None:
            self._split_symbols()

        return self._split.items()

    def values(self):
        if self._split is None:
            self._split_symbols()

        return self._split.values()


class Symbol:
    """
    Single object (variable, procedure, argument etc)
    """

    def __init__(self, id, symbol, *, version):
        self.version = version
        self._id = id
        # For very long variable names we may get 'name'\n'module'
        # So replace any \n we find before we get to the first ((
        # dont use single ( as intrinsics use that in their module name
        self._raw = symbol

        self._symbol = symbol.split(" ", maxsplit=5)

    @property
    def mangled_name(self):
        if not self.bind_c:
            return f"__{self.module}_MOD_{self.name}"
        else:
            return utils.string_clean(self._symbol[3])

    @property
    def id(self):
        return int(self._id)

    @property
    def name(self):
        return utils.string_clean(self._symbol[1])

    @property
    def module(self):
        return utils.string_clean(self._symbol[2])

    @property
    def bind_c(self):
        return len(utils.string_clean(self._symbol[3])) > 0

    @property
    def parent_id(self):
        return int(self._symbol[4])

    @property
    def properties(self):
        return properties.Properties(self._symbol[5], version=self.version)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
