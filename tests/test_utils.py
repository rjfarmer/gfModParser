# SPDX-License-Identifier: GPL-2.0+

import numpy as np
from pprint import pprint

import gfModParser as gf


class TestUtils:
    def test_hex(self):
        assert gf.utils.hextofloat("0.12decde@9") == 5065465344.0
        assert gf.utils.hextofloat("-0.12decde@9") == -5065465344.0

    def test_hex_dble(self):
        h = gf.utils.hextofloat("0.12decde@9", kind=8)
        assert isinstance(h, np.double)

        assert h == np.double(5065465344.0)
