"""
Module with implementations related to linked lists (singly, doubly, etc.).
"""

from typing import Generic
from typing import Optional
from typing import TypeVar

from algorithms.data_containers.node_single_reference import Node

T = TypeVar("T")


class LinkedList(Generic[T]):
    """
    A singly linked list implementation.
    """

    length: int
    first_node: Optional[Node]

    def __init__(self) -> None:
        self.length = 0
        self.first_node = None

    def __len__(self) -> int:
        return self.length

    def is_empty(self) -> bool:
        """
        Checks if the linked list is empty or not.
        """
        return self.length == 0

    def insert(self, item: T) -> None:
        """
        Inserts a new item at the BEGINNING of the linked list.
        """
        if self.is_empty():
            self.first_node = Node(item)
            self.length += 1
        else:
            new_node = Node(item, self.first_node)

            self.first_node = new_node
            self.length += 1
