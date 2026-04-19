# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint
import numpy as np
from packaging.version import Version

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

    def test_array_value_cached(self):
        arr = self.array["const_int_arr"].properties.exp_type

        first = arr.value
        second = arr.value

        assert first is second
        np.testing.assert_equal(
            first, np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], dtype=np.int32)
        )

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

    def test_expression_helper_paths(self):
        typespec = ["INTEGER", "4", "0", "0", "0", "INTEGER", []]
        const_expr = ["CONSTANT", typespec, "0", "1", []]

        op_expr = gf.modules.expressions.Expression(
            ["OP", typespec, "0", "UPLUS", const_expr, const_expr],
            version=Version("15"),
        )
        assert op_expr.type.unary_op == "UPLUS"
        left, right = op_expr.type.unary_args
        assert left.value == 1
        assert right.value == 1

        fn_expr = gf.modules.expressions.Expression(
            ["FUNCTION", typespec, "0", "f", const_expr],
            version=Version("15"),
        )
        assert fn_expr.value == "f"
        assert fn_expr.type.args.value == 1

        with pytest.raises(NotImplementedError):
            _ = fn_expr.arglist

    def test_not_implemented_expression_variants(self):
        typespec = ["INTEGER", "4", "0", "0", "0", "INTEGER", []]
        for et in [
            "SUBSTRING",
            "STRUCTURE",
            "NULL",
            "COMPCALL",
            "PPC",
            "CONDITIONAL",
            "UNKNOWN",
        ]:
            e = gf.modules.expressions.Expression(
                [et, typespec, "0"], version=Version("15")
            )
            with pytest.raises(NotImplementedError):
                _ = e.value

    def test_exp_generic_base(self):
        g = gf.modules.expressions.ExpGeneric("INTEGER", 4, [], version=Version("15"))
        assert str(g) == "INTEGER"
        assert repr(g) == "INTEGER"
        assert g.value is None
        assert g.len is None
        assert g == "INTEGER"

    def test_typespec_branches(self):
        t_class = gf.modules.expressions.typespec(
            ["CLASS", "7", "iface", "0", "0", "X", []], version=Version("15")
        )
        assert t_class.kind == -1
        assert t_class.class_ref == 7
        assert t_class.interface == "iface"
        assert t_class.type2 == "X"

        t_char = gf.modules.expressions.typespec(
            ["CHARACTER", "1", "0", "0", "0", "CHARACTER", [], "DEFERRED_CL"],
            version=Version("15"),
        )
        assert t_char.deferred_cl
        with pytest.raises(AttributeError):
            _ = t_char.charlen

        t_no_defer = gf.modules.expressions.typespec(
            ["INTEGER", "4", "0", "0", "0", "INTEGER", []],
            version=Version("15"),
        )
        assert not t_no_defer.deferred_cl


class TestPDT:
    @pytest.fixture(autouse=True)
    def load(self):
        self.pdt = gf.Module(os.path.join("tests", "build", "pdt.mod"))

    def test_pdt_actual_arglist_type(self):
        aa = self.pdt["pdt_dp_3"].properties.actual_argument
        assert isinstance(aa, gf.modules.procedures.actual_arglist)

    def test_pdt_actual_arglist_len(self):
        assert len(self.pdt["pdt_dp_3"].properties.actual_argument) == 2
        assert len(self.pdt["pdt_qp_2"].properties.actual_argument) == 2

    def test_pdt_actual_arglist_keys(self):
        aa = self.pdt["pdt_dp_3"].properties.actual_argument
        assert aa.keys() == ["k", "a"]

    def test_pdt_actual_arglist_values(self):
        aa = self.pdt["pdt_dp_3"].properties.actual_argument
        assert aa[0].name == "k"
        assert aa[0].expression.value == 8
        assert aa[1].name == "a"
        assert aa[1].expression.value == 3

    def test_pdt_qp_arglist_values(self):
        aa = self.pdt["pdt_qp_2"].properties.actual_argument
        assert aa[0].name == "k"
        assert aa[0].expression.value == 16
        assert aa[1].name == "a"
        assert aa[1].expression.value == 2

    def test_pdt_sp_arglist_values(self):
        aa = self.pdt["pdt_sp_3"].properties.actual_argument
        assert aa[0].name == "k"
        assert aa[0].expression.value == 8
        assert aa[1].name == "a"
        assert aa[1].expression.value == 3

    def test_pdt_actual_arglist_iter(self):
        names = [a.name for a in self.pdt["pdt_dp_3"].properties.actual_argument]
        assert names == ["k", "a"]

    def test_pdt_empty_actual_argument_is_arglist(self):
        # Non-PDT symbols still return the regular Arglist
        aa = self.pdt["dp"].properties.actual_argument
        assert isinstance(aa, gf.modules.procedures.Arglist)
        assert len(aa) == 0
