# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
import copy
from pprint import pprint
import operator
from packaging.version import Version

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

        plus = self.mod.interface["PLUS"]
        assert plus.values == [2, 3]
        assert str(plus) == "[2, 3]"
        assert repr(plus) == "[2, 3]"
        assert "2" in plus
        assert plus[0] == 2

    def test_interface_views(self):
        values = list(self.mod.interface.values())
        items = list(self.mod.interface.items())

        assert len(values) == 3
        assert len(items) == 3
        assert items[0][0] == "PLUS"

    def test_interfaces_op(self):
        assert mod.interface.op("MINUS") == operator.__sub__

    def test_operator(self):
        assert list(self.mod.operator.keys()) == ["myun"]
        assert list(self.mod.operator["myun"]) == [6]
        assert self.mod[self.mod.operator["myun"][0]].name == "my_unnary"

    def test_operator_views(self):
        values = list(self.mod.operator.values())
        items = list(self.mod.operator.items())

        assert len(values) == 1
        assert len(items) == 1
        assert items[0][0] == "myun"
        assert list(items[0][1]) == [6]

    def test_operator_extract_cached(self):
        first = self.mod.operator.extract()
        second = self.mod.operator.extract()
        assert first is second

    def test_generics(self):
        assert list(self.mod.generic.keys()) == ["convert", "my_type"]
        assert list(self.mod.generic["convert"]) == [7, 8, 9, 10, 11]


class TestOperatorsDirect:
    def test_direct_extract_ignores_module_name(self):
        raw = "(('myun' 'face' 6) ('mybin' '' 7 8))"
        op = gf.modules.operators.Operators(raw, version=Version("16"))

        assert list(op.keys()) == ["myun", "mybin"]
        assert list(op["myun"]) == [6]
        assert list(op["mybin"]) == [7, 8]
