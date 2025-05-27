# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint
import pathlib
import sys

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

try:
    coverage = os.environ["PYTEST_COVERAGE"] == "1"
except KeyError:
    coverage = False


class TestModTxtbasic:
    def test_load(self):
        filename = "num_lib.mod.txt"
        m = gf.Module(pathlib.PurePath("tests").joinpath("txt", filename))
        assert m["anonymous_mixing"].properties.attributes.is_parameter

    def test_missing(self):
        with pytest.raises(FileNotFoundError):
            m = gf.Module("xxxxx.mod")


@pytest.mark.skipif(coverage, reason="Skip when running coverage")
class TestModTxtAll:
    @pytest.mark.parametrize("filename", files)
    def test_load(self, filename):
        m = gf.Module(pathlib.PurePath("tests").joinpath("txt", filename))
        for key in m.keys():
            try:
                p = m[key].properties.attributes.is_variable
            except Exception as e:
                if sys.version_info.major > 3 and sys.version_info.minor > 11:
                    e.add_note(f"Key: {key}")
                raise


@pytest.mark.skipif(coverage, reason="Skip when running coverage")
@pytest.mark.benchmark
class TestBenchMark:
    def test_load(self):
        filename = "rates_def.mod.txt"
        m = gf.Module(pathlib.PurePath("tests").joinpath("txt", filename))
        for key in m.keys():
            try:
                p = m[key].properties.attributes.is_variable
            except Exception as e:
                if sys.version_info.major > 3 and sys.version_info.minor > 11:
                    e.add_note(f"Key: {key}")
                raise
