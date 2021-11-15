"""
Module with tests for min. priority queues.
"""
import unittest

from pystrukts.queues.min_priority_queue import MinPriorityQueue


class MinPriorityQueueTestSuite(unittest.TestCase):
    """
    Tests for min. priority queues.
    """

    def test_should_enqueue_and_dequeue_elements_on_priority_queue(self):
        """
        Should enqueue and dequeue elements on a min. priority queue.
        """
        # arrange
        q = MinPriorityQueue()

        # act
        q.enqueue(10, "x")
        q.enqueue(7, "i")
        q.enqueue(7, "w")
        q.enqueue(1, "z")

        # assert
        self.assertFalse(q.is_empty())
        self.assertEqual(len(q), 4)

        # act - dequeue based on min. priority policy
        self.assertEqual(q.dequeue(), "z")
        self.assertEqual(len(q), 3)

        self.assertEqual(q.dequeue(), "i")
        self.assertEqual(len(q), 2)

        self.assertEqual(q.dequeue(), "w")
        self.assertEqual(len(q), 1)

        self.assertEqual(q.dequeue(), "x")
        self.assertEqual(len(q), 0)

        self.assertIsNone(q.dequeue())

        # act - enqueue more elements
        q.enqueue(15, "k")
        q.enqueue(6, "y")

        # assert
        self.assertEqual(len(q), 2)

        self.assertEqual(q.dequeue(), "y")
        self.assertEqual(len(q), 1)

        self.assertEqual(q.dequeue(), "k")
        self.assertEqual(len(q), 0)

        self.assertIsNone(q.dequeue())

        # act - enqueue more elements and then reduce priority
        q.enqueue(5, "a")
        q.enqueue(10, "b")
        q.reduce_priority("b", 1)

        # assert
        self.assertEqual(q.dequeue(), "b")  # priority changed
        self.assertEqual(q.dequeue(), "a")
