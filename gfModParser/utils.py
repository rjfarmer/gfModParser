# SPDX-License-Identifier: GPL-2.0+

import numpy as np
from packaging.version import Version
from typing import Any, Union

try:
    import pyquadp as pyq  # type: ignore[import-not-found]

    PYQ_IMPORTED = True
except ImportError:
    PYQ_IMPORTED = False


def gfortran_mod_map(version: Version) -> Version:
    """
    Map gfortran version to Mod file version
    """
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


def string_clean(string: str) -> str:
    if string is None:
        return ""
    if string.startswith("'") or string.startswith('"'):
        string = string[1:]
    if string.endswith("'") or string.endswith('"'):
        string = string[:-1]

    return string


def hextofloat(s: str, kind: int = 4) -> Union[float, np.double, "pyq.qfloat"]:
    # Given hex like parameter '0.12decde@9' returns 5065465344.0
    if "@" in s:
        man, e = s.split("@")
        exp = int(e)
    else:
        man = s
        exp = 0

    if kind == 16:
        if PYQ_IMPORTED:
            return pyq.qfloat.fromhex(man) * 16**exp
        else:
            raise ValueError("Please install pyQuadp to handle quad precision numbers")
    elif kind == 8:
        return np.double.fromhex(man) * 16**exp  # type: ignore[attr-defined]
    else:
        return float.fromhex(man) * 16**exp


def dtype(type, kind, len=-1) -> np.dtype:
    if type == "REAL":
        if kind == 4:
            return np.dtype(np.float32)
        elif kind == 8:
            return np.dtype(np.float64)
        elif kind == 16:
            return np.dtype(np.float128)
    elif type == "INTEGER":
        if kind == 1:
            return np.dtype(np.int8)
        elif kind == 2:
            return np.dtype(np.int16)
        elif kind == 4:
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

    raise NotImplementedError(f"Type={type} kind={kind}")


def bracket_split(string) -> list[Any]:
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
