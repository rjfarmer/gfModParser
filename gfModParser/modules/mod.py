# SPDX-License-Identifier: GPL-2.0+

# https://github.com/gcc-mirror/gcc/blob/master/gcc/fortran/module.cc
from packaging.version import Version
from typing import Union
from functools import cached_property

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

    def __init__(self, filename: str, *, version: Version) -> None:
        self.filename = filename
        self.version = version

        self._common = None
        self._equivalence = None
        self._omp = None

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

    @cached_property
    def summary(self):
        return summary.Summary(self._raw_summary, version=self.version)

    @cached_property
    def symbols(self):
        return symbols.Symbols(self._raw_symbols, version=self.version)

    def keys(self):
        return self.summary.keys()

    def __contains__(self, key) -> bool:
        return key in self.summary

    def __getitem__(self, key):
        if isinstance(key, int):
            # Lookup by index, used by procedure to find arguments
            return self.symbols[key]
        if key[0].isupper() and key in self.summary:
            # Derivied type definition starts with a captial letter
            return self.symbols[self.summary[key].id]
        elif key.startswith("__"):
            # Don't change case on internal gfortran fucntions
            return self.symbols[self.summary[key].id]
        else:
            # Everything else is lower case
            return self.symbols[self.summary[key.lower()].id]

    @cached_property
    def operator(self) -> operators.Operators:
        return operators.Operators(self._raw_operators, version=self.version)

    @cached_property
    def interface(self) -> operators.Interfaces:
        return operators.Interfaces(self._raw_interface, version=self.version)

    @cached_property
    def generic(self) -> operators.Generics:
        return operators.Generics(self._raw_generics, version=self.version)
