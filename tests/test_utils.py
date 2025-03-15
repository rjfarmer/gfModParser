# SPDX-License-Identifier: GPL-2.0+

import numpy as np

import gfModParser as gf


class TestUtils:
    def test_hex(self):
        assert gf.utils.hextofloat("0.12decde@9") == 5065465344.0
        assert gf.utils.hextofloat("-0.12decde@9") == -5065465344.0

    def test_hex_dble(self):
        h = gf.utils.hextofloat("0.12decde@9", kind=8)
        assert isinstance(h, np.double)

        assert h == np.double(5065465344.0)

    def test_string_clean(self):

        # fmt: off
        assert gf.utils.string_clean("'abc'") == 'abc'
        assert gf.utils.string_clean("'abc'") == 'abc'
        assert gf.utils.string_clean("abc") == 'abc'
        assert gf.utils.string_clean("") == ''
        assert gf.utils.string_clean(None) is None
        # fmt: on
