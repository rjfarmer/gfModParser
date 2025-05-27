# SPDX-License-Identifier: GPL-2.0+

import subprocess
import os
from packaging.version import Version


def pytest_configure(config):
    """This is run when pytest is setting up in the controller process and in the workers too"""
    if hasattr(config, "workerinput"):
        # prevent workers to run the same code
        return

    try:
        os.mkdir(os.path.join("tests", "build"))
    except FileExistsError:
        pass
    subprocess.call(["make", "-f", "Makefile", "all"], cwd="tests")

    if gfortran_version().major >= 15:
        subprocess.call(["make", "-f", "Makefile15", "all"], cwd="tests")


def gfortran_version():
    # Only compile these if we have gfortran 15 or later
    gf_version = (
        subprocess.run(["gfortran", "-dumpversion"], capture_output=True)
        .stdout.strip()
        .decode()
    )

    # Linux and macs we get the major version windows gives us a full string
    return Version(gf_version)
