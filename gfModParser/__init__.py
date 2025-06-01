# SPDX-License-Identifier: GPL-2.0+

import pathlib
from functools import cache

from . import io
from .modules import mod
from .modules.symbols import Symbol

__all__ = ["Module", "Variables", "Parameters", "Procedures", "DerivedTypes"]


class Module:
    def __init__(self, filename):
        self.filename = pathlib.Path(filename)

        if self.filename.suffixes == [".mod", ".txt"]:
            self.header = io.read_uncompressed_header(self.filename)
        else:
            self.header = io.read_compressed_header(self.filename)

        self._version = None
        self._checks()

    def _checks(self):
        if self.version < 15 or self.version > 16:
            raise ValueError(f"Unsupported module version {self.version}")

        if not "GFORTRAN" in self.header:
            raise ValueError("Only supports Gfortran modules")

        self._mod = mod.module(self.filename, version=self.version)

    @property
    def version(self):
        if self._version is None:
            self._version = int(self.header.split("'")[1])
        return self._version

    @property
    def interface(self):
        return self._mod.interface

    @property
    def operator(self):
        return self._mod.operator

    @property
    def generic(self):
        return self._mod.generic

    def keys(self):
        return self._mod.keys()

    def __contains__(self, key):
        return key in self._mod

    def __getitem__(self, key):
        return self._mod[key]

    def __dir__(self):
        return self._mod.__dir__()

    def __str__(self):
        return f"Module: {self.filename} Gfortran: {self.version}"

    def __repr__(self):
        return f"module('{self.filename}')"


class Variables:
    """
    Provides a high level interface to module level variables
    """

    def __init__(self, module):
        self.module = module

    @cache
    def keys(self):
        res = []
        for i in self.module.keys():
            if self.module[i].properties.attributes.is_variable:
                res.append(i)
        return set(res)

    def __contains__(self, key):
        if isinstance(key, str):
            return key in self.keys()
        elif isinstance(key, Symbol):
            return key.properties.attributes.is_variable

    def __getitem__(self, key):
        if key in self:
            if isinstance(key, str):
                return self.module[key]
            elif isinstance(key, Symbol):
                return key
        else:
            raise KeyError(f"Can't find {key} or its not a variable")

    def _id(self, key):
        if isinstance(key, str):
            return self.module[key].id
        elif isinstance(key, Symbol):
            return key.id

    @cache
    def type(self, key):
        """
        Return the Fortran type (INTEGER, REAL, LOGICAL, CHARACTER, etc)
        """
        if key in self:
            return self.module[self._id(key)].properties.typespec.type

    @cache
    def kind(self, key):
        """
        Returns the Fortran kind (1,4,8,16) its not formally the number of bytes but
        for gfortran can be treated as such
        """
        if key in self:
            return self.module[self._id(key)].properties.typespec.kind

    @cache
    def array(self, key):
        """
        Returns an array_spec object which stores information about if the variable
        is an array and if so, its shape, size etc
        """
        if key in self:
            return self.module[self._id(key)].properties.array_spec


class Parameters:
    """
    Provides a high level interface to module parameters
    """

    def __init__(self, module):
        self.module = module

    @cache
    def keys(self):
        res = []
        for i in self.module.keys():
            if self.module[i].properties.attributes.is_parameter:
                res.append(i)
        return set(res)

    def __getitem__(self, key):
        if key in self:
            return self.module[key]

    def __contains__(self, key):
        return key in self.keys()

    @cache
    def value(self, key):
        """
        Returns the parameter value
        """
        if key in self:
            return self.module[key].properties.parameter.value

    @cache
    def type(self, key):
        """
        Return the Fortran type (INTEGER, REAL, LOGICAL, CHARACTER, etc)
        """
        if key in self:
            return self.module[key].properties.typespec.type

    @cache
    def kind(self, key):
        """
        Returns the Fortran kind (1,4,8,16) its not formally the number of bytes but
        for gfortran can be treated as such
        """
        if key in self:
            return self.module[key].properties.typespec.kind

    @cache
    def array(self, key):
        """
        Returns an array_spec object which stores information about if the variable
        is an array and if so, its shape, size etc
        """
        if key in self:
            return self.module[key].properties.array_spec


class Procedures:
    """
    Provides a high level interface to module procedures
    """

    def __init__(self, module):
        self.module = module

    @cache
    def keys(self):
        res = []
        for i in self.module.keys():
            if self.module[i].properties.attributes.is_procedure:
                res.append(i)
        return set(res)

    def __getitem__(self, key):
        if key in self:
            return self.module[key]

    def __contains__(self, key):
        return key in self.keys()

    @cache
    def result(self, key):
        """
        Return the function result variable or None if subroutine

        This can be fed back into the Variables() class for easier accessing
        """
        if key in self:
            ref = self.module[key].properties.symbol_reference
            if ref > 0:
                return self.module[ref]

    @cache
    def arguments(self, key):
        """
        Returns a dict of the dummy arguments to the procedure

        These can be fed back indivdiually into the Variables() class for easier accessing
        """
        if key in self:
            ref = self.module[key].properties.formal_argument
            if ref:
                return {self.module[i].name: self.module[i] for i in ref}
            else:
                return {}


class DerivedTypes:
    """
    Provides a high level interface to module level derived type definitions
    """

    def __init__(self, module):
        self.module = module

    @cache
    def keys(self):
        res = []
        for i in self.module.keys():
            if self.module[i].properties.attributes.is_derived:
                res.append(i)
        return set(res)

    def __getitem__(self, key):
        if key in self:
            return self.module[key]

    def __contains__(self, key):
        return key in self.keys()

    @cache
    def components(self, key):
        """
        Returns a dict of the components of the derived type

        Note the key must have the first letter captialised to find the definition of the type
        """
        res = {}
        if key in self:
            ref = self.module[key]
            for component in ref.properties.components.keys():
                res[component] = ref.properties.components[component]
            return res
