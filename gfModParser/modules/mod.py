# SPDX-License-Identifier: GPL-2.0+

# https://github.com/gcc-mirror/gcc/blob/master/gcc/fortran/module.cc

import typing as t

from .. import utils
from .. import io

from . import summary
from . import symbols


class VersionError(Exception):
    pass


class module:
    def __init__(self, filename, version):
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

    def keys(self):
        self._load_summary()
        return self._summary.keys()

    def __contains__(self, key):
        self._load_summary()
        return key in self._summary

    def __getitem__(self, key):
        self._load_summary()
        self._load_symbols()
        return self._symbols[self._summary[key].id]

    def __dir__(self):
        return self.keys()
