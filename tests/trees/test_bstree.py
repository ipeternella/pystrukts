import unittest

from pystrukts.trees.bstree import BSTree


class TestSuiteBSTree(unittest.TestCase):
    """
    Binary search trees (BSTree) test suite.
    """

    def test_should_create_and_insert_new_items_on_bstree(self):
        """
        Should create and insert new items on a binary search tree.
        """
        # arrange
        tree: BSTree[int, str] = BSTree()

        # act
        tree.insert(10, "one")
        tree.insert(2, "two")
        tree.insert(15, "three")

        # assert
        self.assertEqual(tree.root.key, 10)
        self.assertEqual(tree.root.value, "one")

        self.assertEqual(tree.root.left.key, 2)
        self.assertEqual(tree.root.left.value, "two")
        self.assertIsNone(tree.root.left.left)
        self.assertIsNone(tree.root.left.right)

        self.assertEqual(tree.root.right.key, 15)
        self.assertEqual(tree.root.right.value, "three")
        self.assertIsNone(tree.root.right.left)
        self.assertIsNone(tree.root.right.right)

    def test_should_find_keys_on_bstree(self):
        """
        Should find keys on a bstree fixture number one.
        """
        # arrange
        tree = self.build_bstree_one()

        # act and assert
        self.assertEqual(tree.get(12), 12)
        self.assertEqual(tree.get(2), 2)
        self.assertEqual(tree.get(17), 17)
        self.assertEqual(tree.get(19), 19)
        self.assertIsNone(tree.get(25))

    def test_should_compute_height_of_bstrees(self):
        """
        Should compute heights of some binary search trees.
        """
        # arrange
        tree_1 = self.build_bstree_one()
        tree_2 = self.build_bstree_two()
        tree_3 = self.build_bstree_three()  # single-noded bstree: just the root node
        tree_4 = BSTree()  # empty bstree

        # act
        height_1 = tree_1.height()
        height_2 = tree_2.height()
        height_3 = tree_3.height()
        height_4 = tree_4.height()

        # assert
        self.assertEqual(height_1, 3)
        self.assertEqual(height_2, 1)
        self.assertEqual(height_3, 0)  # single-noded: has no edges, hence its height == 0
        self.assertEqual(height_4, -1)  # tree without any nodes at all: invalid height == -1

    def build_bstree_one(self) -> BSTree[int, int]:
        r"""
        Binary search tree one used on tests:

                12
             /      \
            5        18
          /   \     /  \
         2     9   15   19
                  /  \
                13   17
        """
        tree: BSTree[int, int] = BSTree()

        # root
        tree.insert(12, 12)

        # first level
        tree.insert(5, 5)
        tree.insert(18, 18)

        # second level
        tree.insert(2, 2)
        tree.insert(9, 9)
        tree.insert(15, 15)
        tree.insert(19, 19)

        # third level
        tree.insert(13, 13)
        tree.insert(17, 17)

        return tree

    def build_bstree_two(self) -> BSTree[int, int]:
        r"""
        Binary search tree two used on tests:

          12
         /  \
        5   18
        """
        tree: BSTree[int, int] = BSTree()

        # root
        tree.insert(12, 12)

        # first level
        tree.insert(5, 5)
        tree.insert(18, 18)

        return tree

    def build_bstree_three(self) -> BSTree[int, int]:
        """
        Binary search tree number three used on tests (just the root node).
        """
        tree: BSTree[int, int] = BSTree()

        # root only
        tree.insert(12, 12)

        return tree
