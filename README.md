[![Continuous Integration](https://github.com/rjfarmer/gfmodparser/actions/workflows/linux.yml/badge.svg)](https://github.com/rjfarmer/gfmodparser/actions/workflows/linux.yml)
[![Coverage Status](https://coveralls.io/repos/github/rjfarmer/gfModParser/badge.svg)](https://coveralls.io/github/rjfarmer/gfModParser)
[![PyPI version](https://badge.fury.io/py/gfmodparser.svg)](https://badge.fury.io/py/gfmodparser)
[![Python versions](https://img.shields.io/pypi/pyversions/gfmodparser.svg)](https://img.shields.io/pypi/pyversions/gfmodparser.svg)
[![gfortran versions](https://img.shields.io/badge/gfortran-8%7C9%7C10%7C11%7C12%7C13-blue)](https://img.shields.io/badge/gfortran-8%7C9%7C10%7C11%7C12%7C13-blue)
![PyPI - Downloads](https://img.shields.io/pypi/dm/gfmodparser)


# gfModParser
Parser for gfortran's Fortran module file format. 

Requires gfortran>=8.0, Works with python >= 3.9

GFortran module source code https://github.com/gcc-mirror/gcc/blob/master/gcc/fortran/module.cc

## Build
Installing locally:
````bash
python -m pip install .
````

or install via pypi
````bash
python -m pip install --upgrade --user gfModParser
````

Package is not yet available on PyPi

## Development
````bash
python -m pip install .[dev] # Development tools
python -m pip install .[test] # Tools needs for running pytest
````

``black`` is used to lint the Python code, so before starting development install the pre-commit hook:

````bash
pre-commit install
````

This will then run ``black`` for the Python and ``zizmor`` for the workflows yml files.

````bash
python -m pytest --cov gfModParser --cov-report html # Generate coverage report
````


## License

gfModParser is distributed under the GPLv2 or later.

The following files are from https://aoterodelaroza.github.io/devnotes/modern-fortran-makefiles/ and distributed under GPLv3.
- ``tests/Makefile``
- ``tests/src/Makefile``
- ``tests/src/makedepf08.awk``
