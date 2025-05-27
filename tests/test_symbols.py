# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestSymbols:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "basic.mod"))

    def test_keys(self):
        assert len(self.mod.keys()) == 60

    def test_in(self):
        assert "a_int" in self.mod
        assert "func_test_case" in self.mod
        assert "dp" in self.mod

        assert "XXXX" not in self.mod

    def test_mangled_name(self):
        assert self.mod["a_int"].mangled_name == "__basic_MOD_a_int"
        assert self.mod["bind_c_int"].mangled_name == "A_C_INT"

    def test_bind_c(self):
        assert not self.mod["a_int"].bind_c
        assert self.mod["bind_c_int"].bind_c

    def test_parent_id(self):
        assert self.mod["a_int"].parent_id == 1

    def test_properties(self):
        assert isinstance(
            self.mod["a_int"].properties, gf.modules.properties.Properties
        )

    def test_id(self):
        assert self.mod["a_int"].id != self.mod["dp"].id
        assert isinstance(self.mod["a_int"].id, int)

    def test_str(self):
        assert str(self.mod["dp"]) == "dp"
        assert repr(self.mod["dp"]) == "dp"

    def test_case(self):
        assert self.mod["const_int_MIXED"].name
