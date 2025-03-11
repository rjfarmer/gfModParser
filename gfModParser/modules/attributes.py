# SPDX-License-Identifier: GPL-2.0+

from .. import utils

_all = set(
    [
        i.lower()
        for i in [
            "ABSTRACT",
            "ALLOCATABLE",
            "ALLOC_COMP",
            "ALWAYS_EXPLICIT",
            "ARRAY_OUTER_DEPENDENCY",
            "ARTIFICIAL",
            "DIMENSION",
            "ELEMENTAL",
            "EXTERNAL",
            "FUNCTION",
            "GENERIC",
            "IMPLICIT_PURE",
            "IN_NAMELIST",
            "IS_CLASS",
            "POINTER",
            "POINTER_COMP",
            "PRIVATE_COMP",
            "PROCEDURE",
            "PROC_POINTER",
            "PROC_POINTER_COMP",
            "PROTECTED",
            "PURE",
            "RECURSIVE",
            "SUBROUTINE",
            "TARGET",
            "VTAB",
            "VTYPE",
        ]
    ]
)


class Attributes:

    def __init__(self, attributes):
        self._attributes = attributes

        self.flavor = utils.string_clean(self._attributes[0])
        self.intent = utils.string_clean(self._attributes[1])
        self.procedure = utils.string_clean(self._attributes[2])
        self.if_source = utils.string_clean(self._attributes[3])
        self.save = utils.string_clean(self._attributes[4])
        self._external_attribute = int(self._attributes[5])
        self._extension = int(self._attributes[6])
        self._attributes = set([utils.string_clean(i) for i in self._attributes[7:]])

    @property
    def external_attribute(self):
        return self._external_attribute == 1

    @property
    def extension(self):
        return self._extension == 1

    @property
    def attributes(self):
        return self._attributes

    @property
    def is_parameter(self):
        return self.flavor == "PARAMETER"

    @property
    def is_variable(self):
        return self.flavor == "VARIABLE"

    @property
    def is_procedure(self):
        return self.flavor == "PROCEDURE"

    @property
    def is_derived(self):
        return self.flavor == "DERIVED"

    @property
    def is_module(self):
        return self.flavor == "MODULE"

    def __dir__(self):
        return list(_all)

    def __getattr__(self, key):
        if key in _all:
            return key.upper() in self._attributes
        else:
            raise AttributeError(f"Key not found {key}")
