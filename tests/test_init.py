# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
import copy
from pprint import pprint

import gfModParser as gf


class TestInit:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "basic.mod"))

    def test_in(self):
        assert "a_int" in self.mod

    def test_str(self):
        assert "basic.mod" in str(self.mod)

    def test_repr(self):
        f = os.path.join("tests", "build", "basic.mod")
        assert repr(self.mod) == f"module('{f}')"

    def test_bad_version(self):
        m2 = copy.deepcopy(self.mod)
        m2._version = -99

        with pytest.raises(ValueError):
            m2._checks()

    def test_bad_compiler(self):
        m2 = copy.deepcopy(self.mod)
        m2.header = m2.header.replace("GFORTRAN", "A DIFFERENT COMPILER")

        with pytest.raises(ValueError):
            m2._checks()

    def test_dir(self):
        assert all([i for i in self.mod.keys() if i in dir(self.mod)])

    def test_not_in(self):
        with pytest.raises(KeyError):
            self.mod["xxxx"]

        assert not "xxx" in self.mod._mod._symbols
