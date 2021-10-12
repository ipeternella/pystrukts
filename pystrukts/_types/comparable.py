"""
Module with comparable typedefs.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any
from typing import Protocol
from typing import TypeVar

KT = TypeVar("KT", bound="Comparable")
VT = TypeVar("VT")


class Comparable(Protocol):
    """
    Comparable protocol for two typedefs: KT and VT.
    """

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __lt__(self: KT, other: KT) -> bool:
        pass

    def __gt__(self: KT, other: KT) -> bool:
        return (not self < other) and self != other

    def __le__(self: KT, other: KT) -> bool:
        return self < other or self == other

    def __ge__(self: KT, other: KT) -> bool:
        return not self < other
