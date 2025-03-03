# SPDX-License-Identifier: GPL-2.0+

import os
import pytest
from pprint import pprint

import gfModParser as gf


class TestProperties:
    @pytest.fixture(autouse=True)
    def load(self):
        self.mod = gf.module("tests/build/basic.mod")
