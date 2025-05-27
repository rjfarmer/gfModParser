# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestComponents:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "dt.mod"))

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

    def test_typespec(self):
        ts = self.mod["S_alloc_array"].properties.components["a_int"].typespec

        assert ts.type == "INTEGER"
        assert ts.kind == 4

    def test_array(self):
        assert (
            not self.mod["S_struct_basic"].properties.components["a_int"].array.is_array
        )
        assert (
            self.mod["S_struct_basic"]
            .properties.components["b_int_exp_1d"]
            .array.is_array
        )

        assert (
            self.mod["S_struct_basic"]
            .properties.components["b_int_exp_1d"]
            .array.lower[0]
            .value
            == 1
        )
        assert (
            self.mod["S_struct_basic"]
            .properties.components["b_int_exp_1d"]
            .array.upper[0]
            .value
            == 5
        )
