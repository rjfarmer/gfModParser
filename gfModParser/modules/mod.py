# SPDX-License-Identifier: GPL-2.0+

# https://github.com/gcc-mirror/gcc/blob/master/gcc/fortran/module.cc

import typing as t

from .. import utils
from .. import io

from . import summary
from . import symbols
from . import operators


class VersionError(Exception):
    pass


class module:
    """
    Provides low level interface into the module data
    """

    def __init__(self, filename, *, version):
        self.filename = filename
        self.version = version

        self._interfaces = None
        self._operators = None
        self._common = None
        self._equivalence = None
        self._omp = None
        self._symbols = None
        self._summary = None

        self.load()

    def load(self):
        # Read in data
        if self.filename.suffixes == [".mod", ".txt"]:
            raw_data = io.read_uncompressed(self.filename)
        else:
            raw_data = io.read_compressed(self.filename)

        # Remove header:
        raw_data = raw_data[raw_data.index("(") :]

        # Split into sections
        (
            self._raw_interface,
            self._raw_operators,
            self._raw_generics,
            self._raw_common,
            self._raw_equivalence,
            self._raw_omp,
            self._raw_symbols,
            self._raw_summary,
        ) = raw_data.split("\n\n")

    def _load_summary(self):
        if self._summary is None:
            self._summary = summary.Summary(self._raw_summary, version=self.version)

    def _load_symbols(self):
        if self._symbols is None:
            self._symbols = symbols.Symbols(self._raw_symbols, version=self.version)

    def _load_operators(self):
        if self._operators is None:
            self._interfaces = operators.Interfaces(
                self._raw_interface, version=self.version
            )
            self._operators = operators.Operators(
                self._raw_operators, version=self.version
            )
            self._generics = operators.Generics(
                self._raw_generics, version=self.version
            )

    def keys(self):
        self._load_summary()
        return self._summary.keys()

    def __contains__(self, key):
        self._load_summary()
        return key in self._summary

    def __getitem__(self, key):
        self._load_summary()
        self._load_symbols()
        print(key, type(key))
        if isinstance(key, int):
            # Lookup by index, used by procedure to find arguments
            return self._symbols[key]
        if key[0].isupper() and key in self._summary:
            # Derivied type definition starts with a captial letter
            return self._symbols[self._summary[key].id]
        elif key.startswith("__"):
            # Don't change case on internal gfortran fucntions
            return self._symbols[self._summary[key].id]
        else:
            # Everything else is lower case
            return self._symbols[self._summary[key.lower()].id]

    @property
    def operator(self):
        self._load_operators()
        return self._operators

    @property
    def interface(self):
        self._load_operators()
        return self._interfaces

    @property
    def generic(self):
        self._load_operators()
        return self._generics
