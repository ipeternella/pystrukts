"""
Module with min heap implementation using lists (dynamic arrays).
"""
import math
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple

from pystrukts._types.comparable import KT
from pystrukts._types.comparable import VT
from pystrukts.heaps.exceptions import EmptyHeap


class MinHeap(Generic[KT, VT]):
    """
    Represents a min heap of (key, value) elements.
    """

    heap: List[Tuple[KT, VT]]

    def __init__(self, elements: Optional[List[Tuple[KT, VT]]] = None) -> None:
        self.heap = []

        if elements is None:
            return

        for element in elements:
            if not isinstance(element, Tuple) and len(element) != 2:  # type: ignore
                raise ValueError(f"Elements must be list of 2-tuples [(key, value)] and not: {element}!")

            self.insert(element[0], element[1])

    def __len__(self) -> int:
        """
        Returns the size of the heap.
        """
        return len(self.heap)

    def insert(self, key: KT, value: VT) -> None:
        """
        Inserts a new (key, value) on the heap and corrects the heap list to maintain the min. heap
        property.
        """
        self.heap.append((key, value))
        self.decrease_key(len(self) - 1, key)

    def extract_min(self) -> VT:
        """
        Removes and return the min element of the heap and then re-heapifies the collection to maintain
        the heap property.
        """
        size = len(self)

        if size == 0:
            raise EmptyHeap("Empty heap!")

        value = self.heap[0][1]

        self.heap[0] = self.heap[size - 1]
        self.heap.pop()
        self.min_heapify(0)

        return value

    def decrease_key(self, i: int, new_key: KT) -> None:
        """
        Decreases the key of the i-th heap element and goes top-down approach replacing smaller
        children with their parent until the beginning of the heap is reached. This method is
        used to insert new elements on the heap.
        """
        if len(self) == 0:
            raise EmptyHeap("Cannot decrease key of an empty min heap!")

        if new_key > self.heap[i][0]:
            raise ValueError(f"New key: {new_key} is larger than old key: {self.heap[i][0]}")

        # value i gets new key tuple
        self.heap[i] = (new_key, self.heap[i][1])

        # top-down
        while i > 0 and self.is_smaller_than_parent(i):
            self._swap(i, self.parent(i))
            i = self.parent(i)

    def min_heapify(self, parent_i: int) -> None:
        """
        Compares the parent key with its children to obtain the smallest key. If one of
        the children is smaller than the parent, the smallest child replaces the parent
        recursively. This method is used to maintain the min. heap property and goes in
        a bottom-up approach until the size of heap is reached.
        """
        size = len(self)
        left_i = self.left_child(parent_i)
        right_i = self.right_child(parent_i)
        smallest_i = parent_i

        if left_i < size and self.heap[left_i][0] < self.heap[smallest_i][0]:
            smallest_i = left_i

        if right_i < size and self.heap[right_i][0] < self.heap[smallest_i][0]:
            smallest_i = right_i

        # re-heapify is needed -> bottom-up
        if smallest_i != parent_i:
            self._swap(parent_i, smallest_i)  # smaller values comes first on min. heap
            self.min_heapify(smallest_i)

    def parent(self, child_i: int) -> int:
        """
        Returns the index of the parent of a given child index. Notice that the returned
        value can be out of boundaries of the heap list.
        """
        return math.ceil(child_i / 2) - 1

    def left_child(self, parent_i: int) -> int:
        """
        Returns the index of the left child of a parent index. Notice that the returned
        value can be out of boundaries of the heap list.
        """
        return 2 * parent_i + 1  # 0-indexed array

    def right_child(self, parent_i: int) -> int:
        """
        Returns the index of the right child of a parent index. Notice that the returned
        value can be out of boundaries of the heap list.
        """
        return 2 * parent_i + 2  # 0-indexed array

    def heap_min(self) -> VT:
        """
        Returns the min value (first element) of min. heap.
        """
        return self.heap[0][1]

    def is_smaller_than_parent(self, child_i: int) -> bool:
        """
        Compares the key of the i-th child with its parent's key. Returns True if the child
        is smaller than its parent which is the case the parent must be swapped with the child
        to maintain the min. heap property.
        """
        parent_i = self.parent(child_i)

        return self.heap[child_i][0] < self.heap[parent_i][0]

    def _swap(self, ix_1: int, ix_2: int) -> None:
        """
        Swaps two heap elements.
        """
        tmp = self.heap[ix_1]

        self.heap[ix_1] = self.heap[ix_2]
        self.heap[ix_2] = tmp
