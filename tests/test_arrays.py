# SPDX-License-Identifier: GPL-2.0+

import pytest
import os

import gfModParser as gf


class TestArrayExplicit:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "explicit_arrays.mod"))

    def test_rank(self):
        assert self.mod["b_int_exp_1d"].properties.array_spec.rank == 1
        assert self.mod["b_int_exp_2d"].properties.array_spec.rank == 2
        assert self.mod["b_int_exp_3d"].properties.array_spec.rank == 3
        assert self.mod["b_int_exp_4d"].properties.array_spec.rank == 4
        assert self.mod["b_int_exp_5d"].properties.array_spec.rank == 5

        assert self.mod["b_int_exp_1d"].properties.array_spec.ndims == 1

    def test_corank(self):
        assert self.mod["b_int_exp_1d"].properties.array_spec.corank == 0
        assert self.mod["b_int_exp_2d"].properties.array_spec.corank == 0
        assert self.mod["b_int_exp_3d"].properties.array_spec.corank == 0
        assert self.mod["b_int_exp_4d"].properties.array_spec.corank == 0
        assert self.mod["b_int_exp_5d"].properties.array_spec.corank == 0

    def test_type(self):
        assert self.mod["b_int_exp_1d"].properties.array_spec.type == "EXPLICIT"
        assert not self.mod["b_int_exp_1d"].properties.array_spec.is_defered

    def test_if_array(self):
        assert self.mod["const_int_arr"].properties.array_spec
        assert not self.mod["dp"].properties.array_spec

    def test_lower(self):
        assert self.mod["b_int_exp_1d"].properties.array_spec.lower[0].value == 1
        assert self.mod["b_int_exp_2d"].properties.array_spec.lower[1].value == 1

        assert self.mod["b_int_exp_2d_lower"].properties.array_spec.lower[0].value == 1
        assert self.mod["b_int_exp_2d_lower"].properties.array_spec.lower[1].value == 2

        with pytest.raises(IndexError):
            assert self.mod["b_int_exp_2d_lower"].properties.array_spec.lower[5].value

    def test_upper(self):
        assert self.mod["b_int_exp_1d"].properties.array_spec.upper[0].value == 5
        assert self.mod["b_int_exp_2d"].properties.array_spec.upper[1].value == 5

        assert self.mod["b_int_exp_2d_lower"].properties.array_spec.upper[0].value == 5
        assert self.mod["b_int_exp_2d_lower"].properties.array_spec.upper[1].value == 5

        with pytest.raises(IndexError):
            assert self.mod["b_int_exp_2d_lower"].properties.array_spec.upper[5].value

    def test_fshape(self):
        assert self.mod["b_int_exp_1d"].properties.array_spec.fshape == ((1, 5),)
        assert self.mod["b_int_exp_2d"].properties.array_spec.fshape == ((1, 5), (1, 5))

        assert self.mod["b_int_exp_1d_lower"].properties.array_spec.fshape == ((1, 5),)
        assert self.mod["b_int_exp_2d_lower"].properties.array_spec.fshape == (
            (1, 5),
            (2, 5),
        )

    def test_pyshape(self):
        assert self.mod["b_int_exp_1d"].properties.array_spec.pyshape == (5,)
        assert self.mod["b_int_exp_2d"].properties.array_spec.pyshape == (5, 5)

        assert self.mod["b_int_exp_1d_lower"].properties.array_spec.pyshape == (5,)
        assert self.mod["b_int_exp_2d_lower"].properties.array_spec.pyshape == (5, 4)

    def test_size(self):
        assert self.mod["b_int_exp_1d"].properties.array_spec.size == 5
        assert self.mod["b_int_exp_2d"].properties.array_spec.size == 25

        assert self.mod["b_int_exp_1d_lower"].properties.array_spec.size == 5
        assert self.mod["b_int_exp_2d_lower"].properties.array_spec.size == 20


class TestArrayDummy:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "dummy_arrays.mod"))

    def test_rank(self):
        assert self.mod["c_int_alloc_1d"].properties.array_spec.rank == 1
        assert self.mod["c_int_alloc_2d"].properties.array_spec.rank == 2
        assert self.mod["c_int_alloc_3d"].properties.array_spec.rank == 3
        assert self.mod["c_int_alloc_4d"].properties.array_spec.rank == 4
        assert self.mod["c_int_alloc_5d"].properties.array_spec.rank == 5

        assert self.mod["c_int_alloc_1d"].properties.array_spec.ndims == 1

    def test_corank(self):
        assert self.mod["c_int_alloc_1d"].properties.array_spec.corank == 0
        assert self.mod["c_int_alloc_2d"].properties.array_spec.corank == 0
        assert self.mod["c_int_alloc_3d"].properties.array_spec.corank == 0
        assert self.mod["c_int_alloc_4d"].properties.array_spec.corank == 0
        assert self.mod["c_int_alloc_5d"].properties.array_spec.corank == 0

    def test_type(self):
        assert self.mod["c_int_alloc_1d"].properties.array_spec.is_defered

    def test_lower(self):
        assert self.mod["c_int_alloc_1d"].properties.array_spec.lower == []
        assert self.mod["c_int_alloc_2d"].properties.array_spec.lower == []

    def test_upper(self):
        assert self.mod["c_int_alloc_1d"].properties.array_spec.upper == []
        assert self.mod["c_int_alloc_2d"].properties.array_spec.upper == []

    def test_fshape(self):
        assert self.mod["c_int_alloc_1d"].properties.array_spec.fshape == ()
        assert self.mod["c_int_alloc_2d"].properties.array_spec.fshape == ()

    def test_pyshape(self):
        assert self.mod["c_int_alloc_1d"].properties.array_spec.pyshape == ()
        assert self.mod["c_int_alloc_2d"].properties.array_spec.pyshape == ()

    def test_size(self):
        assert self.mod["c_int_alloc_1d"].properties.array_spec.size is None
        assert self.mod["c_int_alloc_2d"].properties.array_spec.size is None
