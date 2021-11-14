"""
Module with minimal priority queue implementations.
"""
from typing import Generic
from typing import Optional

from pystrukts._types.basic import T
from pystrukts.heaps.min_heap import MinHeap


class MinPriorityQueue(Generic[T]):
    """
    Represents a queue built as a thin wrapper on top of a min. heap in
    order to follow a minimal priority policy.
    """

    _min_heap: MinHeap[int, T]

    def __init__(self) -> None:
        self._min_heap = MinHeap()

    def __len__(self) -> int:
        return len(self._min_heap)

    def is_empty(self) -> bool:
        """
        Returns True if the queue is empty. Otherwise, False.
        """
        return len(self) == 0

    def enqueue(self, priority: int, value: T) -> None:
        """
        Adds a new key/value to the queue.
        """
        self._min_heap.insert(priority, value)

    def dequeue(self) -> Optional[T]:
        """
        Removes the first item on the queue according to a FIFO policy.
        """
        if len(self) == 0:
            return None

        return self._min_heap.extract_min()
