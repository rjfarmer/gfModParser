# SPDX-License-Identifier: GPL-2.0+


from .. import utils

from . import attributes


class Components:
    def __init__(self, components):
        self._components = components

    def __len__(self):
        return len(self._components)

    def __iter__(self):
        return iter(self._components)


class component:
    def __init__(self, component):
        self._component = component

        self.id = int(self._component[0])
        self.name = utils.string_clean(self._component[1])
        self.ts = typespec(self._component[2])
        self.array_spec = arrayspec(self._component[3])
        if len(self._component[4]):
            self.expr = expression(self._component[4])
        if len(self._component[5]):
            self.actual_arg = actual_arglist(self._component[5])
        self.attr = attributes.attribute(self._component[6])
        self.access = utils.string_clean(self._component[7])

        if self.name == "_final" or self.name == "_hash":
            self.initializer = expression(self._component[8])
            _ = self._component.pop(8)

        if not self.attr.proc == "UNKNOWN-PROC":
            self.proc_ptr = typebound_proc(self._component[8])
