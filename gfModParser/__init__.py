# SPDX-License-Identifier: GPL-2.0+

import pathlib

from . import io
from .modules import mod


class module:
    def __init__(self, filename):
        self.filename = pathlib.Path(filename)

        if self.filename.suffixes == [".mod", ".txt"]:
            self.header = io.read_uncompressed_header(self.filename)
        else:
            self.header = io.read_compressed_header(self.filename)

        self._version = None
        self._checks()

    def _checks(self):
        if not self.version == 15:
            raise ValueError(f"Unsupported module version {self.version}")

        if not "GFORTRAN" in self.header:
            raise ValueError("Only supports Gfortran modules")

        self._mod = mod.module(self.filename, version=self.version)

    @property
    def version(self):
        if self._version is None:
            self._version = int(self.header.split("'")[1])
        return self._version

    def keys(self):
        return self._mod.keys()

    def __contains__(self, key):
        return key in self._mod

    def __getitem__(self, key):
        return self._mod[key]

    def __dir__(self):
        return self._mod.__dir__()

    def __str__(self):
        return f"Module: {self.filename} Gfortran: {self.version}"

    def __repr__(self):
        return f"module('{self.filename}')"
