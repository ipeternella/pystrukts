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


def test_should_three_new_nodes_at_the_beginning():
    # arrange
    linked_list: LinkedList[str] = LinkedList()

    # act: add first string to the linked list
    linked_list.insert("world")

    # assert
    assert len(linked_list) == 1
    assert linked_list._first_node.item == "world"
    assert linked_list._first_node.next is None
    assert linked_list._last_node.item == "world"
    assert linked_list._last_node.next is None

    # act: add another string to the linked list
    linked_list.insert("hello")  # this should be the NEW first node

    # assert: second string must be the first element
    assert len(linked_list) == 2
    assert linked_list._first_node.item == "hello"
    assert linked_list._first_node.next.item == "world"
    assert linked_list._first_node.next.next is None

    assert linked_list._last_node.item == "world"
    assert linked_list._last_node.next is None

    # act: add a third string
    linked_list.insert("hey")

    # assert: last_node should not have been changed
    assert linked_list._first_node.item == "hey"
    assert linked_list._first_node.next.item == "hello"

    assert linked_list._last_node.item == "world"
    assert linked_list._last_node.next is None


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

    assert linked_list._first_node is None
    assert linked_list._last_node is None


def test_should_pop_element_from_linked_list_with_two_elements():
    # arrange
    linked_list: LinkedList[str] = LinkedList()
    linked_list.insert("world")
    linked_list.insert("hello")  # this is the first node now

    assert len(linked_list) == 2
    assert linked_list._first_node.item == "hello"
    assert linked_list._last_node.item == "world"

    # act
    removed_item = linked_list.pop()

    # assert
    assert removed_item == "hello"
    assert len(linked_list) == 1
    assert linked_list.is_empty() is False

    # first and last node now converge to the same reference
    assert linked_list._first_node.item == "world"
    assert linked_list._last_node.item == "world"

    # act: remove last element
    removed_item = linked_list.pop()

    # assert: linked list should be empty now
    assert removed_item == "world"
    assert len(linked_list) == 0
    assert linked_list.is_empty() is True


def test_should_traverse_linked_list():
    # arrange
    linked_list: LinkedList[str] = LinkedList()
    linked_list.insert("!")
    linked_list.insert("world")
    linked_list.insert("hello")  # this is the first node now

    # act
    nodes = [node for node in linked_list]

    # assert
    assert nodes == ["hello", "world", "!"]


def test_should_insert_right_for_empty_linked_list():
    # arrange
    linked_list: LinkedList[str] = LinkedList()

    # act
    linked_list.insert_right("hi")

    # assert
    assert linked_list._first_node.item == linked_list._last_node.item
    assert linked_list._first_node.next is None
    assert linked_list._last_node.next is None
    assert len(linked_list) == 1


def test_should_remain_consistent_through_many_inserts_and_pop_operations():
    # arrange
    linked_list: LinkedList[str] = LinkedList()
    linked_list.insert_right("hello")
    linked_list.insert_right("world")
    linked_list.insert_right("!")

    assert linked_list._first_node.item == "hello"
    assert linked_list._first_node.next.item == "world"
    assert linked_list._last_node.item == "!"

    # act
    linked_list.insert("new first")

    # assert: last_node must remain as is
    assert linked_list._last_node.item == "!"
    assert linked_list._first_node.item == "new first"
    assert len(linked_list) == 4

    # act: pop
    removed_item = linked_list.pop()

    # assert: last element should remain as is
    assert removed_item == "new first"
    assert linked_list._last_node.item == "!"
    assert linked_list._first_node.item == "hello"
    assert len(linked_list) == 3

    # act and assert: pop more
    assert linked_list.pop() == "hello"
    assert linked_list._last_node.item == "!"
    assert linked_list._first_node.item == "world"
    assert len(linked_list) == 2

    assert linked_list.pop() == "world"
    assert linked_list._first_node.item == "!"  # first and last are the same now!
    assert linked_list._last_node.item == "!"
    assert len(linked_list) == 1

    # act: left insert
    linked_list.insert("hi")

    # assert
    assert len(linked_list) == 2
    assert linked_list._first_node.item == "hi"
    assert linked_list._last_node.item == "!"

    # act and assert: pop
    assert linked_list.pop() == "hi"

    assert len(linked_list) == 1
    assert linked_list._first_node.item == "!"
    assert linked_list._last_node.item == "!"

    # act: insert right
    linked_list.insert_right("last one")
    assert len(linked_list) == 2
    assert linked_list._first_node.item == "!"  # first and last diverge again
    assert linked_list._last_node.item == "last one"

    # act: final pops
    assert linked_list.pop() == "!"
    assert linked_list.pop() == "last one"

    assert len(linked_list) == 0
    assert linked_list._first_node is None
    assert linked_list._last_node is None
