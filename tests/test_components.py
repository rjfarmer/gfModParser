# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestComponents:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.module("tests/build/dt.mod")

    def test_no_comp(self):
        assert not len(self.mod["dp"].properties.components)

    def test_entries(self):
        assert 9 == len(self.mod["S_struct_basic"].properties.components)
        assert "a_int" in self.mod["S_struct_basic"].properties.components
        assert len(self.mod["S_struct_basic"].properties.components.keys()) == 9

        with pytest.raises(KeyError):
            self.mod["S_struct_basic"].properties.components["XXXXXX"]

    def test_comp(self):
        x = self.mod["S_struct_basic"].properties.components["a_int"]

        assert isinstance(x.id, int)
        assert x.name == "a_int"
        assert x.access == "UNKNOWN-ACCESS"
        assert x.attribute.flavor == "UNKNOWN-FL"
