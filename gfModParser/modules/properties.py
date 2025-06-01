# SPDX-License-Identifier: GPL-2.0+
import pyparsing

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

    def __init__(self, properties, *, version):
        self._raw = properties
        self.version = version
        self._properties = None
        self._components = None

        self._comp_access = None
        self._parameter = None

    def _load(self):
        p = pyparsing.OneOrMore(pyparsing.nestedExpr()).parseString(self._raw)
        self._properties = p[0]

        if isinstance(self._properties[2], str):
            self._comp_access = self._properties[2]
            _ = self._properties.pop(2)
        if self.attributes.is_parameter:
            self._parameter = self._properties[6]
            _ = self._properties.pop(6)

    @property
    def attributes(self):
        if self._properties is None:
            self._load()
        return attributes.Attributes(self._properties[0], version=self.version)

    @property
    def components(self):
        if self._properties is None:
            self._load()
        if self._components is None:
            self._components = components.Components(
                self._properties[1], version=self.version
            )

        return self._components

    @property
    def component_access(self):
        if self._properties is None:
            self._load()
        return self._comp_access

    @property
    def typespec(self):
        if self._properties is None:
            self._load()
        return expressions.typespec(self._properties[2], version=self.version)

    @property
    def namespace(self):
        if self._properties is None:
            self._load()
        return namespaces.namespace(self._properties[3], version=self.version)

    @property
    def common_symbol(self):
        if self._properties is None:
            self._load()
        return int(self._properties[4])

    @property
    def formal_argument(self):
        """
        Symbol references for the procedure arguments
        """
        if self._properties is None:
            self._load()
        return procedures.Arglist(self._properties[5], version=self.version)

    @property
    def parameter(self):
        if self._properties is None:
            self._load()
        if self._parameter is not None:
            return expressions.Expression(self._parameter, version=self.version)

    @property
    def array_spec(self):
        if self._properties is None:
            self._load()
        return arrays.arrayspec(self._properties[6], version=self.version)

    @property
    def symbol_reference(self):
        """
        0 if a subroutine, else the symbol reference for a function result
        """
        if self._properties is None:
            self._load()
        if not any([i == "CRAY_POINTER" for i in self.attributes.attributes]):
            return int(self._properties[7])

    @property
    def cray_pointer_reference(self):
        if self._properties is None:
            self._load()
        if any([i == "CRAY_POINTER" for i in self.attributes.attributes]):
            return int(self._properties[7])

    @property
    def derived(self):
        if self._properties is None:
            self._load()
        return namespaces.derived_ns(self._properties[8], version=self.version)

    @property
    def actual_argument(self):
        if self._properties is None:
            self._load()
        return procedures.Arglist(self._properties[9], version=self.version)

    @property
    def namelist(self):
        if self._properties is None:
            self._load()
        if self.attributes.is_namelist:
            return namelists.Namelist(self._properties[10], version=self.version)

    @property
    def intrinsic(self):
        if self._properties is None:
            self._load()
        return self._properties[11] == 1

    @property
    def intrinsic_symbol(self):
        if self._properties is None:
            self._load()
        if len(self._properties) > 12:
            return self._properties[12] == 1

    @property
    def hash(self):
        if self._properties is None:
            self._load()
        if len(self._properties) > 13:
            return int(self._properties[13])

    @property
    def simd(self):
        if self._properties is None:
            self._load()
        if len(self._properties) >= 14:
            return simds.simd(self._properties[14], version=self.version)
