"""
Module with utilities for testing trees.
"""

from typing import List
from typing import Optional

from algorithms.searching.trees.binary_search_tree import BinarySearchTree
from algorithms.searching.trees.binary_search_tree import Node
from algorithms.searching.types import KT
from algorithms.searching.types import VT


def assert_node(
    binary_tree: BinarySearchTree[KT, VT],
    path: List[str],
    expected_key: Optional[KT] = None,
    expected_value: Optional[VT] = None,
    expected_total_nodes_below: Optional[int] = None,
):
    tree_node = binary_tree_walk(binary_tree, path)

    try:
        assert tree_node.key == expected_key  # type: ignore
        assert tree_node.value == expected_value  # type: ignore
    except AttributeError:
        # tree_node is None
        assert expected_key is None
        assert expected_value is None
        assert expected_total_nodes_below is None


def binary_tree_walk(binary_tree: BinarySearchTree[KT, VT], path: List[str]) -> Optional[Node[KT, VT]]:
    """
    Given a path of directions, returns a given node of a tree.
    """
    current_node: Node[KT, VT] = binary_tree._root

    if not path:  # empty path []
        return binary_tree.root

    for direction in path:
        if direction == "<-":
            if current_node.left is None:
                return None

            current_node = current_node.left

        elif direction == "->":
            if current_node.right is None:
                return None

            current_node = current_node.right

        else:
            raise Exception("Unexpected direction for binary tree walk!")

    return current_node
