# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestSymbols:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "basic.mod"))

    def test_type(self):
        assert self.mod["a_int"].properties.typespec.type == "INTEGER"
        assert self.mod["a_real"].properties.typespec.type == "REAL"

    def test_kind(self):
        assert self.mod["a_int"].properties.typespec.kind == 4
        assert self.mod["a_real"].properties.typespec.kind == 4
        assert self.mod["a_int_lp"].properties.typespec.kind == 8
        assert self.mod["a_real_dp"].properties.typespec.kind == 8


class TestISOC:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "isoc.mod"))

    def test_interop(self):
        assert self.mod["func_bind_c"].properties.typespec.is_c_interop
        assert self.mod["a_c_int"].properties.typespec.is_c_interop
        assert not self.mod["a_int"].properties.typespec.is_c_interop

    def test_is_iso_c(self):
        assert not self.mod["a_c_int"].properties.typespec.is_iso_c
        assert not self.mod["a_int"].properties.typespec.is_iso_c
