"""
Module with binary search tree implementation.
"""
from __future__ import annotations

from typing import Generic
from typing import Optional

from pystrukts._types.comparable import KT
from pystrukts._types.comparable import VT


class BSTNode(Generic[KT, VT]):
    """
    Represents a binary search tree node.
    """

    key: KT
    value: VT
    parent: Optional[BSTNode[KT, VT]]
    left: Optional[BSTNode[KT, VT]]
    right: Optional[BSTNode[KT, VT]]

    def __init__(self, key: KT, value: VT) -> None:
        self.key = key
        self.value = value
        self.parent = None
        self.left = None
        self.right = None


class BSTree(Generic[KT, VT]):
    """
    Represents a binary search tree.
    """

    root: Optional[BSTNode[KT, VT]]

    def __init__(self) -> None:
        self.root = None

    def height(self) -> int:
        """
        Computes the height of the binary search tree.
        """
        return self.height_from_node(self.root)

    def height_from_node(self, node: Optional[BSTNode]) -> int:
        """
        Computes the height of the binary search tree starting from a base node.
        """
        if node is None:
            return -1

        return max(self.height_from_node(node.left), self.height_from_node(node.right)) + 1

    def get(self, key: KT) -> Optional[VT]:
        """
        Searches for a given key in the binary search tree and returns its value if
        such key was found. Otherwise, returns None.
        """
        searched_node = self.root

        while searched_node is not None:
            if searched_node.key == key:
                return searched_node.value

            if key < searched_node.key:
                searched_node = searched_node.left
            else:
                searched_node = searched_node.right

        return None

    def insert(self, key: KT, value: VT) -> None:
        """
        Inserts a new node into the binary search tree.
        """
        new_node = BSTNode(key, value)
        self._insert(new_node)

    def _insert(self, new_node: BSTNode[KT, VT]) -> None:
        current_node = self.root
        parent: Optional[BSTNode[KT, VT]] = None

        while current_node is not None:
            # stores the last seen parent as a reference for the insertion
            parent = current_node  # type: ignore[assignment]

            if new_node.key >= current_node.key:
                current_node = current_node.right
            else:
                current_node = current_node.left

        # None if the tree was empty
        new_node.parent = parent

        if parent is None:
            self.root = new_node  # empty tree
        elif new_node.key >= parent.key:
            parent.right = new_node
        else:
            parent.left = new_node
