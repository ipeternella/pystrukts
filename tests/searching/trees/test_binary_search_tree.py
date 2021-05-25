"""
Module with tests written for tree nodes classes.
"""
import pytest

from algorithms.searching.trees.binary_search_tree import BinarySearchTree
from algorithms.searching.trees.binary_search_tree import Node
from tests.searching.trees.utils import assert_node
from tests.searching.trees.utils import binary_tree_walk


def test_should_create_root_node_with_no_siblings():
    # arrange & act
    node = Node("key1", 1)

    # assert
    assert node.key == "key1"
    assert node.value == 1
    assert node.total_nodes_below == 0


def test_should_create_root_node_with_two_siblings():
    # arrange
    root_node = Node("root", 1)
    left_sibling_node = Node("left", 2)
    right_sibling_node = Node("right", 3)

    # assert
    assert root_node.total_nodes_below == 0

    # act
    root_node.add_left_sibling(left_sibling_node)

    # assert
    assert root_node.total_nodes_below == 1

    # act
    root_node.add_right_sibling(right_sibling_node)

    # assert
    assert root_node.total_nodes_below == 2
    assert root_node.left == left_sibling_node
    assert root_node.right == right_sibling_node

    assert left_sibling_node.total_nodes_below == 0
    assert right_sibling_node.total_nodes_below == 0


def test_should_find_key_in_binary_search_tree():
    r"""
    Initial tree:

            10
           /  \
          6   15
         / \
        3  8

    Final tree:

              10
            /    \
           6     15
         /  \   /
        3   8  12
          /
         7
    """
    # arrange
    tree: BinarySearchTree[int, int] = BinarySearchTree(10, 10)
    tree.put(6, 6)
    tree.put(15, 15)
    tree.put(8, 8)
    tree.put(3, 3)

    # act - get an existent value
    value = tree.get(3)

    # assert
    assert value == 3

    # act - update an existent value
    tree.put(8, 80)

    # assert
    assert tree.get(8) == 80

    # act & assert - attempt to get key that is not in the tree
    with pytest.raises(KeyError):
        tree.get(-1)

    # act - add a new node to the tree that's bigger than the root
    tree.put(12, 12)

    # assert
    assert tree.get(12) == 12

    # act - add a new node to the tree's that smaller than the root
    tree.put(7, 7)

    tree.get(12)

    # assert
    assert tree.get(7) == 7

    # assert final tree structure
    assert_node(tree, [], 10, 10)  # root
    assert_node(tree, ["->"], 15, 15)
    assert_node(tree, ["->", "->"], None)
    assert_node(tree, ["->", "<-"], 12, 12)
    assert_node(tree, ["->", "<-", "->"], None)
    assert_node(tree, ["->", "<-", "<-"], None)

    assert_node(tree, ["<-"], 6, 6)
    assert_node(tree, ["<-", "<-"], 3, 3)
    assert_node(tree, ["<-", "<-", "->"], None)
    assert_node(tree, ["<-", "<-", "<-"], None)

    assert_node(tree, ["<-", "->"], 8, 80)  # updated value
    assert_node(tree, ["<-", "->", "->"], None)
    assert_node(tree, ["<-", "->", "<-"], 7, 7)
    assert_node(tree, ["<-", "->", "<-", "->"], None)
    assert_node(tree, ["<-", "->", "<-", "<-"], None)
