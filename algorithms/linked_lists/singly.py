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

    _length: int
    _first_node: Optional[Node]
    _last_node: Optional[Node]

    def __init__(self) -> None:
        self._length = 0
        self._first_node = None

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Generator:
        """
        Traverses the whole linked list.

        Time Complexity: O(N)
        """

        if self.is_empty():
            raise StopIteration

        current_node = self._first_node

        while current_node is not None:
            yield current_node.item  # using generators to facilitate the iteration state
            current_node = current_node.next

    def is_empty(self) -> bool:
        """
        Checks if the linked list is empty or not.

        Time Complexity: O(1)
        """
        return self._length == 0

    def insert(self, item: T) -> None:
        """
        Inserts a new item at the BEGINNING (left-side) of the linked list.

        Time Complexity: O(1)
        """
        if self.is_empty():
            new_node = Node(item)

            self._first_node = new_node
            self._last_node = new_node
        else:
            # last_node remains as is: nothing changes for left insertions.
            new_node = Node(item, self._first_node)

            self._first_node = new_node

        self._length += 1

    def insert_right(self, item: T) -> None:
        """
        Inserts a new item at the END (right-side) of the linked list.

        Time Complexity: O(1)
        """
        new_node = Node(item)  # no next reference: it's the end of the linked list!

        if self.is_empty():
            self._first_node = new_node
            self._last_node = new_node
        else:
            # first_node remains as is: nothing changes for right insertions.
            self._last_node.next = new_node  # type: ignore
            self._last_node = new_node  # updates last_node reference

        self._length += 1

    def pop(self) -> T:
        """
        Removes the first node of the linked list.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise EmptyLinkedList("Cannot remove items from an empty linked list.")

        removed_item: T = self._first_node.item  # type: ignore

        if self._length == 1:
            self._first_node = None
            self._last_node = None
            self._length -= 1

            return removed_item

        second_node = self._first_node.next  # type: ignore
        self._first_node = second_node
        self._length -= 1

        return removed_item
