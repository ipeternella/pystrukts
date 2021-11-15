"""
Module with tests for the min heap structure.
"""
import unittest

from pystrukts.heaps.exceptions import EmptyHeap
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

    def test_should_build_min_heap_without_list(self):
        """
        Should build min heap without a starter list.
        """
        # act
        min_heap: MinHeap[int, str] = MinHeap()

        # assert
        self.assertEqual(len(min_heap), 0)

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
        expected_min_heap_handles = {"a": 0, "b": 1, "z": 2, "x": 3}

        self.assertEqual(len(min_heap), 4)
        self.assertEqual(min_heap.heap, expected_min_heap)
        self.assertEqual(min_heap.handles, expected_min_heap_handles)

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

        self.assertRaises(EmptyHeap, min_heap.extract_min)

        # act - re-insert values to the min heap
        min_heap.insert(7, "x")
        min_heap.insert(7, "w")
        min_heap.insert(2, "b")

        # assert
        self.assertEqual(len(min_heap), 3)
        self.assertEqual(min_heap.extract_min(), "b")

        self.assertEqual(len(min_heap), 2)
        self.assertEqual(min_heap.extract_min(), "x")

        self.assertEqual(len(min_heap), 1)
        self.assertEqual(min_heap.extract_min(), "w")

        self.assertEqual(len(min_heap), 0)
        self.assertRaises(EmptyHeap, min_heap.extract_min)

    def test_should_remove_elements_using_handles(self):
        """
        Should remove elements from the heap using handles.
        """
        # arrange
        elements = [(5, "z"), (7, "x"), (2, "b"), (1, "a")]
        min_heap: MinHeap[int, str] = MinHeap(elements)

        # act
        min_heap.decrease_key_from_handle("x", 0)

        # assert
        self.assertEqual(min_heap.handles, {"x": 0, "z": 2, "b": 3, "a": 1})

        # act
        min_heap.decrease_key_from_handle("z", 0)  # z remain as is due to same priority
        self.assertEqual(min_heap.handles, {"x": 0, "z": 2, "b": 3, "a": 1})

        # assert
        x_priority = min_heap.heap[0][0]
        z_priority = min_heap.heap[2][0]

        self.assertEqual(x_priority, 0)
        self.assertEqual(z_priority, 0)

        self.assertEqual(min_heap.extract_min(), "x")
        self.assertEqual(min_heap.extract_min(), "z")
        self.assertEqual(min_heap.extract_min(), "a")
        self.assertEqual(min_heap.extract_min(), "b")

        self.assertEqual(len(min_heap), 0)
        self.assertEqual(len(min_heap.handles), 0)

        # act
        min_heap.insert(17, "p")
        min_heap.insert(10, "i")

        # assert
        self.assertEqual(min_heap.heap, [(10, "i"), (17, "p")])
        self.assertEqual(min_heap.handles, {"i": 0, "p": 1})
        self.assertEqual(len(min_heap), 2)
        self.assertEqual(len(min_heap.handles), 2)

        # act decrease priority from handle
        min_heap.decrease_key_from_handle("p", 2)

        # assert
        self.assertEqual(min_heap.heap, [(2, "p"), (10, "i")])
        self.assertEqual(min_heap.handles, {"p": 0, "i": 1})
