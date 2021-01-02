"""
Module with a symbol table (dictionary) implementation using two lists: one for the keys and
one for the values. Uses binary search for findings keys efficiently.
"""
from typing import Generic
from typing import List

from algorithms.searching.binary_search import binary_search_index
from algorithms.searching.exceptions import KeyErrorWithRank
from algorithms.searching.types import KT
from algorithms.searching.types import VT


class OrderedDict(Generic[KT, VT]):
    """
    Dictionary (symbol table) implementation based on two parallel lists and binary search. The keys are
    kept 'in order' in order to benefit from binary search's efficiency O(logN) and not require linear scans O(N).
    """

    # parallel lists
    _keys: List[KT]
    _values: List[VT]

    def __init__(self) -> None:
        self._length = 0
        self._keys = []
        self._values = []

    def __len__(self) -> int:
        return len(self._keys)

    def is_empty(self) -> bool:
        """
        Checks if the dictionary is empty (no keys/vals) or not.

        Time Complexity: O(1)
        """
        return len(self._keys) == 0

    def rank(self, key: KT) -> int:
        """
        Returns the amount of keys that are less than the given key.

        Time Complexity: O(logN)
        """
        try:
            key_rank = binary_search_index(key, self._keys)
        except KeyErrorWithRank as e:
            return e.rank

        return key_rank

    def get(self, key: KT) -> VT:
        """
        Gets a key from the dictionary collection. Raises KeyErrorWithRank if the key is not found which
        contains the searched key's rank.
        """
        key_rank = binary_search_index(key, self._keys)

        return self._values[key_rank]

    def put(self, key: KT) -> None:
        """
        Puts a new key in the dictionary in a sorted way to keep the keys ordered for binary search.
        """
        pass
