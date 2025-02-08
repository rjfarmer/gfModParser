# SPDX-License-Identifier: GPL-2.0+

import numpy as np
import itertools


try:
    import pyquadp as pyq

    PYQ_IMPORTED = True
except ImportError:
    PYQ_IMPORTED = False


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
