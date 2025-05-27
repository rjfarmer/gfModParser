# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestAttributes:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "basic.mod"))
        self.mod2 = gf.Module(os.path.join("tests", "build", "dt.mod"))

    def test_flavor(self):
        assert self.mod["a_int"].properties.attributes.is_variable
        assert self.mod["dp"].properties.attributes.is_parameter
        assert self.mod["func_int_no_args"].properties.attributes.is_procedure

        # Procedure argument
        assert self.mod._mod._symbols[34].properties.attributes.is_variable

    def test_proc(self):
        assert self.mod["a_int"].properties.attributes.procedure == "UNKNOWN-PROC"
        assert self.mod["sub_int_in"].properties.attributes.procedure == "MODULE-PROC"

    def test_if_src(self):
        assert self.mod["a_int"].properties.attributes.if_source == "UNKNOWN"
        assert self.mod["sub_int_in"].properties.attributes.if_source == "DECL"

    def test_intent(self):
        assert self.mod["a_int"].properties.attributes.intent == "UNKNOWN-INTENT"
        assert self.mod._mod._symbols[34].properties.attributes.intent == "IN"

    def test_save(self):
        assert self.mod["a_int"].properties.attributes.save == "IMPLICIT-SAVE"
        assert self.mod._mod._symbols[34].properties.attributes.save == "UNKNOWN"
        assert self.mod["a_int_save"].properties.attributes.save == "EXPLICIT-SAVE"

    def test_ext_attr(self):
        assert not self.mod["a_int"].properties.attributes.external_attribute

    def test_extension(self):
        assert not self.mod["a_int"].properties.attributes.extension

    def test_attrs(self):
        assert "SUBROUTINE" in self.mod["sub_int_in"].properties.attributes.attributes
        assert (
            "FUNCTION" in self.mod["func_real_no_args"].properties.attributes.attributes
        )

        assert self.mod["sub_int_in"].properties.attributes.subroutine
        assert self.mod["func_real_no_args"].properties.attributes.function

        assert not self.mod["func_real_no_args"].properties.attributes.subroutine
        assert not self.mod["sub_int_in"].properties.attributes.function

    def test_missing(self):
        with pytest.raises(AttributeError):
            self.mod["sub_int_in"].properties.attributes.XXXXXXXXX

    def test_module(self):
        assert self.mod["basic2"].properties.attributes.is_module
        assert not self.mod["sub_int_in"].properties.attributes.is_module

    def test_derived(self):
        assert self.mod2["S_alloc_array"].properties.attributes.is_derived
        assert not self.mod2["s_alloc_array"].properties.attributes.is_derived
        assert not self.mod2["f_struct"].properties.attributes.is_derived

    def test_dir(self):
        assert "dimension" in dir(self.mod2["S_alloc_array"].properties.attributes)


class TestAttrElemental:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "elements.mod"))

    def test_status(self):
        assert self.mod["pure_func"].properties.attributes.pure
        assert self.mod["impure_func"].properties.attributes.implicit_pure
        assert self.mod["ele_func_1"].properties.attributes.elemental
