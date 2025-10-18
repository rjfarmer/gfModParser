# SPDX-License-Identifier: GPL-2.0+
from packaging.version import Version
from functools import cached_property


from typing import Type, Any


from gfModParser import utils

from . import attributes
from . import components
from . import expressions
from . import simds
from . import namespaces
from . import procedures
from . import arrays
from . import namelists


class Properties:
    """
    Stores properties of an object
    """

    def __init__(self, properties, *, version: Version) -> None:
        self._raw = properties
        self.version = version
        self._properties: list[Any] = []

        self._comp_access = ""
        self._exp_type = None

    def _load(self) -> None:
        self._properties = []
        p = utils.bracket_split(self._raw)
        self._properties = p[0]

        if isinstance(self._properties[2], str):
            self._comp_access = self._properties[2]
            _ = self._properties.pop(2)
        if self.attributes.is_parameter:
            self._exp_type = self._properties[6]
            _ = self._properties.pop(6)

    @property
    def attributes(self) -> attributes.Attributes:
        if not len(self._properties):
            self._load()
        return attributes.Attributes(self._properties[0], version=self.version)

    @cached_property
    def components(self) -> components.Components:
        if not len(self._properties):
            self._load()

        return components.Components(self._properties[1], version=self.version)

    @property
    def component_access(self):
        if not len(self._properties):
            self._load()
        return self._comp_access

    @property
    def typespec(self) -> expressions.typespec:
        if not len(self._properties):
            self._load()
        return expressions.typespec(self._properties[2], version=self.version)

    @property
    def namespace(self) -> namespaces.namespace:
        if not len(self._properties):
            self._load()
        return namespaces.namespace(self._properties[3], version=self.version)

    @property
    def common_symbol(self) -> int:
        if not len(self._properties):
            self._load()
        return int(self._properties[4])

    @property
    def formal_argument(self) -> procedures.Arglist:
        """
        Symbol references for the procedure arguments
        """
        if not len(self._properties):
            self._load()
        return procedures.Arglist(self._properties[5], version=self.version)

    @property
    def exp_type(self) -> expressions.Expression | None:
        if not len(self._properties):
            self._load()

        if self._exp_type is not None:
            return expressions.Expression(self._exp_type, version=self.version)
        return None

    @property
    def array_spec(self) -> arrays.arrayspec:
        if not len(self._properties):
            self._load()
        return arrays.arrayspec(self._properties[6], version=self.version)

    @property
    def symbol_reference(self) -> int:
        """
        0 if a subroutine, else the symbol reference for a function result
        """
        if not len(self._properties):
            self._load()
        if not any([i == "CRAY_POINTER" for i in self.attributes.attributes]):
            return int(self._properties[7])
        return -1

    @property
    def cray_pointer_reference(self) -> int:
        if not len(self._properties):
            self._load()
        if any([i == "CRAY_POINTER" for i in self.attributes.attributes]):
            return int(self._properties[7])
        return -1

    @property
    def derived(self) -> namespaces.derived_ns:
        if not len(self._properties):
            self._load()
        return namespaces.derived_ns(self._properties[8], version=self.version)

    @property
    def actual_argument(self) -> procedures.Arglist:
        if not len(self._properties):
            self._load()
        return procedures.Arglist(self._properties[9], version=self.version)

    @property
    def namelist(self) -> namelists.Namelist | None:
        if not len(self._properties):
            self._load()
        if self.attributes.is_namelist:
            return namelists.Namelist(self._properties[10], version=self.version)
        return None

    @property
    def intrinsic(self) -> bool:
        if not len(self._properties):
            self._load()
        return self._properties[11] == 1

    @property
    def intrinsic_symbol(self) -> bool:
        if not len(self._properties):
            self._load()
        if len(self._properties) > 12:
            return self._properties[12] == 1
        return False

    @property
    def hash(self) -> int:
        if not len(self._properties):
            self._load()
        if len(self._properties) > 13:
            return int(self._properties[13])
        return -1

    @property
    def simd(self) -> simds.simd_dec | None:
        if not len(self._properties):
            self._load()
        if len(self._properties) >= 14:
            return simds.simd_dec(self._properties[14], version=self.version)
        return None
