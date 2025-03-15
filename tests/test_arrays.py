# SPDX-License-Identifier: GPL-2.0+

import pytest

import gfModParser as gf


class TestArrays:
    @pytest.fixture(autouse=True)
    def load(self):
        self.explicit = gf.module("tests/build/explicit_arrays.mod")
        self.dummy = gf.module("tests/build/dummy_arrays.mod")

    def test_rank(self):
        assert self.explicit["b_int_exp_1d"].properties.array_spec.rank == 1
        assert self.explicit["b_int_exp_2d"].properties.array_spec.rank == 2
        assert self.explicit["b_int_exp_3d"].properties.array_spec.rank == 3
        assert self.explicit["b_int_exp_4d"].properties.array_spec.rank == 4
        assert self.explicit["b_int_exp_5d"].properties.array_spec.rank == 5

    def test_corank(self):
        assert self.explicit["b_int_exp_1d"].properties.array_spec.corank == 0
        assert self.explicit["b_int_exp_2d"].properties.array_spec.corank == 0
        assert self.explicit["b_int_exp_3d"].properties.array_spec.corank == 0
        assert self.explicit["b_int_exp_4d"].properties.array_spec.corank == 0
        assert self.explicit["b_int_exp_5d"].properties.array_spec.corank == 0

    def test_type(self):
        assert self.explicit["b_int_exp_1d"].properties.array_spec.type == "EXPLICIT"
        assert self.dummy["c_str_alloc_1d"].properties.array_spec.type == "DEFERRED"

    def test_if_array(self):
        assert self.explicit["const_int_arr"].properties.array_spec
        assert not self.explicit["dp"].properties.array_spec
