# SPDX-License-Identifier: GPL-2.0+

import pyparsing

from .. import utils
from . import attributes
from . import typespecs
from . import arrays


class Components:
    def __init__(self, components):
        self._components = {}
        for c in components:
            self._components[utils.string_clean(c[1])] = c

    def __len__(self):
        return len(self._components)

    def __contains__(self, key):
        return key in self._components

    def keys(self):
        return self._components.keys()

    def __getitem__(self, key):
        if key in self._components:
            if isinstance(self._components[key], pyparsing.results.ParseResults):
                self._components[key] = component(self._components[key])
            return self._components[key]
        else:
            raise KeyError(f"No key {key} found")


class component:
    def __init__(self, component):
        self._component = component

        self.id = int(self._component[0])
        self.name = utils.string_clean(self._component[1])
        self.typespec = typespecs.typespec(self._component[2])

        self.array = arrays.arrayspec(self._component[3])
        # if len(self._component[4]):
        #     self.expr = expression(self._component[4])
        # if len(self._component[5]):
        #     self.actual_arg = actual_arglist(self._component[5])
        self.attribute = attributes.Attributes(self._component[6])
        self.access = utils.string_clean(self._component[7])

        if self.name == "_final" or self.name == "_hash":
            # self.initializer = expression(self._component[8])
            _ = self._component.pop(8)

        if not self.attribute.procedure == "UNKNOWN-PROC":
            pass
            # self.proc_ptr = typebound_proc(self._component[8])
