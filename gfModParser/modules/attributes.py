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
        self.external_attribute = int(self._attributes[5])
        self.extension = int(self._attributes[6])
        self.attributes = set([utils.string_clean(i) for i in self._attributes[7:]])

    @property
    def is_parameter(self):
        return self.flavor == 'PARAMETER'
    
    @property
    def is_variable(self):
        return self.flavor == 'VARIABLE'