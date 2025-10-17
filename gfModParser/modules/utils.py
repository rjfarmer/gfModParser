# SPDX-License-Identifier: GPL-2.0+
from typing import Iterator
from packaging.version import Version


class ListSymbols:
    def __init__(self, args: list[str], *, version: Version) -> None:
        self._args = [int(i) for i in args]
        self.version = version

    def __len__(self) -> int:
        return len(self._args)

    def __iter__(self) -> Iterator[int]:
        return iter(self._args)

    @property
    def values(self) -> list[int]:
        return self._args

    def __str__(self) -> str:
        return str(self._args)

    def __repr__(self) -> str:
        return repr(self._args)

    def __contains__(self, key: str) -> bool:
        return int(key) in self._args

    def __getitem__(self, key: int) -> int:
        return self._args[key]
