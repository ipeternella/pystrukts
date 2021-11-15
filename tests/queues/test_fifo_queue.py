"""
Module with tests for FIFO queues.
"""
import unittest

from pystrukts.queues.fifo import Queue


class QueueTestSuite(unittest.TestCase):
    """
    Tests for queues that follow FIFO policies.
    """

    def test_should_enqueue_and_dequeue_elements_on_queue(self):
        """
        Should enqueue and dequeue elements on the queue
        """
        # arrange
        q = Queue()

        # act
        q.enqueue(10, "x")
        q.enqueue(7, "i")
        q.enqueue(7, "i")
        q.enqueue(1, "z")

        # assert
        self.assertFalse(q.is_empty())
        self.assertEqual(len(q), 4)

        # act - dequeue elements
        self.assertEqual(q.dequeue(), "x")
        self.assertEqual(len(q), 3)

        self.assertEqual(q.dequeue(), "i")
        self.assertEqual(len(q), 2)

        self.assertEqual(q.dequeue(), "i")
        self.assertEqual(len(q), 1)

        self.assertEqual(q.dequeue(), "z")
        self.assertEqual(len(q), 0)
        self.assertTrue(q.is_empty())

        # act - enqueue more elements
        q.enqueue(15, "k")
        q.enqueue(6, "y")

        # assert
        self.assertEqual(len(q), 2)

        self.assertEqual(q.dequeue(), "k")
        self.assertEqual(len(q), 1)

        self.assertEqual(q.dequeue(), "y")
        self.assertEqual(len(q), 0)

        self.assertIsNone(q.dequeue())
