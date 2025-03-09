# SPDX-License-Identifier: GPL-2.0+

from .. import utils


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
        if len(self._attributes) == 0:
            return None
        else:
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
    def is_subroutine(self):
        return "SUBROUTINE" in self.attributes

    @property
    def is_function(self):
        return "FUNCTION" in self.attributes

    @property
    def is_elemental(self):
        return "ELEMENTAL" in self.attributes

    @property
    def is_pure(self):
        return "PURE" in self.attributes

    @property
    def is_impure(self):
        return "IMPLICIT_PURE" in self.attributes
