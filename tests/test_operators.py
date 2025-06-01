# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
import copy
from pprint import pprint
import operator

import gfModParser as gf

mod = gf.Module(os.path.join("tests", "build", "face.mod"))


class TestOperators:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "face.mod"))

    def test_interfaces(self):
        assert list(self.mod.interface.keys()) == ["PLUS", "MINUS", "PARENTHESES"]
        assert list(self.mod.interface["PLUS"]) == [2, 3]
        assert list(self.mod.interface["MINUS"]) == [4]
        assert list(self.mod.interface["PARENTHESES"]) == [5]

    def test_interfaces_op(self):
        assert mod.interface.op("MINUS") == operator.__sub__

    def test_operator(self):
        assert list(self.mod.operator.keys()) == ["myun"]
        assert list(self.mod.operator["myun"]) == [6]
        assert self.mod[self.mod.operator["myun"][0]].name == "my_unnary"

    def test_generics(self):
        assert list(self.mod.generic.keys()) == ["convert", "my_type"]
        assert list(self.mod.generic["convert"]) == [7, 8, 9, 10, 11]
