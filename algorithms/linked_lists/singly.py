"""
Module with implementations related to linked lists (singly, doubly, etc.).
"""

from typing import Generator
from typing import Generic
from typing import Optional
from typing import TypeVar

from algorithms.data_containers.node_single_reference import Node
from algorithms.linked_lists.exceptions import EmptyLinkedList

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

    def __iter__(self) -> Generator:
        if self.is_empty():
            raise StopIteration

        current_node = self.first_node

        while current_node is not None:
            yield current_node.item  # using generators to facilitate the iteration state
            current_node = current_node.next

    def is_empty(self) -> bool:
        """
        Checks if the linked list is empty or not.

        Time Complexity: O(1)
        """
        return self.length == 0

    def insert(self, item: T) -> None:
        """
        Inserts a new item at the BEGINNING (left-side) of the linked list.

        Time Complexity: O(1)
        """
        if self.is_empty():
            self.first_node = Node(item)
            self.length += 1
        else:
            new_node = Node(item, self.first_node)

            self.first_node = new_node
            self.length += 1

    def pop(self) -> T:
        """
        Removes the first node of the linked list.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise EmptyLinkedList("Cannot remove items from an empty linked list.")

        removed_item: T = self.first_node.item  # type: ignore

        if self.length == 1:
            self.first_node = None
            self.length -= 1

            return removed_item

        second_node = self.first_node.next  # type: ignore
        self.first_node = second_node
        self.length -= 1

        return removed_item
