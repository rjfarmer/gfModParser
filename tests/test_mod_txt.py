# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint
import pathlib

import gfModParser as gf


# Modules where we have the uncompressed text version of the module

files = [
    "accurate_sum_auto_diff_star_order1.mod.txt",
    "gyre_mesa_m.mod.txt",
    "num_lib.mod.txt",
    "utils_def.mod.txt",
    "accurate_sum.mod.txt",
    "ionization_def.mod.txt",
    "pulse.mod.txt",
    "utils_dict.mod.txt",
    "auto_diff.mod.txt",
    "ionization_lib.mod.txt",
    "rates_def.mod.txt",
    "utils_idict.mod.txt",
    "chem_def.mod.txt",
    "kap_def.mod.txt",
    "rates_lib.mod.txt",
    "utils_lib.mod.txt",
    "chem_lib.mod.txt",
    "kap_lib.mod.txt",
    "star_data_def.mod.txt",
    "utils_nan_dp.mod.txt",
    "colors_def.mod.txt",
    "net_def.mod.txt",
    "star_data_lib.mod.txt",
    "utils_nan.mod.txt",
    "colors_lib.mod.txt",
    "net_lib.mod.txt",
    "star_def.mod.txt",
    "utils_nan_qp.mod.txt",
    "eos_def.mod.txt",
    "neu_def.mod.txt",
    "star_lib.mod.txt",
    "utils_nan_sp.mod.txt",
    "eos_lib.mod.txt",
    "neu_lib.mod.txt",
    "star_pgstar.mod.txt",
    "utils_openmp.mod.txt",
    "forum_m.mod.txt",
    "num_def.mod.txt",
    "turb.mod.txt",
    "utils_system.mod.txt",
]


class TestModTxt:
    def test_load(self):
        for i in files:
            m = gf.module(pathlib.PurePath("tests").joinpath("txt", i))
            assert len(m.keys()) > 0

    def test_missing(self):
        with pytest.raises(FileNotFoundError):
            m = gf.module("xxxxx.mod")
