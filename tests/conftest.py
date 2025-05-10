# SPDX-License-Identifier: GPL-2.0+

import subprocess
import os


def pytest_configure(config):
    """This is run when pytest is setting up in the controller process and in the workers too"""
    if hasattr(config, "workerinput"):
        # prevent workers to run the same code
        return
    try:
        os.mkdir(os.path.join("tests", "build"))
    except FileExistsError:
        pass
    subprocess.call(["make", "all"], shell=True, cwd="tests")
