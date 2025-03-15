# SPDX-License-Identifier: GPL-2.0+

import pytest

import gfModParser as gf


class TestArrays:
    @pytest.fixture(autouse=True)
    def load(self):
        self.explicit = gf.module("tests/build/explicit_arrays.mod")
        self.dummy = gf.module("tests/build/dummy_arrays.mod")

    @property
    def test_rank(self):
        assert self.explicit["b_int_exp_1d"].properties.array_spec.rank == 1
        assert self.explicit["b_int_exp_2d"].properties.array_spec.rank == 2
        assert self.explicit["b_int_exp_3d"].properties.array_spec.rank == 3
        assert self.explicit["b_int_exp_4d"].properties.array_spec.rank == 4
        assert self.explicit["b_int_exp_5d"].properties.array_spec.rank == 5

    @property
    def test_corank(self):
        assert self.explicit["b_int_exp_1d"].properties.array_spec.corank == 0
        assert self.explicit["b_int_exp_2d"].properties.array_spec.corank == 0
        assert self.explicit["b_int_exp_3d"].properties.array_spec.corank == 0
        assert self.explicit["b_int_exp_4d"].properties.array_spec.corank == 0
        assert self.explicit["b_int_exp_5d"].properties.array_spec.corank == 0

    @property
    def test_type(self):
        assert self.explicit["b_int_exp_1d"].properties.array_spec.type == "INTEGER"
        assert self.explicit["b_real_exp_1d"].properties.array_spec.type == "REAL"
        assert self.explicit["b_str_exp_1d"].properties.array_spec.type == "CHARACTER"
        assert (
            self.explicit["const_logical_arr"].properties.array_spec.type == "LOGICAL"
        )

    @property
    def test_if_array(self):
        assert self.explicit["const_int_arr"].properties.array_spec
        assert not self.explicit["dp"].properties.array_spec
