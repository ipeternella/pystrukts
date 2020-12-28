"""
Module with tests for binary search implementations.
"""

from algorithms.searching.binary_search import binary_search_index


def test_should_find_key_present_on_list():
    # arrange
    xs = [1, 2, 3, 4, 5]
    key = 2

    # act
    ix = binary_search_index(key, xs)

    # assert
    assert ix == 1
