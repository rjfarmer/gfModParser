# SPDX-License-Identifier: GPL-2.0+

import subprocess
import os


def pytest_configure(config):
    try:
        os.mkdir(os.path.join("tests", "build"))
    except FileExistsError:
        pass
    subprocess.call(["make", "all"], shell=True, cwd="tests")
