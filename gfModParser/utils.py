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
    if "@" in s:
        man, exp = s.split("@")
        exp = int(exp)
    else:
        man = s
        exp = 0

    if PYQ_IMPORTED and kind == 16:
        return pyq.qfloat.fromhex(man) * 16**exp
    elif kind == 8:
        return np.double.fromhex(man) * 16**exp
    else:
        return float.fromhex(man) * 16**exp


def dtype(type, kind, len=-1):
    if type == "REAL":
        if kind == 4:
            return np.dtype(np.float32)
        elif kind == 8:
            return np.dtype(np.float64)
        elif kind == 16:
            return np.dtype(np.float128)
    elif type == "INTEGER":
        if kind == 4:
            return np.dtype(np.int32)
        elif kind == 8:
            return np.dtype(np.int64)
        elif kind == 16:
            return np.dtype(np.int128)
    elif type == "UNSIGNED":
        if kind == 4:
            return np.dtype(np.uint32)
        elif kind == 8:
            return np.dtype(np.uint64)
        elif kind == 16:
            return np.dtype(np.uint128)
    elif type == "CHARACTER":
        return np.dtype(f"S{len}")
    elif type == "COMPLEX":
        if kind == 4:
            return np.dtype(np.complex64)
        elif kind == 8:
            return np.dtype(np.complex128)
        elif kind == 16:
            return np.dtype(np.complex256)
    elif type == "LOGICAL":
        return np.dtype(np.int32)
    else:
        raise NotImplementedError(f"Type={type} kind={kind}")


def bracket_split(string):
    def _helper(substring):
        items = []
        tmp = []
        for item in substring:
            if item == "(":
                result, closeparen = _helper(substring)
                if not closeparen:
                    raise ValueError("Unbalanced parentheses")
                items.append(result)
            elif item == ")":
                t = "".join(tmp).strip()
                if len(t):
                    items.append(t)
                return items, True
            else:
                if item != " ":
                    tmp.append(item)
                else:
                    t = "".join(tmp).strip()
                    if len(t):
                        items.append(t)
                        tmp = []
        return items, False

    return _helper(iter(string))[0]
