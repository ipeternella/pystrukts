"""
Module with tests for the OrderedDict implementation based on two parallel lists
and binary searching.
"""
import pytest

from algorithms.searching.dictionaries.parallel_lists import OrderedDict
from algorithms.searching.exceptions import KeyErrorWithRank


def test_should_assert_ordered_dict_is_empty():
    # arrange
    d = OrderedDict()

    # act and assert
    assert len(d) == 0
    assert d.is_empty() is True


def test_should_raise_keyerrorwithrank_if_key_is_not_found():
    # arrange
    d: OrderedDict[str, int] = OrderedDict()

    # act and assert
    with pytest.raises(KeyErrorWithRank):
        d.get("not_found")
