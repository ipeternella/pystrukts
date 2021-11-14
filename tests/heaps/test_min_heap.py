"""
Module with tests for the min heap structure.
"""
import unittest

from pystrukts.heaps.min_heap import MinHeap


class MinHeapTestSuite(unittest.TestCase):
    """
    Tests for the min. heap data structure.
    """

    def test_should_raise_error_when_build_wrong_heap(self):
        """
        Should raise an error when building a min heap with wronng list shape.
        """
        # arrange
        elements = ["z", "x", "b", "a"]

        # act and assert
        self.assertRaises(ValueError, MinHeap, elements)

        # arrange
        elements = [(5, "z"), (7, "x"), "b", (1, "a")]  # one wrong element

        # act and assert
        self.assertRaises(ValueError, MinHeap, elements)

    def test_should_build_min_heap_with_list(self):
        """
        Should build min heap with list.
        """
        # arrange
        elements = [(5, "z"), (7, "x"), (2, "b"), (1, "a")]

        # act
        min_heap: MinHeap[int, str] = MinHeap(elements)

        # assert
        expected_min_heap = [(1, "a"), (2, "b"), (5, "z"), (7, "x")]

        self.assertEqual(len(min_heap), 4)
        self.assertEqual(min_heap.heap, expected_min_heap)

    def test_should_remove_min_elements_from_heap(self):
        """
        Should remove min elements from heap as min
        """
        # arrange
        elements = [(5, "z"), (7, "x"), (2, "b"), (1, "a")]

        # act
        min_heap: MinHeap[int, str] = MinHeap(elements)

        # assert
        self.assertEqual(len(min_heap), 4)

        self.assertEqual(min_heap.extract_min(), "a")
        self.assertEqual(len(min_heap), 3)

        self.assertEqual(min_heap.extract_min(), "b")
        self.assertEqual(len(min_heap), 2)

        self.assertEqual(min_heap.extract_min(), "z")
        self.assertEqual(len(min_heap), 1)

        self.assertEqual(min_heap.extract_min(), "x")
        self.assertEqual(len(min_heap), 0)

        self.assertRaises(Exception, min_heap.extract_min)

        # act - re-insert values to the min heap
        min_heap.insert(7, "x")
        min_heap.insert(7, "x")
        min_heap.insert(2, "b")

        # assert
        self.assertEqual(len(min_heap), 3)
        self.assertEqual(min_heap.extract_min(), "b")

        self.assertEqual(len(min_heap), 2)
        self.assertEqual(min_heap.extract_min(), "x")

        self.assertEqual(len(min_heap), 1)
        self.assertEqual(min_heap.extract_min(), "x")

        self.assertEqual(len(min_heap), 0)
        self.assertRaises(Exception, min_heap.extract_min)
