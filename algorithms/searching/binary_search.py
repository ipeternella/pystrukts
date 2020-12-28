"""
Binary search algorithm to be used with python lists.
"""
from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import List
from typing import Optional
from typing import TypeVar


class UpperBoundComparableType(metaclass=ABCMeta):
    """
    Upper-bound generic type which implements a comparison protocol.
    """

    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        pass


T = TypeVar("T", bound=UpperBoundComparableType)


def binary_search_index(key: T, values: List[T]) -> Optional[int]:
    """
    Non-recursive binary search implementation which can be used to find a key's index on
    a List. Returns None if the key was not found in the list.

    Time complexity: O(logN)
    """
    low, high = 0, len(values) - 1

    while low <= high:
        # to get mid value of the sorted list
        mid = (low + high) // 2  # floor

        # compare mid value with the desired key
        if key > values[mid]:
            low = mid + 1  # key is too big: update low index
        elif key < values[mid]:
            high = mid - 1  # key is too small: update high index
        else:
            return mid  # gotcha!

    return None
