"""
Module with generic comparable type used by searching algorithms.
"""
from __future__ import annotations

from abc import abstractmethod
from typing import Protocol
from typing import TypeVar


class Comparable(Protocol):
    """
    Protocol for using comparable types hints.
    """

    @abstractmethod
    def __lt__(self: KT, other: KT) -> bool:
        pass


KT = TypeVar("KT", bound=Comparable)
VT = TypeVar("VT")
