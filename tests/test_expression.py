# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestExpressions:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.module(os.path.join("tests", "build", "basic.mod"))
        self.comp = gf.module(os.path.join("tests", "build", "comp.mod"))
        self.char = gf.module(os.path.join("tests", "build", "strings.mod"))
        self.array = gf.module(os.path.join("tests", "build", "explicit_arrays.mod"))

    def test_type(self):
        assert self.mod["dp"].properties.parameter.type == "INTEGER"

    def test_typespec(self):
        assert (
            self.mod["dp"].properties.parameter.typespec.type
            == self.mod["dp"].properties.parameter.type
        )

    def test_kind(self):
        assert self.mod["dp"].properties.parameter.rank == 0

    def test_str(self):
        assert str(self.mod["dp"].properties.parameter) == "INTEGER"
        assert repr(self.mod["dp"].properties.parameter) == "INTEGER"

    def test_parameters(self):

        assert self.mod["const_real"].properties.parameter.value == 1.0
        assert self.mod["const_real_dp"].properties.parameter.value == 1.0

        assert self.mod["const_neg_int"].properties.parameter.value == -1
        assert self.mod["const_int"].properties.parameter.value == 1
        assert self.mod["const_int_lp"].properties.parameter.value == 1
        assert self.mod["const_int_p1"].properties.parameter.value == 2

        assert self.mod["const_neg_real"].properties.parameter.value == -3.14

        assert self.mod["const_logical_true"].properties.parameter.value
        assert not self.mod["const_logical_false"].properties.parameter.value

    def test_complex(self):
        assert self.comp["const_cmplx"].properties.parameter.value == complex(1.0, 1.0)
        assert self.comp["const_cmplx_dp"].properties.parameter.value == complex(
            1.0, 1.0
        )

    def test_strings(self):
        assert self.char["const_str"].properties.parameter.value == "1234567890"
        assert self.char["const_str"].properties.parameter.len == 10

    # def test_array(self):
    #     assert self.array['const_int_arr'].properties.parameter.value == [1,2,3,4,5,6,7,8,9,0]
