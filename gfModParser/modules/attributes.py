# SPDX-License-Identifier: GPL-2.0+

from .. import utils

_all = set(
    [
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
)


class Attributes:

    def __init__(self, attributes):
        self._attributes = attributes
        self._attr = None

    @property
    def flavor(self):
        return utils.string_clean(self._attributes[0])

    @property
    def intent(self):
        return utils.string_clean(self._attributes[1])

    @property
    def procedure(self):
        return utils.string_clean(self._attributes[2])

    @property
    def if_source(self):
        return utils.string_clean(self._attributes[3])

    @property
    def save(self):
        return utils.string_clean(self._attributes[4])

    @property
    def external_attribute(self):
        return int(self._attributes[5]) == 1

    @property
    def extension(self):
        return int(self._attributes[6]) == 1

    @property
    def attributes(self):
        if self._attr is None:
            self._attr = set([utils.string_clean(i) for i in self._attributes[7:]])
        return self._attr

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
        # Get things defined by the getattr plus the properties (needs to dir the class though)
        return [i.lower() for i in _all] + dir(self.__class__)

    def __getattr__(self, key):
        if key.upper() in _all:
            return key.upper() in self.attributes
        else:
            raise AttributeError(f"Key not found {key}")
