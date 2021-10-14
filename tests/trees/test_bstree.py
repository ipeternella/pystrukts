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

    def test_should_return_max_and_min_values_of_bstree(self):
        """
        Should return max and min values of a binary search tree.
        """
        # arrange
        tree = self.build_bstree_one()

        # act
        min_value = tree.min()
        max_value = tree.max()

        # assert
        self.assertEqual(min_value, 2)
        self.assertEqual(max_value, 19)

        # arrange - empty tree
        tree = BSTree()

        # act
        min_value = tree.min()
        max_value = tree.max()

        # assert
        self.assertIsNone(min_value)
        self.assertIsNone(max_value)

        # arrange - tree of a single node
        tree = self.build_bstree_three()

        # act
        min_value = tree.min()
        max_value = tree.max()

        # assert
        self.assertEqual(min_value, 12)
        self.assertEqual(max_value, 12)

    def test_should_delete_items_from_bstree(self):
        """
        Should delete items from a bstree.
        """
        # arrange
        #         12
        #      /      \
        #     5        18
        #   /   \     /  \
        #  2     9   15   19
        #           /  \
        #         13   17
        tree = self.build_bstree_one()

        # act
        deleted = tree.delete(15)

        # assert - height == 3
        #         12
        #      /      \
        #     5        18
        #   /   \     /  \
        #  2     9   17   19
        #           /
        #         13
        self.assertEqual(deleted, 15)
        self.assertEqual(tree.root.right.left.key, 17)
        self.assertEqual(tree.root.right.left.left.key, 13)
        self.assertEqual(tree.height(), 3)

        # act - delete root node
        deleted = tree.delete(12)

        # assert - height == 2
        #         13
        #      /      \
        #     5        18
        #   /   \     /  \
        #  2     9   17   19
        self.assertEqual(deleted, 12)
        self.assertEqual(tree.root.key, 13)
        self.assertEqual(tree.root.left.key, 5)
        self.assertEqual(tree.root.right.key, 18)
        self.assertEqual(tree.height(), 2)

        # act
        deleted = tree.delete(13)

        # assert - state:
        #         17
        #      /      \
        #     5        18
        #   /   \        \
        #  2     9       19
        self.assertEqual(deleted, 13)
        self.assertEqual(tree.root.key, 17)
        self.assertEqual(tree.root.right.key, 18)
        self.assertEqual(tree.root.left.key, 5)

        # act
        deleted = tree.delete(18)

        # assert - state:
        #         17
        #      /      \
        #     5        19
        #   /   \
        #  2     9
        self.assertEqual(tree.root.key, 17)
        self.assertEqual(tree.root.right.key, 19)

        # act
        deleted = tree.delete(2)
        deleted = tree.delete(9)

        # assert - height == 1
        #         17
        #      /      \
        #     5        19
        self.assertEqual(deleted, 9)
        self.assertEqual(tree.height(), 1)
        self.assertEqual(tree.root.key, 17)
        self.assertEqual(tree.root.left.key, 5)
        self.assertEqual(tree.root.right.key, 19)

        # act
        deleted = tree.delete(5)
        deleted = tree.delete(19)

        # assert - height == 0
        #         17 (final node)
        self.assertEqual(tree.root.key, 17)
        self.assertEqual(tree.height(), 0)

        # act - nonexistent key
        deleted = tree.delete(20)

        # assert
        self.assertIsNone(deleted)

        # act - tree has been emptied
        deleted = tree.delete(17)

        # assert
        self.assertEqual(deleted, 17)
        self.assertEqual(tree.height(), -1)  # empty tree
        self.assertIsNone(tree.root)

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
