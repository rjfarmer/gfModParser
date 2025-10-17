# SPDX-License-Identifier: GPL-2.0+
from packaging.version import Version

from typing import Any

from .. import utils


class SummaryItem:
    """
    Single entry into the Summary look up table
    """

    def __init__(self, name: str, ambiguous: str, id: int, *, version: Version):
        self.name = utils.string_clean(name)
        self.ambiguous = ambiguous != "0"
        self.id = int(id)
        self.version = version


class Summary:
    """
    Look up table of top level variables/procedures and thier ID's
    """

    def __init__(self, summary: str, *, version: Version) -> None:
        self.version = version
        # Remove any nested newlines
        rs = summary.replace("\n", " ")
        # Remove start and end brackets
        rs = rs.replace("(", "").replace(") ", "")

        # Split into list
        list_raw: list[Any] = rs.split()
        self._names = {}

        # Split into groups of three
        for i in range(0, len(list_raw), 3):
            d = SummaryItem(*list_raw[i : i + 3], version=self.version)
            self._names[d.name] = d

    def __getitem__(self, key: str) -> SummaryItem:
        return self._names[key]

    def keys(self):
        return self._names.keys()

    def __contains__(self, key: str) -> bool:
        return key in self._names
