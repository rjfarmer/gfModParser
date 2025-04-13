# SPDX-License-Identifier: GPL-2.0+


# TODO: Find some Fortran that trigger this
class simd_dec:
    def __init__(self, simds, *, version):
        self._simds = simds
        self.version = version
