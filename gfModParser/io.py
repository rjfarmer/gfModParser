# SPDX-License-Identifier: GPL-2.0+

import gzip


def read_compressed(filename):
    with gzip.open(filename) as f:
        data = f.read().decode()

    return data


def read_uncompressed(filename):
    with open(filename, "r") as f:
        data = f.read()

    return data


def read_compressed_header(filename):
    with gzip.open(filename) as f:
        data = f.readline().decode()

    return data


def read_uncompressed_header(filename):
    with open(filename, "r") as f:
        data = f.readline()

    return data
