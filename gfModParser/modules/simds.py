# SPDX-License-Identifier: GPL-2.0+
from packaging.version import Version


# TODO: Find some Fortran that trigger this
class simd_dec:
    def __init__(self, simds, *, version: Version) -> None:
        self._simds = simds
        self.version = version
