# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestTypeboundProc:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "proc_ptrs.mod"))

    def test_pass(self):
        pp = self.mod["Ppptr"].properties.components["p_func_pass"].proc_pointer

        assert pp.access == "PUBLIC"
        assert pp.overridable == "OVERRIDABLE"
        assert not pp.nopass
        assert pp.is_generic == "SPECIFIC"
        assert pp.ppc == "PPC"
        assert pp.pass_arg == ""
        assert pp.pass_arg_num > 0

    def test_nopass(self):
        pp = self.mod["Ppptr"].properties.components["p_func_func_run_ptr"].proc_pointer
        assert pp.nopass
        assert pp.pass_arg == ""
        assert pp.pass_arg_num == 0

    def test_pass_self(self):
        pp = self.mod["Ppptr"].properties.components["p_func_pass2"].proc_pointer
        assert not pp.nopass
        assert pp.pass_arg_num > 0
