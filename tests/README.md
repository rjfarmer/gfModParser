
# Test suite

## src folder

The ``src/`` folder contains raw Fortran code. Each file must be standalone (to simpliy building), if mulitple modules are needed then list them all in the same file.

All code MUST be in a module

All code MUST have a .f90 file extension.

File names SHOULD either describe the feature (``arrays.f90``) or a Github bug (``GH-1.f90``)

Files MUST be licensed under a open source license.

## txt folder

This contains pre-compiled Fortran modules. The prefered way for testing is to have the Fortran file (so we can recompile with different versions of the compilier). But
sometimes the build process would be too complex to insert into the test suite, so the pre-compiled files can be shipped. These MUST be plain text, so after compilation extract the file:

````shell
gunzip < file.mod > file.mod.txt
````

We don't want the ``.mod`` themselves as people can sneak in malicious code via binary-encoded files in test suites (see the [xz attack](https://en.wikipedia.org/wiki/XZ_Utils_backdoor)). So all files MUST be plain text.

Files MUST have the ``.mod.txt`` file extensions.

Files MUST also be listed in the ``txt/README`` file with where they came from (so we can rebuild them when needed)

Files MUST be licensed under a open source license.


# Tests

The tests themselves MUST exist in the top level ``tests/`` folder and have a file prefix of ``test_``. These should be broken down by either the input ``.f90`` or ``.mod.txt`` file or general Fortran feature.

Files should start with:

````python
# SPDX-License-Identifier: GPL-2.0+

import pytest
import os

import gfModParser as gf


class TestXXXX:
    @pytest.fixture(autouse=True)
    def load(self):
        # Note use of os.path.join for Windows testing
        self.mod = gf.module(os.path.join("tests", "build", "file.mod"))

        # mod.txt files are loaded the same way as a normal .mod file
        self.mod2 = gf.module(os.path.join("tests", "src", "file.mod.txt"))

````

Where ``TestXXXX`` is set to a apprioate name for the features being tested

Some tests may be repetivtive (when testing many combinations of things), so SHOULD be skipped when doing computing the coverage:

````python
try:
    coverage = os.environ["PYTEST_COVERAGE"] == "1"
except KeyError:
    coverage = False

@pytest.mark.skipif(coverage, reason="Skip when running coverage")
class TestXXXX:
````