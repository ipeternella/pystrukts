"""
Module with stack implementations.
"""

from typing import Generator
from typing import Generic
from typing import TypeVar

from algorithms.linked_lists.exceptions import EmptyLinkedList
from algorithms.linked_lists.singly import LinkedList
from algorithms.stacks.exceptions import EmptyStack

T = TypeVar("T")


class Stack(Generic[T]):
    """
    Basic stack (LIFO structure) implementation which uses an underlying
    singly linked list implementation.
    """

    _linked_list: LinkedList[T]

    def __init__(self) -> None:
        self._linked_list = LinkedList()

    def __len__(self) -> int:
        return len(self._linked_list)

    def __iter__(self) -> Generator:
        """
        Traverses all the items of the queue by traversing the internal linked list.
        Warning: this operation DEQUEUES the items from the queue.

        Time complexity: O(N)
        """
        for item in self._linked_list:
            yield self._linked_list.pop()

    def push(self, item: T) -> None:
        """
        Pushes a new item on the top of the stack. As the stack is LIFO structure, this internally
        inserts a new item at the beginning (left insert) of the underlying linked list so that it
        can be popped first.
        """
        self._linked_list.insert(item)

    def pop(self) -> T:
        """
        Pops the last inserted item on the stack.
        """
        try:
            lifo_item = self._linked_list.pop()
        except EmptyLinkedList:
            raise EmptyStack("Cannot pop an item from an empty stack.")

        return lifo_item
