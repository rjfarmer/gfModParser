# SPDX-License-Identifier: GPL-2.0+

import gzip


def read_compressed(filename) -> str:
    with gzip.open(filename) as f:
        data = f.read().decode()

    return data


def read_uncompressed(filename) -> str:
    with open(filename, "r", encoding="utf8") as f:
        data = f.read()

    return data


def read_compressed_header(filename) -> list[str]:
    with gzip.open(filename) as f:
        data = f.readline().decode()

    return data


def read_uncompressed_header(filename) -> list[str]:
    with open(filename, "r", encoding="utf8") as f:
        data = f.readline()

    return data
