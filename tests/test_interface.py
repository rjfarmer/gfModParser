import os
import pytest
from pprint import pprint

import gfModParser as gf


@pytest.mark.benchmark
class TestComponents:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(os.path.join("tests", "build", "basic.mod"))
        self.dt = gf.Module(os.path.join("tests", "build", "dt.mod"))

        self.v = gf.Variables(self.mod)
        self.p = gf.Parameters(self.mod)
        self.proc = gf.Procedures(self.mod)
        self.dtypes = gf.DerivedTypes(self.dt)

    def test_parameters(self):
        assert "dp" in self.p
        assert not "sub_no_args" in self.p
        assert self.p["dp"].name == "dp"
        assert self.p["dp"].properties.parameter.value == 8
        assert self.p.value("dp") == 8
        assert self.p.type("dp") == "INTEGER"
        assert self.p.kind("dp") == 4
        assert not self.p.array("dp").is_array

    def test_variables(self):
        assert "a_int" in self.v
        assert not "sub_no_args" in self.v
        assert self.v["a_int"].name == "a_int"
        assert self.v.type("a_int") == "INTEGER"
        assert self.v.kind("a_int") == 4
        assert not self.v.array("a_int").is_array
        assert not "asfdfgsf" in self.v
        with pytest.raises(KeyError):
            _ = self.v["sadsad"].name

    def test_procedures(self):
        assert "sub_no_args" in self.proc
        assert not "dp" in self.proc
        assert self.proc["sub_no_args"].name == "sub_no_args"

        assert self.proc.result("sub_no_args") is None
        assert self.proc.result("func_int_in").name == "func_int_in"
        assert self.proc.result("func_result").name == "z"

        args = self.proc.arguments("func_result")
        assert args["y"].name == "y"
        assert args["x"].name == "x"

        assert len(self.proc.arguments("sub_no_args")) == 0

    def test_feedback(self):
        arg = self.proc.arguments("func_result")["y"]

        assert arg in self.v
        assert self.v[arg].name == "y"
        assert self.v.type(arg) == "INTEGER"

    def test_dt(self):
        assert "S_struct_basic" in self.dtypes
        assert not "s_struct_basic" in self.dtypes

        assert self.dtypes["S_struct_basic"].name == "S_struct_basic"

        comps = self.dtypes.components("S_struct_basic")

        assert len(comps) == 9

        assert comps["a_int"].name == "a_int"
