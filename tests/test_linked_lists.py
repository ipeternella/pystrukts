"""
Module with tests regarding linked lists data structures and algorithms.
"""
from algorithms.linked_lists import LinkedList


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
