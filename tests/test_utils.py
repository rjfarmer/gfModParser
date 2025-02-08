# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestUtils:
    def test_hex(self):
        assert gf.utils.hextofloat("0.12decde@9") == 5065465344.0
        assert gf.utils.hextofloat("-0.12decde@9") == -5065465344.0
