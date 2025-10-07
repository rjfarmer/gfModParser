# SPDX-License-Identifier: GPL-2.0+

import gzip
from typing import List


def read_compressed(filename) -> str:
    with gzip.open(filename) as f:
        data = f.read().decode()

    return data


def read_uncompressed(filename) -> str:
    with open(filename, "r") as f:
        data = f.read()

    return data


def read_compressed_header(filename) -> List[str]:
    with gzip.open(filename) as f:
        data = f.readline().decode()

    return data


def read_uncompressed_header(filename) -> List[str]:
    with open(filename, "r") as f:
        data = f.readline()

    return data
