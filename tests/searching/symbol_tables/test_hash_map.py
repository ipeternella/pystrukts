"""
Module with tests for hash maps implementations.
"""
from algorithms.searching.symbol_tables.hash_map import HashMap


def test_should_add_and_get_key_in_hashmap():
    # arrange
    hash_map = HashMap()

    # act
    hash_map.put("k1", 1)

    # assert
    item = hash_map.get("k1", None)

    assert item == 1
    assert hash_map.buckets_size == 97
    assert len(hash_map) == 1

    # act
    hash_map.put("k1", 5)

    # assert
    item = hash_map.get("k1", None)

    assert item == 5
    assert hash_map.buckets_size == 97
    assert len(hash_map) == 1

    # act
    hash_map.put("k2", 2)

    # arrange
    item = hash_map.get("k2", None)

    assert item == 2
    assert hash_map.buckets_size == 97
    assert len(hash_map) == 2
