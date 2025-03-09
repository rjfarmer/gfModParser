# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestComponents:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.module("tests/build/basic.mod")

    def test_no_comp(self):
        assert self.mod["a_int"].properties.components is None
