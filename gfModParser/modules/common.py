# SPDX-License-Identifier: GPL-2.0+
import regex

from .. import utils


#################################


class SummaryItem:
    """
    Single entry into the Summary look up table
    """

    def __init__(self, name, ambiguous, id):
        self.name = utils.string_clean(name)
        self.ambiguous = ambiguous != "0"
        self.id = int(id)


class Summary:
    """
    Look up table of top level variables/procedures and thier ID's
    """

    def __init__(self, summary):
        # Remove any nested newlines
        self._raw_summary = summary.replace("\n", " ")
        # Remove start and end brackets
        self._raw_summary = self._raw_summary.replace("(", "").replace(") ", "")

        # Split into list
        self._raw_summary = self._raw_summary.split()
        self._names = {}

        # Split into groups of three
        for i in range(0, len(self._raw_summary), 3):
            d = SummaryItem(*self._raw_summary[i : i + 3])
            self._names[d.name] = d

    def __getitem__(self, key):
        return self._names[key]

    def keys(self):
        return self._names.keys()

    def __contains__(self, key):
        return key in self._names


######################################


class Symbols:
    """
    Holds all variables/procedures/arguements in module
    """

    def __init__(self, symbols):
        self.symbols = symbols
        self._split = None

    def __getitem__(self, key):
        if self._split is None:
            self.split_symbols()

        return self._split[key]

    def keys(self):
        if self._split is None:
            self.split_symbols()

        return self._split.keys()

    def __contains__(self, key):
        if self._split is None:
            self.split_symbols()
        return key in self._split

    def split_symbols(self):

        # Remove initial '(' and final ')\n')
        self.symbols = self.symbols[1:-2]

        # Make the first symbol look like the others
        self.symbols = ")\n" + self.symbols

        # Split data up into groups
        # We want close bracket-newline-number-space-single quote
        matches = regex.split(r"(\)\n[0-9]+\s')", self.symbols)

        self._split = {}
        # Ignore first match which is empty and take
        # pairs of elements as we get (id,data) from the regex
        for i in range(1, len(matches), 2):
            id = int(matches[i][2:-1])  # Remove initial ')\n' and final "'"
            data = "'" + matches[i + 1]
            self._split[id] = Symbol(data)


class Symbol:
    """
    Single object (variable, procedure, argument etc)
    """

    def __init__(self, symbol):
        self._symbol = symbol
        self._name = None
        self._module = None
        self._bind_c = None
        self._parent_id = None
        self._data = None

        # Don't process data yet, wait till the user actually
        # accesses the element before further processing
        # otherwise loading times will balloon.

    def _load(self):
        if self._name is not None:
            return

        (self._name, self._module, self._bind_c, self._parent_id, self._data) = (
            self._symbol.split(" ", maxsplit=4)
        )

        # Tidy up values
        self._name = utils.string_clean(self._name)
        self._module = utils.string_clean(self._module)
        self._bind_c = utils.string_clean(self._bind_c)  # boolean?
        self._parent_id = int(self._parent_id)

    def mangled_name(self):
        if self._name is None:
            self.load()
        return f"__{self.module}_MOD_{self.name}"

    @property
    def name(self):
        if self._name is None:
            self._load()
        return self._name

    @property
    def module(self):
        if self._module is None:
            self._load()
        return self._module

    @property
    def bind_c(self):
        if self._bind_c is None:
            self._load()
        return self._bind_c

    @property
    def parent_id(self):
        if self._parent_id is None:
            self._load()
        return self._parent_id
