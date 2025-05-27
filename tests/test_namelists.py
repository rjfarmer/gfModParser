# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestNamelists:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "namelist.mod"))

    def test_nml(self):
        nml = self.mod["namelist1"]
        assert nml.properties.attributes.is_namelist
        elements = nml.properties.namelist
        assert len(elements) == 4
        assert self.mod[elements[0]].name == "a_int"

    def test_arg(self):
        nml = self.mod["namelist1"]
        elements = nml.properties.namelist
        assert self.mod[elements[0]].properties.attributes.in_namelist
        assert not self.mod["dp"].properties.attributes.in_namelist
