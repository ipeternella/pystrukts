"""
Module with queues implementations (queues, deques, etc.).
"""

from typing import Generator
from typing import Generic
from typing import TypeVar

from algorithms.linked_lists.exceptions import EmptyLinkedList
from algorithms.linked_lists.singly import LinkedList
from algorithms.queues.exceptions import EmptyQueue

T = TypeVar("T")


class Queue(Generic[T]):
    """
    Basic queue (FIFO structure) implementation which uses an underlying
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

    def enqueue(self, item: T) -> None:
        """
        Enqueues an item in the queue. All the items are inserted at the end (right-insert) of the
        linked list in order to maintain the FIFO nature of queues.

        Time complexity: O(1)
        """
        self._linked_list.insert_right(item)  # FIFO fashion: new items go to the end

    def dequeue(self) -> T:
        """
        Dequeues an item from the queue in a FIFO fashion.

        Time complexity: O(1)
        """
        try:
            dequeued_item = self._linked_list.pop()  # removes from the linked list
        except EmptyLinkedList:
            raise EmptyQueue("Cannot dequeue items from an empty queue.")

        return dequeued_item
