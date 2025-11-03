# SPDX-License-Identifier: GPL-2.0+
from packaging.version import Version

from functools import cached_property

from .. import utils

_all = set(
    [
        "ALLOCATABLE",
        "ARTIFICIAL",
        "ASYNCHRONOUS",
        "DIMENSION",
        "CODIMENSION",
        "CONTIGUOUS",
        "EXTERNAL",
        "INTRINSIC",
        "OPTIONAL",
        "POINTER",
        "VOLATILE",
        "TARGET",
        "THREADPRIVATE",
        "DUMMY",
        "RESULT",
        "DATA",
        "IN_NAMELIST",
        "IN_COMMON",
        "FUNCTION",
        "SUBROUTINE",
        "SEQUENCE",
        "ELEMENTAL",
        "PURE",
        "RECURSIVE",
        "GENERIC",
        "ALWAYS_EXPLICIT",
        "CRAY_POINTER",
        "CRAY_POINTEE",
        "IS_BIND_C",
        "IS_C_INTEROP",
        "IS_ISO_C",
        "VALUE",
        "ALLOC_COMP",
        "COARRAY_COMP",
        "LOCK_COMP",
        "EVENT_COMP",
        "POINTER_COMP",
        "PROC_POINTER_COMP",
        "PRIVATE_COMP",
        "ZERO_COMP",
        "PROTECTED",
        "ABSTRACT",
        "IS_CLASS",
        "PROCEDURE",
        "PROC_POINTER",
        "VTYPE",
        "VTAB",
        "CLASS_POINTER",
        "IMPLICIT_PURE",
        "UNLIMITED_POLY",
        "OMP_DECLARE_TARGET",
        "ARRAY_OUTER_DEPENDENCY",
        "MODULE_PROCEDURE",
        "OACC_DECLARE_CREATE",
        "OACC_DECLARE_COPYIN",
        "OACC_DECLARE_DEVICEPTR",
        "OACC_DECLARE_DEVICE_RESIDENT",
        "OACC_DECLARE_LINK",
        "OMP_DECLARE_TARGET_LINK",
        "PDT_KIND",
        "PDT_LEN",
        "PDT_TYPE",
        "PDT_TEMPLATE",
        "PDT_ARRAY",
        "PDT_STRING",
        "OACC_ROUTINE_LOP_GANG",
        "OACC_ROUTINE_LOP_WORKER",
        "OACC_ROUTINE_LOP_VECTOR",
        "OACC_ROUTINE_LOP_SEQ",
        "OACC_ROUTINE_NOHOST",
        "OMP_REQ_REVERSE_OFFLOAD",
        "OMP_REQ_UNIFIED_ADDRESS",
        "OMP_REQ_UNIFIED_SHARED_MEMORY",
        "OMP_REQ_SELF_MAPS",
        "OMP_REQ_DYNAMIC_ALLOCATORS",
        "OMP_REQ_MEM_ORDER_SEQ_CST",
        "OMP_REQ_MEM_ORDER_ACQ_REL",
        "OMP_REQ_MEM_ORDER_ACQUIRE",
        "OMP_REQ_MEM_ORDER_RELAXED",
        "OMP_REQ_MEM_ORDER_RELEASE",
        "OMP_DEVICE_TYPE_HOST",
        "OMP_DEVICE_TYPE_NOHOST",
        "OMP_DEVICE_TYPE_ANYHOST",
    ]
)


class Attributes:

    def __init__(self, attributes, *, version: Version) -> None:
        self._attributes = attributes
        self.version = version

    @property
    def flavor(self) -> str:
        return utils.string_clean(self._attributes[0])

    @property
    def intent(self) -> str:
        return utils.string_clean(self._attributes[1])

    @property
    def procedure(self) -> str:
        return utils.string_clean(self._attributes[2])

    @property
    def if_source(self) -> str:
        return utils.string_clean(self._attributes[3])

    @property
    def save(self) -> str:
        return utils.string_clean(self._attributes[4])

    @property
    def external_attribute(self) -> bool:
        return int(self._attributes[5]) == 1

    @property
    def extension(self) -> bool:
        return int(self._attributes[6]) == 1

    @cached_property
    def attributes(self) -> set[str]:
        return set([utils.string_clean(i) for i in self._attributes[7:]])

    @property
    def is_parameter(self) -> bool:
        return self.flavor == "PARAMETER"

    @property
    def is_variable(self) -> bool:
        return self.flavor == "VARIABLE"

    @property
    def is_procedure(self) -> bool:
        return self.flavor == "PROCEDURE"

    @property
    def is_derived_definition(self) -> bool:
        """
        Note this is only true for the definition of the derived type, not an instance of the type
        Instance of a deriver type should check the typespec.type == 'DERIVED'
        """
        return self.flavor == "DERIVED"

    @property
    def is_module(self) -> bool:
        return self.flavor == "MODULE"

    @property
    def is_namelist(self) -> bool:
        return self.flavor == "NAMELIST"

    def __dir__(self):
        # Get things defined by the getattr plus the properties (needs to dir() the class though)
        return [i.lower() for i in _all] + dir(self.__class__)

    def __getattr__(self, key: str):
        if key.upper() in _all:
            return key in self
        else:
            raise AttributeError(f"Key not found {key}")

    def __contains__(self, key: str) -> bool:
        return key.upper() in self.attributes
