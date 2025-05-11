# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestExpressions:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.module(os.path.join("tests", "build", "basic.mod"))

    def test_type(self):
        assert self.mod["dp"].properties.parameter.type == "INTEGER"

    def test_typespec(self):
        assert (
            self.mod["dp"].properties.parameter.typespec.type
            == self.mod["dp"].properties.parameter.type
        )

    def test_kind(self):
        assert self.mod["dp"].properties.parameter.rank == 0

    def test_str(self):
        assert str(self.mod["dp"].properties.parameter) == "INTEGER"
        assert repr(self.mod["dp"].properties.parameter) == "INTEGER"
