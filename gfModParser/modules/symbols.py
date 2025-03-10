# SPDX-License-Identifier: GPL-2.0+
import re
import functools

from .. import utils
from . import properties


class Symbols:
    """
    Holds all variables/procedures/arguments in module
    """

    def __init__(self, symbols):
        self._raw = symbols
        self.symbols = symbols
        self._split = None

    def __getitem__(self, key):
        if self._split is None:
            self._split_symbols()

        if key not in self._split:
            raise KeyError(f"Can't find symbol {key}")
        return self._split[key]

    def _split_symbols(self):

        # Remove initial '(' and final ')\n')
        self.symbols = self.symbols[1:-2]

        # Make the first symbol look like the others
        self.symbols = ")\n" + self.symbols

        # Split data up into groups
        matches = re.split(r"(\n\d+ '\w*' '\w*' '\w*' \d+ )", self.symbols)

        self._split = {}
        # Ignore first match which is empty and take
        # pairs of elements as we get (id,data) from the regex
        for i in range(1, len(matches), 2):
            id = int(matches[i].split(" ")[0].strip())
            data = matches[i] + matches[i + 1]
            # Remove starting \n and ending
            self._split[id] = Symbol(data[1:])


class Symbol:
    """
    Single object (variable, procedure, argument etc)
    """

    def __init__(self, symbol):
        # For very long variable names we may get 'name'\n'module'
        # So replace any \n we find before we get to the first ((
        # dont use single ( as intrinsics use that in their module name
        self._raw = symbol

        if "((" in symbol:
            index = symbol.index("((")
        else:
            # We got (\n(
            index = symbol.index("(\n(")

        s1 = symbol[:index].replace("\n", " ")
        s2 = symbol[index:]
        symbol = s1 + s2

        self._symbol = symbol.split(" ", maxsplit=5)

    @property
    def mangled_name(self):
        if not self.bind_c:
            return f"__{self.module}_MOD_{self.name}"
        else:
            return utils.string_clean(self._symbol[3])

    @property
    def id(self):
        return int(utils.string_clean(self._symbol[0]))

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

    @functools.cached_property
    def properties(self):
        return properties.Properties(self._symbol[5])
