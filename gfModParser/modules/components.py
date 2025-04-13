# SPDX-License-Identifier: GPL-2.0+

import pyparsing

from .. import utils
from . import attributes
from . import expressions
from . import arrays
from . import procedures


class Components:
    def __init__(self, components, *, version):
        self._components = {}
        self.version = version
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
                self._components[key] = component(
                    self._components[key], version=self.version
                )
            return self._components[key]
        else:
            raise KeyError(f"No key {key} found")


class component:
    def __init__(self, component, *, version):
        self._component = component
        self.version = version

    @property
    def id(self):
        return int(self._component[0])

    @property
    def name(self):
        return utils.string_clean(self._component[1])

    @property
    def typespec(self):
        return expressions.typespec(self._component[2], version=self.version)

    @property
    def array(self):
        return arrays.arrayspec(self._component[3], version=self.version)

    @property
    def pdt_expression(self):
        return expressions.expression(self._component[4], version=self.version)

    # PDT component specification
    @property
    def pdt_arglist(self):
        return procedures.actual_arglist(self._component[5], version=self.version)

    @property
    def attribute(self):
        return attributes.Attributes(self._component[6], version=self.version)

    @property
    def access(self):
        return utils.string_clean(self._component[7])

    @property
    def initializer(self):
        # also check for vtype?
        if self.name == "_final" or self.name == "_hash":
            return expressions.expression(self._component[8], version=self.version)

    @property
    def proc_pointer(self):
        if self.attribute.proc_pointer:
            # The initialzer might be in slot 8 so instead of looking at 8 or 9 just look at the final one
            return procedures.typebound_proc(self._component[-1], version=self.version)
