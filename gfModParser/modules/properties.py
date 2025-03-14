# SPDX-License-Identifier: GPL-2.0+
import functools
import pyparsing

from . import attributes
from . import components


class Properties:
    """
    Stores properties of an object
    """

    def __init__(self, properties, version):
        self._raw = properties
        self.version = version
        self._properties = None
        self._components = None

    def _load(self):
        p = pyparsing.OneOrMore(pyparsing.nestedExpr()).parseString(self._raw)

        self._properties = p[0]

        self._offset1 = 0
        self._offset2 = 0
        if isinstance(self._properties[2], str):
            self._offset1 = 1
        if self.attributes.is_parameter:
            self._offset2 = 1

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
        return self._properties[2]

    @property
    def typespec(self):
        if self._properties is None:
            self._load()
        return self._properties[2 + self._offset1]

    @property
    def namespace(self):
        if self._properties is None:
            self._load()
        return self._properties[3 + self._offset1]

    @property
    def common_symbol(self):
        if self._properties is None:
            self._load()
        return self._properties[4 + self._offset1]

    @property
    def formal_argument(self):
        if self._properties is None:
            self._load()
        return self._properties[5 + self._offset1]

    @property
    def parameter(self):
        if self._properties is None:
            self._load()
        return self._properties[6 + self._offset1]

    @property
    def array_spec(self):
        if self._properties is None:
            self._load()
        return self._properties[7 + self._offset1 + self._offset2]

    @property
    def symbol_reference(self):
        if self._properties is None:
            self._load()
        if not any([i == "CRAY_POINTER" for i in self.attributes]):
            return self._properties[8 + self._offset1 + self._offset2]

    @property
    def cray_pointer_reference(self):
        if self._properties is None:
            self._load()
        if any([i == "CRAY_POINTER" for i in self.attributes]):
            return self._properties[9 + self._offset1 + self._offset2]

    @property
    def derived(self):
        if self._properties is None:
            self._load()
        return self._properties[10 + self._offset1 + self._offset2]

    @property
    def actual_argument(self):
        if self._properties is None:
            self._load()
        return self._properties[11 + self._offset1 + self._offset2]

    @property
    def namelist(self):
        if self._properties is None:
            self._load()
        return self._properties[12 + self._offset1 + self._offset2]

    @property
    def intrinsic(self):
        if self._properties is None:
            self._load()
        return self._properties[13 + self._offset1 + self._offset2]

    @property
    def intrinsic_symbol(self):
        if self._properties is None:
            self._load()
        if len(self._properties) >= 14 + self._offset1 + self._offset2:
            return self._properties[14 + self._offset1 + self._offset2]

    @property
    def hash(self):
        if self._properties is None:
            self._load()
        if len(self._properties) >= 15 + self._offset1 + self._offset2:
            return self._properties[15 + self._offset1 + self._offset2]

    @property
    def simd(self):
        if self._properties is None:
            self._load()
        if len(self._properties) >= 16 + self._offset1 + self._offset2:
            return self._properties[16 + self._offset1 + self._offset2]
