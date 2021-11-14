"""
Module with FIFO queues implementations.
"""
from typing import Generic
from typing import Optional

from pystrukts._types.basic import KT
from pystrukts._types.basic import VT
from pystrukts.linked_lists.doubly import LinkedList


class Queue(Generic[KT, VT]):
    """
    Represents a queue data structure with FIFO policy.
    """

    _linked_list: LinkedList[KT, VT]

    def __init__(self) -> None:
        self._linked_list = LinkedList()

    def __len__(self) -> int:
        return len(self._linked_list)

    def is_empty(self) -> bool:
        """
        Returns True if the queue is empty. Otherwise, False.
        """
        return len(self) == 0

    def enqueue(self, key: KT, value: VT) -> None:
        """
        Adds a new key/value to the queue.
        """
        self._linked_list.append(key, value)

    def dequeue(self) -> Optional[VT]:
        """
        Removes the first item on the queue according to a FIFO policy.
        """
        first_node = self._linked_list.first_node

        if first_node is None:
            return None  # empty queue

        return self._linked_list.delete(first_node.key)
