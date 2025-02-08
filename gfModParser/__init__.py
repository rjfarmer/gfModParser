# SPDX-License-Identifier: GPL-2.0+

import pathlib

from . import io
from .modules import mod15


class module:
    def __init__(self, filename):
        self.filename = pathlib.Path(filename)

        if self.filename.suffixes == [".mod", ".txt"]:
            self.header = io.read_uncompressed_header(self.filename)
        else:
            self.header = io.read_compressed_header(self.filename)

        self._version = None
        self.checks()

        self._mod

    def checks(self):
        if self.version == 15:
            self._mod = mod15.module15(self.filename)
        else:
            raise ValueError(f"Unsupported module version {self.version}")

        if not "GFORTRAN" in self.header:
            raise ValueError("Only supports Gfortran modules")

    @property
    def version(self):
        if self._version is None:
            self._version = int(self.header.split("'")[1])
        return self._version

    def keys(self):
        return self._mod.keys()

