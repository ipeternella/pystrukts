"""
Module with implementations of algorithms to hash integers.
"""
from dataclasses import dataclass
from typing import Generic
from typing import List

from algorithms.linked_lists.singly import LinkedList
from algorithms.searching.types import KT
from algorithms.searching.types import VT


@dataclass
class Node(Generic[KT, VT]):
    """
    Node for holding both keys and values of a hash map.
    """

    key: KT
    value: VT


class HashMap(Generic[KT, VT]):
    """
    Dictionary (symbol table) implemented with hashing strategy with separate chaining
    as the strategy for collision resolution.
    """

    _buckets: List[LinkedList[Node[KT, VT]]]  # list of linked lists (buckets)
    _keys_count: int  # total keys inside the hashmap

    def __init__(self, hash_table_size: int = 97) -> None:
        self._buckets = [LinkedList()] * hash_table_size  # empty list of linked lists
        self._keys_count = 0

    @property
    def buckets_size(self) -> int:
        """
        Returns the size of the hashmap's bucket list. Notice that this is not the same as the
        amount of keys inside the map (not _keys_count).
        """
        return len(self._buckets)

    def get(self, key: KT, default_value: VT) -> VT:
        """
        Gets a key value from the hash table. If the key is not found, the defaukt_value is returned.
        """

        try:
            node = self._get_node(key)
            return node.value
        except KeyError:
            return default_value

    def put(self, key: KT, value: VT) -> None:
        """
        Puts a new key and value into the hash table. If the key already exists, it's value
        is updated. In case of hash collisions, the linked list gets a new element appended
        item to its end (separate chaining).
        """
        bucket_ix = self._hash(key)

        try:
            node = self._get_node(key)
            node.value = value  # updates value
        except KeyError:
            linked_list = self._buckets[bucket_ix]

            new_node = Node(key, value)
            linked_list.insert_right(new_node)  # adds new value
            self._keys_count += 1  # increases key count

    def _hash(self, key: KT) -> int:
        """
        Hashing function of the keys. The hash function if a composition of two functions:

        1. The first fn converts the key into its integer hash code:
            - Each type has require its own hash fn, so we use std lib's hash fn

        2. The second fn converts the hash code into a bucket index (from _buckets list)
            - Here we use modular hashing (common for ints): hash_code % M (M = table size)
        """
        # fn 1
        hash_code = hash(key)

        # fn 2
        bucket_ix = hash_code % self.buckets_size  # modular hashing

        return bucket_ix

    def _get_node(self, key: KT) -> Node[KT, VT]:
        """
        Gets a node from the hash table. If the key is not found, raises KeyError.
        """
        bucket_ix = self._hash(key)
        linked_list = self._buckets[bucket_ix]

        # traverses linked list to find the appropriate key value
        for node in linked_list:
            if node.key == key:
                return node

        raise KeyError

    def __len__(self) -> int:
        """
        Returns the amount of keys inside the hashmap.
        """
        return self._keys_count
