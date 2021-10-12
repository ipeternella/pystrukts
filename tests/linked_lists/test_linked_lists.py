"""
Module with tests of linked lists.
"""
import unittest

from pystrukts.linked_lists import LinkedList


class TestSuiteLinkedList(unittest.TestCase):
    """
    Test suite for linked lists.
    """

    def test_linked_list_new(self):
        """
        Should create an empty linked list.
        """
        # arrange and act
        linked_list = LinkedList()

        # assert
        self.assertEqual(len(linked_list), 0)
        self.assertIsNone(linked_list.first_node)
        self.assertIsNone(linked_list.last_node)

    def test_should_append_values_to_linked_list(self):
        """
        Should append new elements to a linked list.

        Expected final state: ["first", 1] <-> ["second", 2] <-> ["third", 3]
        """
        # arrange
        linked_list: LinkedList[str, int] = LinkedList()

        # act
        linked_list.append("first", 1)
        linked_list.append("second", 2)
        linked_list.append("third", 3)

        # assert - elements
        self.assertEqual(linked_list.first_node.key, "first")
        self.assertEqual(linked_list.first_node.value, 1)

        self.assertEqual(linked_list.first_node.next_node.key, "second")
        self.assertEqual(linked_list.first_node.next_node.value, 2)

        self.assertEqual(linked_list.last_node.key, "third")
        self.assertEqual(linked_list.last_node.value, 3)

        # assert - size
        self.assertEqual(len(linked_list), 3)

    def test_should_prepend_values_to_linked_list(self):
        """
        Should prepend new elements to a linked list.

        Expected final state: ["third", 3] <-> ["second", 2] <-> ["first", 1]
        """
        # arrange
        linked_list: LinkedList[str, int] = LinkedList()

        # act
        linked_list.prepend("first", 1)
        linked_list.prepend("second", 2)
        linked_list.prepend("third", 3)

        # assert - elements
        self.assertEqual(linked_list.first_node.key, "third")
        self.assertEqual(linked_list.first_node.value, 3)

        self.assertEqual(linked_list.first_node.next_node.key, "second")
        self.assertEqual(linked_list.first_node.next_node.value, 2)

        self.assertEqual(linked_list.last_node.key, "first")
        self.assertEqual(linked_list.last_node.value, 1)

        # assert - size
        self.assertEqual(len(linked_list), 3)

    def test_should_get_value_from_linked_list(self):
        """
        Should get values from a linked list.
        """
        # arrange
        linked_list: LinkedList[str, int] = LinkedList()
        linked_list.prepend("first", 1)
        linked_list.prepend("second", 2)
        linked_list.prepend("third", 3)

        # act
        first_value = linked_list.get("first")
        second_value = linked_list.get("second")
        third_value = linked_list.get("third")
        not_found = linked_list.get("fourth")

        # assert
        self.assertEqual(first_value, 1)
        self.assertEqual(second_value, 2)
        self.assertEqual(third_value, 3)
        self.assertIsNone(not_found)

    def test_should_delete_values_from_linked_list(self):
        """
        Should delete elements from a linked list from different list states.
        """
        # arrange
        linked_list: LinkedList[str, int] = LinkedList()

        # act - delete from empty list
        deleted = linked_list.delete("not_found")

        # assert
        self.assertEqual(len(linked_list), 0)
        self.assertIsNone(deleted)

        # arrange - insert single element (first node deletion)
        linked_list.append("first", 1)

        # act
        deleted = linked_list.delete("first")

        # assert
        self.assertEqual(deleted, 1)
        self.assertEqual(len(linked_list), 0)

        # arrange - insert two elements
        linked_list.append("first", 1)
        linked_list.append("last", 2)

        # act - delete a last node
        deleted = linked_list.delete("last")

        # assert
        self.assertEqual(deleted, 2)
        self.assertEqual(len(linked_list), 1)
        self.assertEqual(linked_list.first_node.key, "first")
        self.assertEqual(linked_list.first_node.value, 1)

        # arrange - inserts more two elements
        linked_list.append("second", 2)
        linked_list.append("third", 3)
        self.assertEqual(len(linked_list), 3)  # sanity check

        # act
        deleted = linked_list.delete("second")

        # assert
        self.assertEqual(deleted, 2)
        self.assertEqual(len(linked_list), 2)

        # act - empty the list
        deleted_first = linked_list.delete("first")
        deleted_third = linked_list.delete("third")
        deleted_not_found = linked_list.delete("not_found")

        # assert
        self.assertEqual(deleted_first, 1)
        self.assertEqual(deleted_third, 3)
        self.assertIsNone(deleted_not_found)
        self.assertEqual(len(linked_list), 0)
