# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint
import numpy as np

import gfModParser as gf


class TestExpressions:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "basic.mod"))
        self.comp = gf.Module(os.path.join("tests", "build", "comp.mod"))
        self.char = gf.Module(os.path.join("tests", "build", "strings.mod"))
        self.array = gf.Module(os.path.join("tests", "build", "explicit_arrays.mod"))
        self.unicode = gf.Module(os.path.join("tests", "build", "unicode.mod"))
        self.params = gf.Module(os.path.join("tests", "build", "params_modules.mod"))

    def test_type(self):
        assert self.mod["dp"].properties.exp_type.type == "INTEGER"

    def test_typespec(self):
        assert (
            self.mod["dp"].properties.exp_type.typespec.type
            == self.mod["dp"].properties.exp_type.type
        )

    def test_kind(self):
        assert self.mod["dp"].properties.exp_type.rank == 0

    def test_str(self):
        assert str(self.mod["dp"].properties.exp_type) == "INTEGER(kind=4)"
        assert repr(self.mod["dp"].properties.exp_type) == "INTEGER"

        assert str(self.mod["const_real"].properties.exp_type) == "REAL(kind=4)"
        assert str(self.mod["const_real_dp"].properties.exp_type) == "REAL(kind=8)"

        assert (
            str(self.char["const_str"].properties.exp_type)
            == "CHARACTER(kind=1,len=10)"
        )

    def test_parameters(self):

        assert self.mod["const_real"].properties.exp_type.value == 1.0
        assert self.mod["const_real_dp"].properties.exp_type.value == 1.0

        assert self.mod["const_neg_int"].properties.exp_type.value == -1
        assert self.mod["const_int"].properties.exp_type.value == 1
        assert self.mod["const_int_lp"].properties.exp_type.value == 1
        assert self.mod["const_int_p1"].properties.exp_type.value == 2

        assert self.mod["const_neg_real"].properties.exp_type.value == -3.14

        assert self.mod["const_logical_true"].properties.exp_type.value
        assert not self.mod["const_logical_false"].properties.exp_type.value

    def test_complex(self):
        assert self.comp["const_cmplx"].properties.exp_type.value == complex(1.0, 1.0)
        assert self.comp["const_cmplx_dp"].properties.exp_type.value == complex(
            1.0, 1.0
        )

    def test_strings(self):
        assert self.char["const_str"].properties.exp_type.value == "1234567890"
        assert self.char["const_str"].properties.exp_type.len == 10

        assert self.char["a_str"].properties.typespec.charlen.value == 10

    def test_array(self):
        a1 = self.array["const_int_arr"].properties.exp_type
        a2 = self.array["const_int_arr2d"].properties.exp_type
        np.testing.assert_equal(
            a1.value, np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], dtype=np.int32)
        )
        np.testing.assert_equal(
            a2.value, np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 0]], dtype=np.int32)
        )

        assert str(a2) == "INTEGER(kind=4),dimension(2, 5)"

        a3 = self.char["a_str_p_1d"].properties.exp_type
        np.testing.assert_equal(a3.value, np.array([b"aa", b"bb", b"cc"], dtype="|S2"))
        assert str(a3) == "CHARACTER(kind=1,len=2),dimension(3,)"

    def test_real_arrays(self):
        a1 = self.array["const_real_arr"].properties.exp_type
        np.testing.assert_equal(
            a1.value,
            np.array(
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 0.0], dtype=np.float32
            ),
        )

        a2 = self.array["const_real_dp_arr"].properties.exp_type
        np.testing.assert_equal(
            a2.value,
            np.array(
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 0.0], dtype=np.float64
            ),
        )

        a3 = self.array["const_logical_arr"].properties.exp_type
        np.testing.assert_equal(a3.value, np.array([True, False, True, False, True]))

    def test_char_kind_4(self):
        assert self.unicode["uni_param"].properties.exp_type.value == "😀😎😩"

    def test_char_defered_len(self):
        assert self.mod[104].properties.typespec.charlen.value == -1
        assert self.mod[103].properties.typespec.charlen.value == 5

    def test_int_kinds_array(self):
        assert np.allclose(
            self.params["int_i1_1d"].properties.exp_type.value,
            np.array([-10, -1, 0, 1, 10], dtype=np.int8),
        )
        assert np.allclose(
            self.params["int_i2_1d"].properties.exp_type.value,
            np.array([-10, -1, 0, 1, 10], dtype=np.int16),
        )
        assert np.allclose(
            self.params["int_i4_1d"].properties.exp_type.value,
            np.array([-10, -1, 0, 1, 10], dtype=np.int32),
        )
        assert np.allclose(
            self.params["int_i8_1d"].properties.exp_type.value,
            np.array([-10, -1, 0, 1, 10], dtype=np.int64),
        )
