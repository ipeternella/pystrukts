"""
Module with tests for the stack data structure.
"""
import pytest

from algorithms.stacks.exceptions import EmptyStack
from algorithms.stacks.lifo import Stack


def test_should_push_and_assert_stack_length():
    # arrange
    stack = Stack()
    assert len(stack) == 0

    # act
    stack.push("hello")
    stack.push("world")
    stack.push("!")

    # assert
    assert len(stack) == 3


def test_should_push_and_pop_until_empty():
    # arrange
    stack = Stack()

    # act
    stack.push("1")
    stack.push("2")
    stack.push("3")

    # assert
    assert stack.pop() == "3"  # last in, first out!
    assert stack.pop() == "2"
    assert stack.pop() == "1"
    assert len(stack) == 0

    # act: push again
    stack.push("4")
    stack.push("5")

    # assert: final len
    assert len(stack) == 2
    assert stack.pop() == "5"
    assert stack.pop() == "4"
    assert len(stack) == 0


def test_traverse_on_stack():
    # arrange
    stack = Stack()
    stack.push("first")
    stack.push("second")
    stack.push("third")

    # act
    popped_items = [item for item in stack]

    # assert
    assert popped_items == ["third", "second", "first"]  # LIFO dynamic
    assert len(stack) == 0


def test_should_raise_if_pop_is_called_on_empty_stack():
    # arrange
    stack = Stack()
    assert len(stack) == 0

    # act and assert
    with pytest.raises(EmptyStack):
        stack.pop()
