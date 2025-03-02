# SPDX-License-Identifier: GPL-2.0+
from .. import utils


class SummaryItem:
    """
    Single entry into the Summary look up table
    """

    def __init__(self, name, ambiguous, id):
        self.name = utils.string_clean(name)
        self.ambiguous = ambiguous != "0"
        self.id = int(id)


class Summary:
    """
    Look up table of top level variables/procedures and thier ID's
    """

    def __init__(self, summary):
        # Remove any nested newlines
        self._raw_summary = summary.replace("\n", " ")
        # Remove start and end brackets
        self._raw_summary = self._raw_summary.replace("(", "").replace(") ", "")

        # Split into list
        self._raw_summary = self._raw_summary.split()
        self._names = {}

        # Split into groups of three
        for i in range(0, len(self._raw_summary), 3):
            d = SummaryItem(*self._raw_summary[i : i + 3])
            self._names[d.name] = d

    def __getitem__(self, key):
        return self._names[key]

    def keys(self):
        return self._names.keys()

    def __contains__(self, key):
        return key in self._names
