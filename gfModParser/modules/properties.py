# SPDX-License-Identifier: GPL-2.0+
import functools
import pyparsing

from . import attributes


class Properties:
    """
    Stores properties of an object
    """

    def __init__(self, properties):
        p = properties.replace("\n", " ") + ")"
        p = pyparsing.OneOrMore(pyparsing.nestedExpr()).parseString(p)

        self._properties = p[0]

        self._offset1 = 0
        self._offset2 = 0
        if isinstance(self._properties[2], str):
            self._offset1 = 1
        if self.attributes.is_parameter:
            self._offset2 = 1

    @functools.cached_property
    def attributes(self):
        return attributes.Attributes(self._properties[0])

    @functools.cached_property
    def components(self):
        return self._properties[1]

    @functools.cached_property
    def component_access(self):
        return self._properties[2]

    @functools.cached_property
    def typespec(self):
        return self._properties[2 + self._offset1]

    @functools.cached_property
    def namespace(self):
        return self._properties[3 + self._offset1]

    @functools.cached_property
    def common_symbol(self):
        return self._properties[4 + self._offset1]

    @functools.cached_property
    def formal_argument(self):
        return self._properties[5 + self._offset1]

    @functools.cached_property
    def parameter(self):
        return self._properties[6 + self._offset1]

    @functools.cached_property
    def array_spec(self):
        return self._properties[7 + self._offset1 + self._offset2]

    @functools.cached_property
    def symbol_reference(self):
        if not any([i == "CRAY_POINTER" for i in self.attributes]):
            return self._properties[8 + self._offset1 + self._offset2]

    @functools.cached_property
    def cray_pointer_reference(self):
        if any([i == "CRAY_POINTER" for i in self.attributes]):
            return self._properties[9 + self._offset1 + self._offset2]

    @functools.cached_property
    def derived(self):
        return self._properties[10 + self._offset1 + self._offset2]

    @functools.cached_property
    def actual_argument(self):
        return self._properties[11 + self._offset1 + self._offset2]

    @functools.cached_property
    def namelist(self):
        return self._properties[12 + self._offset1 + self._offset2]

    @functools.cached_property
    def intrinsic(self):
        return self._properties[13 + self._offset1 + self._offset2]

    @functools.cached_property
    def intrinsic_symbol(self):
        if len(self._properties) >= 14 + self._offset1 + self._offset2:
            return self._properties[14 + self._offset1 + self._offset2]

    @functools.cached_property
    def hash(self):
        if len(self._properties) >= 15 + self._offset1 + self._offset2:
            return self._properties[15 + self._offset1 + self._offset2]

    @functools.cached_property
    def simd(self):
        if len(self._properties) >= 16 + self._offset1 + self._offset2:
            return self._properties[16 + self._offset1 + self._offset2]
