# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestProperties:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "basic.mod"))
        self.dt = gf.Module(os.path.join("tests", "build", "dt.mod"))
        self.ptrs = gf.Module(os.path.join("tests", "build", "ptrs.mod"))

    def test_parameter(self):
        assert self.mod["dp"].properties.exp_type.value == 8

    def test_comp_access(self):
        assert self.dt["S_struct_basic"].properties.component_access == "PUBLIC"

    def test_namespace(self):
        assert self.mod["dp"].properties.namespace.ref == 0

    def test_common_symbol(self):
        assert self.mod["dp"].properties.common_symbol == 0

    def test_symbol_reference(self):
        assert self.mod["dp"].properties.symbol_reference == 0

    def test_cray(self):
        assert self.mod["dp"].properties.cray_pointer_reference == -1

        assert self.ptrs["ipt"].properties.cray_pointer_reference == 0

    def test_derived(self):
        assert self.dt["S_struct_basic"].properties.derived
        assert not self.mod["dp"].properties.derived

    def test_derived_proc(self):
        proc = self.dt["S_struct_basic"].properties.derived.proc
        assert len(proc) == 3
        # TODO: Needs tests for the actual elements of proc, seems to be empty for S_struct_basic
