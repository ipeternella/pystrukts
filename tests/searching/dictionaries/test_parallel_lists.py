"""
Module with tests for the OrderedDict implementation based on two parallel lists
and binary searching.
"""
import pytest

from algorithms.searching.dictionaries.parallel_lists import OrderedDict
from algorithms.searching.exceptions import KeyErrorWithRank


def test_should_assert_ordered_dict_two_lists_is_empty():
    # arrange
    d = OrderedDict()

    # act and assert
    assert len(d) == 0
    assert d.is_empty() is True


def test_should_assert_raise_keyerrorwithrank_if_key_is_not_found_in_ordered_dict_two_lists():
    # arrange
    d: OrderedDict[str, int] = OrderedDict()

    # act and assert
    assert d.get("not_found") is None


def test_should_assert_key_is_found_after_insertion_in_ordered_dict_two_lists():
    # arrange
    d: OrderedDict[str, str] = OrderedDict()

    # act
    d.put("first_name", "igor")
    d.put("last_name", "grillo peternella")

    # assert
    assert d.get("first_name") == "igor"
    assert d.get("last_name") == "grillo peternella"
    assert d.get("middle_name") is None
    assert len(d) == 2


def test_should_update_value_of_same_key_in_ordered_dict_two_lists():
    # arrange
    d: OrderedDict[str, str] = OrderedDict()

    # act
    d.put("k1", 1)

    # assert
    assert d.get("k1") == 1

    # act: put the same 'k1'
    d.put("k1", 2)

    # assert: updated value
    assert d.get("k1") == 2


def test_should_insert_bigger_keys_in_ordered_dict():
    # arrange
    d: OrderedDict[str, str] = OrderedDict()
    updated_1 = d.put("a", 1)

    # act
    updated_2 = d.put("b", 2)
    updated_3 = d.put("c", 3)

    # assert
    assert updated_1 is False
    assert updated_2 is False
    assert updated_3 is False

    assert d.get("a") == 1
    assert d.get("b") == 2
    assert d.get("c") == 3
    assert d.get("e") is None
    assert len(d) == 3

    # act: update 'b' key
    updated_4 = d.put("b", -1)

    # assert: updated b value
    assert d.get("b") == -1
    assert updated_4 is True

    # act: adds a key in between the first two existing keys
    updated_5 = d.put("a1", 10)  # 'a' < 'a1' < 'b'

    # assert: a new key must have been inserted (no update)
    assert d.get("a1") == 10
    assert updated_5 is False

    # act: a new key is added in between the end (no update)
    updated_6 = d.put("c1", 20)
    assert updated_6 is False

    # assert: new key is added
    assert d.get("c1") == 20
    assert len(d) == 5
