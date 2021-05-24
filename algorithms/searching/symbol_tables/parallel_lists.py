"""
Module with a symbol table (dictionary) implementation using two lists: one for the keys and
one for the values. Uses binary search for findings keys efficiently.
"""
from typing import Generic
from typing import List
from typing import Optional

from algorithms.searching.binary_search import binary_search_index
from algorithms.searching.exceptions import KeyErrorWithRank
from algorithms.searching.types import KT
from algorithms.searching.types import VT


class OrderedDict(Generic[KT, VT]):
    """
    Dictionary (symbol table) implementation based on two parallel lists and binary search. The keys are
    kept 'in order' in order to benefit from binary search's efficiency O(logN) and not require linear scans O(N).
    """

    # two parallel lists
    _length: int
    _keys: List[KT]
    _values: List[VT]

    def __init__(self) -> None:
        self._length = 0
        self._keys = []
        self._values = []

    def __len__(self) -> int:
        return self._length

    def _insert(self, key: KT, value: VT, index: int) -> None:
        """
        Inserts or updates a key and value into their respective lists. Increases
        the lists sizes in case of inserts.

        Time complexity: O(N)
        """
        self._keys.insert(index, key)
        self._values.insert(index, value)
        self._length += 1

    def _update(self, value: VT, index: int) -> None:
        """
        Updates a value of a given key that already exists in the dictionary. Does
        not increase the list sizes.

        Time complexity: O(1)
        """
        self._values[index] = value

    def is_empty(self) -> bool:
        """
        Checks if the dictionary is empty (no keys/vals) or not.

        Time Complexity: O(1)
        """
        return self._length == 0

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

    def get(self, key: KT, default_value: Optional[VT] = None) -> Optional[VT]:
        """
        Gets a key from the dictionary collection. Raises KeyErrorWithRank if the key is not found which
        contains the searched key's rank.

        Time Complexity: O(logN)
        """
        try:
            key_rank = binary_search_index(key, self._keys)
        except KeyErrorWithRank:
            return default_value

        return self._values[key_rank]

    def put(self, key: KT, value: VT) -> bool:
        """
        Puts (inserts or updates) a new key in the dictionary in a sorted way to keep the keys ordered for
        binary search. Returns True if a key has been updated and False otherwise.

        Time complexity: O(N) - inserts in worst case scenario due to insert()'s reallocation
        Time complexity: O(1) - updates
        """
        rank = self.rank(key)

        if self.is_empty() or rank == self._length or self._keys[rank] != key:  # insert-only cases
            self._insert(key, value, rank)
            return False

        self._update(value, rank)  # insert or update (upsert) cases
        return True

    def pop(self, key: KT) -> VT:
        """
        Pops (removes) a key and its corresponding value from the dictionary. If the key is not found, it
        raises an exception.

        Time complexity: O(N) - worst case scenario due to pop()'s reallocation.
        """
        rank = self.rank(key)

        if self.is_empty() or rank == self._length or self._keys[rank] != key:
            raise KeyErrorWithRank(rank, str(key))

        removed_value = self._values.pop(rank)
        self._keys.pop(rank)
        self._length -= 1

        return removed_value