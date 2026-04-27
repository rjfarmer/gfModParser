# SPDX-License-Identifier: GPL-2.0+

import os
from pprint import pprint

import pytest

import gfModParser as gf


class TestSymbols:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "basic.mod"))
        self.arrmod = gf.Module(os.path.join("tests", "build", "explicit_arrays.mod"))

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

    def test_symbol_container_views(self):
        syms = self.mod._mod.symbols

        keys = list(syms.keys())
        items = list(syms.items())
        values = list(syms.values())

        assert len(keys) > 0
        assert len(items) == len(values) == len(keys)
        assert isinstance(items[0][0], int)
        assert isinstance(items[0][1], gf.modules.symbols.Symbol)
        assert isinstance(values[0], gf.modules.symbols.Symbol)

    def test_symbol_predicates(self):
        assert not self.mod["a_int"].is_array
        assert self.arrmod["const_int_arr"].is_array

        assert self.mod["func_int_in"].is_procedure
        assert self.mod["func_int_in"].is_function
        assert not self.mod["func_int_in"].is_subroutine

        assert self.mod["sub_no_args"].is_procedure
        assert self.mod["sub_no_args"].is_subroutine
        assert not self.mod["sub_no_args"].is_function
