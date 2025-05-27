import os
import pytest
from pprint import pprint

import gfModParser as gf

filename = os.path.join("tests", "build", "unsign.mod")


@pytest.mark.skipif(not os.path.exists(filename), reason="Skip when running coverage")
class TestUnsigned:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.Module(filename)
