# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
import copy
from pprint import pprint

import gfModParser as gf


class TestProcedures:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "basic.mod"))

    def test_ret_func(self):
        ref = self.mod["func_check_mod"].properties.symbol_reference
        assert ref > 0
        assert self.mod[ref].name == "func_check_mod"

    def test_ret_func_result(self):
        ref = self.mod["func_result"].properties.symbol_reference
        assert ref > 0
        assert self.mod[ref].name == "z"

    def test_ret_sub(self):
        ref = self.mod["sub_int_in"].properties.symbol_reference
        assert ref == 0

    def test_args(self):
        refs = self.mod["func_intent_out"].properties.formal_argument
        assert len(refs) == 2
        assert self.mod[refs[0]].name == "y"
        assert self.mod[refs[1]].name == "x"

    def test_args_ret_type(self):
        ref = self.mod["func_check_mod"].properties.symbol_reference
        arg = self.mod[ref]
        assert arg.properties.typespec.kind == 4
        assert arg.properties.typespec.type == "LOGICAL"

    def test_intent(self):
        ref = self.mod["func_result"].properties.symbol_reference
        return_arg = self.mod[ref]
        assert return_arg.properties.attributes.intent == "UNKNOWN-INTENT"

        refs = self.mod["func_result"].properties.formal_argument
        assert self.mod[refs[0]].properties.attributes.intent == "IN"
        assert self.mod[refs[1]].properties.attributes.intent == "OUT"

    def test_value(self):
        refs = self.mod["func_int_value"].properties.formal_argument
        assert self.mod[refs[0]].properties.attributes.value

    def test_optional(self):
        refs = self.mod["sub_int_opt"].properties.formal_argument
        assert self.mod[refs[0]].properties.attributes.optional

    def test_case(self):
        assert self.mod["func_TEST_CASE"].properties.symbol_reference > 0
