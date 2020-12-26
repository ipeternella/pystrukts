"""
Some useful node implementations that many data structures require.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic
from typing import Optional
from typing import TypeVar

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    """
    A node representation with one reference only: the next node.
    """

    item: T
    next: Optional[Node]

    def __init__(self, item: T, next: Optional[Node] = None) -> None:
        self.item = item
        self.next = next
