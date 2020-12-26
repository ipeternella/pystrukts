"""
Module with tests regarding linked lists data structures and algorithms.
"""
import pytest

from algorithms.linked_lists.exceptions import EmptyLinkedList
from algorithms.linked_lists.singly import LinkedList


def test_should_create_empty_linked_list():
    # arrange
    linked_list = LinkedList()

    # act and assert
    assert len(linked_list) == 0
    assert linked_list.is_empty()


def test_should_two_new_nodes_at_the_beginning():
    # arrange
    linked_list: LinkedList[str] = LinkedList()

    # act: add first string to the linked list
    linked_list.insert("world")

    # assert
    assert len(linked_list) == 1
    assert linked_list.first_node.item == "world"
    assert linked_list.first_node.next is None

    # act: add another string to the linked list
    linked_list.insert("hello")  # this should be the NEW first node

    # assert: second string must be the first element
    assert len(linked_list) == 2
    assert linked_list.first_node.item == "hello"
    assert linked_list.first_node.next.item == "world"
    assert linked_list.first_node.next.next is None


def test_should_raise_exception_when_popping_from_empty_linked_list():
    # arrange
    linked_list: LinkedList[str] = LinkedList()

    # act and assert
    with pytest.raises(EmptyLinkedList):
        linked_list.pop()


def test_should_pop_element_from_linked_list_with_one_element():
    # arrange
    linked_list: LinkedList[int] = LinkedList()
    linked_list.insert(5)

    # act
    removed_item = linked_list.pop()

    # assert
    assert removed_item == 5
    assert len(linked_list) == 0
    assert linked_list.is_empty()


def test_should_pop_element_from_linked_list_with_two_elements():
    # arrange
    linked_list: LinkedList[str] = LinkedList()
    linked_list.insert("world")
    linked_list.insert("hello")  # this is the first node now

    assert len(linked_list) == 2

    # act
    removed_item = linked_list.pop()

    # assert
    assert removed_item == "hello"
    assert len(linked_list) == 1
    assert linked_list.is_empty() is False

    # act: remove last element
    removed_item = linked_list.pop()

    # assert: linked list should be empty now
    assert removed_item == "world"
    assert len(linked_list) == 0
    assert linked_list.is_empty() is True
