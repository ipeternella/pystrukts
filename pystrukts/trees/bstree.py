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
        searched_node = self._get(key)

        if searched_node is not None:
            return searched_node.value

        return None

    def _get(self, key: KT) -> Optional[BSTNode[KT, VT]]:
        searched_node = self.root

        while searched_node is not None:
            if searched_node.key == key:
                return searched_node

            if key < searched_node.key:
                searched_node = searched_node.left
            else:
                searched_node = searched_node.right

        return searched_node

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

    def max(self) -> Optional[KT]:
        """
        Finds the maximum key of the bstree and returns it. If the tree is empty,
        returns None.
        """
        max_node = self._max(self.root)

        if max_node is not None:
            return max_node.key

        return None

    def _max(self, start_node: Optional[BSTNode[KT, VT]]) -> Optional[BSTNode[KT, VT]]:
        """
        Finds the maximum node of a bstree and returns it.
        """
        current_node = start_node
        max_node: Optional[BSTNode[KT, VT]] = None

        while current_node is not None:
            max_node = current_node
            current_node = current_node.right  # always traverses right for bigger values

        return max_node

    def min(self) -> Optional[KT]:
        """
        Finds the minimum node of a bstree and returns it. If the tree is empty,
        returns None.
        """
        min_node = self._min(self.root)

        if min_node is not None:
            return min_node.key

        return None

    def _min(self, start_node: Optional[BSTNode[KT, VT]]) -> Optional[BSTNode[KT, VT]]:
        """
        Finds the minimum node of a bstree.
        """
        current_node = start_node
        min_node: Optional[BSTNode[KT, VT]] = None

        while current_node is not None:
            min_node = current_node
            current_node = current_node.left  # always traverses left for smaller values

        return min_node

    def delete(self, key: KT) -> Optional[VT]:
        """
        Deletes a key (and its node) from the tree. If the key was found, and the node was deleted, then
        its value is returned. Otherwise, None is returned.
        """
        node = self._get(key)

        # key was not found
        if node is None:
            return None

        # trivial cases: one child is missing
        if node.left is None:
            self._transplant(node, node.right)
            return node.value

        elif node.right is None:
            self._transplant(node, node.left)
            return node.value

        # non-trivial cases: with children
        else:
            # here, successor_node is always != None or trivial cases are triggered
            successor_node: BSTNode[KT, VT] = self._min(node.right)  # type: ignore

            # successor is not a direct child the the node, so we must "free" it first
            if successor_node != node.right:
                self._transplant(successor_node, successor_node.right)
                successor_node.right = node.right
                node.right.parent = successor_node

            # direct child
            self._transplant(node, successor_node)
            successor_node.left = node.left
            node.left.parent = successor_node

            return node.value

    def _transplant(self, old_node: BSTNode[KT, VT], new_node: Optional[BSTNode[KT, VT]]) -> None:
        """
        Transplants (removes out of the tree) an old node for a newer node (which can be None) and
        adjusts the new node's parent reference.

        Note: this method does NOT adjust the new node's children and their references. It adjusts
        only the new node's parent. The children reference adjustment is responsibility of the caller.
        """
        # adjusts the old node's parent to point to the new node
        if old_node.parent is None:
            self.root = new_node  # old node was the root of the tree
        elif self._is_left_child(old_node):
            old_node.parent.left = new_node
        else:
            old_node.parent.right = new_node

        # if the new node is not None, adjusts its parent reference back
        if new_node is not None:
            new_node.parent = old_node.parent

    def _is_left_child(self, node: BSTNode[KT, VT]) -> bool:
        if node.parent is None:
            return False

        return node == node.parent.left
