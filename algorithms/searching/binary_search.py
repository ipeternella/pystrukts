"""
Binary search algorithm to be used with python lists.
"""
from typing import List

from algorithms.searching.exceptions import KeyErrorWithRank
from algorithms.searching.types import KT


def binary_search_index(key: KT, values: List[KT]) -> int:
    """
    Non-recursive binary search implementation which can be used to find a key's index on
    a List.

    Raises KeyError if the key was not found together with the final low value
    which ended up as low > high. This value is also known as the 'rank' of the searched key,
    and means the amount of less keys than the searched key.

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

    raise KeyErrorWithRank(low, str(key))
