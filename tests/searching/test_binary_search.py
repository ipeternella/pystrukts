"""
Module with tests for binary search implementations.
"""

import pytest

from algorithms.searching.binary_search import binary_search_index
from algorithms.searching.exceptions import KeyErrorWithRank


def test_should_find_key_present_on_int_list():
    # arrange
    xs = [1, 2, 3, 4, 5]
    key = 2

    # act
    ix = binary_search_index(key, xs)

    # assert
    assert ix == 1


def test_should_raise_keyerrorrank_rank_zero_when_key_is_not_found():
    # arrange
    xs = ["luigi", "mario", "peach", "yoshi"]
    key = "bowser"

    # act
    with pytest.raises(KeyErrorWithRank) as exception_info:
        binary_search_index(key, xs)

    # assert: exception
    assert exception_info.value.rank == 0


def test_should_raise_keyerrorrank_rank_one_when_key_is_not_found():
    # arrange
    xs = ["bowser", "luigi", "mario", "peach", "yoshi"]
    key = "igu"

    # act
    with pytest.raises(KeyErrorWithRank) as exception_info:
        binary_search_index(key, xs)

    # assert: exception
    assert exception_info.value.rank == 1
