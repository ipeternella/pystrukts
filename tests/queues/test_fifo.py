"""
Module with tests for the queue (FIFO) data structures.
"""
import pytest

from algorithms.queues.exceptions import EmptyQueue
from algorithms.queues.fifo import Queue


def test_should_enqueue_and_assert_queue_length():
    # arrange
    q = Queue()
    assert len(q) == 0

    # act
    q.enqueue("hello")
    q.enqueue("world")
    q.enqueue("!")

    # assert
    assert len(q) == 3


def test_should_enqueue_and_dequeue_items():
    # arrange
    q = Queue()

    # act
    q.enqueue("first")  # first in, must be the first out!
    q.enqueue("second")
    q.enqueue("third")

    # assert FIFO dynamics
    assert q.dequeue() == "first"
    assert q.dequeue() == "second"
    assert q.dequeue() == "third"
    assert len(q) == 0

    # act: readd some elements
    q.enqueue("fourth")
    q.enqueue("fifth")

    # assert: final dequeues
    assert q.dequeue() == "fourth"
    assert q.dequeue() == "fifth"
    assert len(q) == 0


def test_should_traverse_queue_without_dequeing_items():
    # arrange
    q = Queue()

    q.enqueue("first")  # first in, must be the first out!
    q.enqueue("second")
    q.enqueue("third")

    assert len(q) == 3

    # act
    dequeued_items = [item for item in q]

    # assert
    assert dequeued_items == ["first", "second", "third"]  # FIFO dynamic
    assert len(q) == 0


def test_should_raise_if_dequeue_is_called_on_empty_queue():
    # arrange
    q = Queue()
    q.enqueue(1)

    # act and assert
    q.dequeue()  # ok

    with pytest.raises(EmptyQueue):
        q.dequeue()
