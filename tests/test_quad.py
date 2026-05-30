# SPDX-License-Identifier: GPL-2.0+

import os

import pytest

import gfModParser as gf

pyq = pytest.importorskip("pyquadp", reason="Requires pyquadp for quad values")


class TestQuad:
    @pytest.fixture(autouse=True)
    def load(self) -> None:
        self.mod = gf.Module(os.path.join("tests", "build", "quad.mod"))

        if "const_real_qp" not in self.mod:
            pytest.skip("Requires gfortran REAL128 support")

        self.variables = gf.Variables(self.mod)
        self.parameters = gf.Parameters(self.mod)

    def test_quad_kind_parameter_value(self) -> None:
        assert "qp" in self.parameters
        assert self.parameters.type("qp") == "INTEGER"
        assert self.parameters.kind("qp") == 4
        assert self.parameters.value("qp") == 16
        assert self.parameters.value("qp_twice") == 32
        assert self.parameters.value("qp_plus_dp") == 24

    def test_quad_real_parameter_value(self) -> None:
        symbol = self.parameters["const_real_qp"]

        assert symbol.properties.typespec.type == "REAL"
        assert symbol.properties.typespec.kind == 16

        value = self.parameters.value("const_real_qp")
        assert isinstance(value, pyq.qfloat)
        assert value == pyq.qfloat("1.0")

    def test_quad_complex_parameter_value(self) -> None:
        symbol = self.parameters["const_cmplx_qp"]

        assert symbol.properties.typespec.type == "COMPLEX"
        assert symbol.properties.typespec.kind == 16
        assert self.parameters.value("const_cmplx_qp") == complex(1.0, 1.0)

    def test_additional_quad_real_parameters(self) -> None:
        neg_symbol = self.parameters["const_real_qp_neg"]
        sum_symbol = self.parameters["const_real_qp_sum"]

        assert neg_symbol.properties.typespec.type == "REAL"
        assert neg_symbol.properties.typespec.kind == 16
        assert sum_symbol.properties.typespec.type == "REAL"
        assert sum_symbol.properties.typespec.kind == 16

        neg_value = self.parameters.value("const_real_qp_neg")
        sum_value = self.parameters.value("const_real_qp_sum")
        base_value = self.parameters.value("const_real_qp")

        assert isinstance(neg_value, pyq.qfloat)
        assert isinstance(sum_value, pyq.qfloat)
        assert neg_value < pyq.qfloat("0.0")
        assert sum_value > base_value

    def test_additional_quad_complex_parameters(self) -> None:
        neg_symbol = self.parameters["const_cmplx_qp_neg"]
        sum_symbol = self.parameters["const_cmplx_qp_sum"]

        assert neg_symbol.properties.typespec.type == "COMPLEX"
        assert neg_symbol.properties.typespec.kind == 16
        assert sum_symbol.properties.typespec.type == "COMPLEX"
        assert sum_symbol.properties.typespec.kind == 16

        neg_value = self.parameters.value("const_cmplx_qp_neg")
        sum_value = self.parameters.value("const_cmplx_qp_sum")
        base_value = self.parameters.value("const_cmplx_qp")

        assert isinstance(neg_value, complex)
        assert isinstance(sum_value, complex)
        assert neg_value.real < 0.0
        assert neg_value.imag > 0.0
        assert sum_value.real > base_value.real
        assert sum_value.imag < base_value.imag

    def test_quad_variable_type_and_kind(self) -> None:
        assert self.variables.type("a_real_qp") == "REAL"
        assert self.variables.kind("a_real_qp") == 16

        assert self.variables.type("a_cmplx_qp") == "COMPLEX"
        assert self.variables.kind("a_cmplx_qp") == 16

    def test_quad_array_variables(self) -> None:
        assert self.variables.is_array("a_real_qp_arr")
        assert self.variables.kind("a_real_qp_arr") == 16

        assert self.variables.is_array("a_cmplx_qp_arr")
        assert self.variables.kind("a_cmplx_qp_arr") == 16
