[![Continuous Integration](https://github.com/rjfarmer/gfmodparser/actions/workflows/linux.yml/badge.svg)](https://github.com/rjfarmer/gfmodparser/actions/workflows/linux.yml)
[![Coverage Status](https://coveralls.io/repos/github/rjfarmer/gfmodparser/badge.svg?branch=main)](https://coveralls.io/github/rjfarmer/gfmodparser?branch=main)
[![PyPI version](https://badge.fury.io/py/gfmodparser.svg)](https://badge.fury.io/py/gfmodparser)
[![Python versions](https://img.shields.io/pypi/pyversions/gfmodparser.svg)](https://img.shields.io/pypi/pyversions/gfmodparser.svg)
[![gfortran versions](https://img.shields.io/badge/gfortran-8%7C9%7C10%7C11%7C12%7C13-blue)](https://img.shields.io/badge/gfortran-8%7C9%7C10%7C11%7C12%7C13-blue)
![PyPI - Downloads](https://img.shields.io/pypi/dm/gfmodparser)


# gfModParser
Parser for gfortran's Fortran module file format. 

Requires gfortran>=8.0, Works with python >= 3.9

## Build
Installing locally:
````bash
python -m pip install .
````

or install via pypi
````bash
python -m pip install --upgrade --user gfModParser
````

## Development
````bash
python -m pip install .[dev]
python -m pip install .[test]
````




## License

gfModParser is distributed under the GPLv2 or later.

The following files are from https://aoterodelaroza.github.io/devnotes/modern-fortran-makefiles/ and distributed under GPLv3.
- ``tests/Makefile``
- ``tests/src/Makefile``
- ``tests/src/makedepf08.awk``
