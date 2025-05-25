# SPDX-License-Identifier: GPL-2.0+

import numpy as np
from packaging.version import Version

try:
    import pyquadp as pyq

    PYQ_IMPORTED = True
except ImportError:
    PYQ_IMPORTED = False


"""
Map gfortran version to Mod file version
"""


def gfortran_mod_map(version):
    if version < Version("4.8.1"):
        return Version("9")
    elif version < Version("4.9.2"):
        return Version("10")
    elif version < Version("5.1.0"):
        return Version("12")
    elif version < Version("8.0.0"):
        return Version("14")
    elif version < Version("15.0.0"):
        return Version("15")
    elif version.major == 15:
        return Version("16")
    else:
        raise ValueError(f"Unknown gfortran version {version}")


def string_clean(string):
    if string is None:
        return
    if string.startswith("'") or string.startswith('"'):
        string = string[1:]
    if string.endswith("'") or string.endswith('"'):
        string = string[:-1]

    return string


def hextofloat(s, kind=4):
    # Given hex like parameter '0.12decde@9' returns 5065465344.0
    man, exp = s.split("@")
    exp = int(exp)
    decimal = man.index(".")
    negative = man[0] == "-"
    man = man[decimal + 1 :]
    man = man.ljust(exp, "0")
    man = man[:exp] + "." + man[exp:]
    man = man + "P0"
    if negative:
        man = "-" + man
    if PYQ_IMPORTED and kind == 16:
        return pyq.qfloat.fromhex(man)
    elif kind == 8:
        return np.double.fromhex(man)
    else:
        return float.fromhex(man)
