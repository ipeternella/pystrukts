"""
Module with a binary search tree implementation.
"""
from __future__ import annotations

from typing import Generic
from typing import Optional

from algorithms.searching.types import KT
from algorithms.searching.types import VT


class Node(Generic[KT, VT]):
    """
    Represents a binary node of a tree with two siblings. Stores the amount of nodes below
    this node in order to boost searching algorithms performance.
    """

    # this node's state
    _key: KT
    _value: VT

    # nodes below references (siblings)
    _total_nodes_below: int
    _left: Optional[Node[KT, VT]]
    _right: Optional[Node[KT, VT]]

    def __init__(
        self,
        key: KT,
        value: VT,
        nodes_below_count: int = 0,
        right_sibling: Node[KT, VT] = None,
        left_sibling: Node[KT, VT] = None,
    ) -> None:
        self._key = key
        self._value = value
        self._total_nodes_below = nodes_below_count
        self._right = right_sibling
        self._left = left_sibling

    @property
    def key(self) -> KT:
        return self._key

    @property
    def value(self) -> VT:
        return self._value

    @value.setter
    def value(self, value: VT) -> None:
        self._value = value

    @property
    def left(self) -> Optional[Node[KT, VT]]:
        return self._left

    @property
    def right(self) -> Optional[Node[KT, VT]]:
        return self._right

    @property
    def total_nodes_below(self) -> int:
        return self._total_nodes_below

    def add_left_sibling(self, node: Node[KT, VT]) -> None:
        """
        Adds a left sibling node below this node.
        """
        self._total_nodes_below += 1
        self._left = node

    def add_right_sibling(self, node: Node[KT, VT]) -> None:
        """
        Adds a right sibling node below this node.
        """
        self._total_nodes_below += 1
        self._right = node


class BinarySearchTree(Generic[KT, VT]):
    """
    Binary Search Tree implementation: for any given node, its own value is larger than
    all keys in all nodes of its left subtree and smaller than all keys in all nodes of its
    right subtree.
    """

    _root: Node[KT, VT]

    def __init__(self, root_key: KT, root_value: VT) -> None:
        self._root = Node(root_key, root_value)

    @property
    def root(self) -> Node[KT, VT]:
        return self._root

    def get(self, key: KT) -> VT:
        return self._get(key, self._root)

    def put(self, key: KT, value: VT) -> None:
        self._put(key, value, self._root)

    def _get(self, key: KT, node: Node[KT, VT]) -> VT:
        # base case
        if key == node.key:
            return node.value

        # reduce the problem: recursion!
        if key > node.key:
            # nowhere to go: not found!
            if node.right is None:
                raise KeyError

            return self._get(key, node.right)

        # nowhere to go: not found!
        if node.left is None:
            raise KeyError

        # follow the left side of the binary tree
        return self._get(key, node.left)

    def _put(self, key: KT, value: VT, node: Node[KT, VT]) -> None:
        # base case: key was found -> update it!
        if key == node.key:
            node.value = value

        elif key > node.key:
            if node.right is None:  # nowhere else to go, time to add a new key!
                new_node = Node(key, value)
                node.add_right_sibling(new_node)

                return

            self._put(key, value, node.right)

        else:
            if node.left is None:  # nowhere else to go, time to add a new key!
                new_node = Node(key, value)
                node.add_left_sibling(new_node)

                return

            self._put(key, value, node.left)
