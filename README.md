[![Continuous Integration](https://github.com/rjfarmer/gfmodparser/actions/workflows/linux.yml/badge.svg)](https://github.com/rjfarmer/gfmodparser/actions/workflows/linux.yml)
[![Coverage Status](https://coveralls.io/repos/github/rjfarmer/gfModParser/badge.svg)](https://coveralls.io/github/rjfarmer/gfModParser)
[![PyPI version](https://badge.fury.io/py/gfmodparser.svg)](https://badge.fury.io/py/gfmodparser)
[![Python versions](https://img.shields.io/pypi/pyversions/gfmodparser.svg)](https://img.shields.io/pypi/pyversions/gfmodparser.svg)
[![gfortran versions](https://img.shields.io/badge/gfortran-8%7C9%7C10%7C11%7C12%7C13%7C14%7C15-blue)](https://img.shields.io/badge/gfortran-8%7C9%7C10%7C11%7C12%7C13%7C14%7C15-blue)
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

or install via PyPi
````bash
python -m pip install --upgrade --user gfModParser
````


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

## Usage

Basic usage involes loading a module then exploring what it offers:

````python
import gfModParser as gf
mod = gf.Module("fortran.mod")

# Get list of all available things in the module
mod.keys()

# Extract a single variable named 'a_variable'
mod['a_variable']
````

The ``Module`` class provides all the information known about a thing, but can be complicated to use. So there exists some convienance classes to make life easier:

````python
import gfModParser as gf
mod = gf.Module("fortran.mod")

# Stores all module level varibles
variables = gf.Variables(mod)

# Stores all module level parameters
parameters = gf.Parameters(mod)

# Stores all module level procedures
procedures = gf.Procedures(mod)

# Stores all module level derived types
dt = gf.DerivedTypes(mod)
````

Each acts like a dict, with a ``keys()`` function to list available members and ``__contains__`` for lookup. Each class is accessed like a dict so ``variables['a_variable']`` is the same as ``mod['a_variable']``


### Variables
The ``Variables`` class also contains functions for quick reference to the ``type`` and ``kind`` of a variable

````python
variables.type('a_variable')
variables.kind('a_variable')
````

and ``array`` provides information on its array status:

````python
variables.array('a_variable').is_array
variables.array('a_variable').shape # etc
````

### Parameter
Has the same fucntions as ``Variables`` but also a method for returning the value of the parameter:

````python
parameters.value('a_parameter')
````

### Procedures
The return value of a Fortran function (None if a subroutine) can be accessed via:

````python
result = procedures.result('a_function')

# This can be fed back into Variables
variables.type(result)
````

Arguments to the procedure can be accessed via, and returnd as a dict:

````python
args = procedures.arguments('a_function')

# This can be fed back into Variables class
variables.type(result['a_argument'])
````

### Derived types

The components of a derived type can be found with (returned as a dict):

````python
components = dt.components('A_dt')
````

Note the use of a captial first letter, this is required to find the definition. Also a derived type component is not like a function argument and can not be fed back into the ``Variables`` class (they are not stored in the same way as procedure arguments).




## License

gfModParser is distributed under the GPLv2 or later.
