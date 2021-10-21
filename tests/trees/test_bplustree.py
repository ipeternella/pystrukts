import unittest

from pystrukts._types.basic import Endianness
from pystrukts.trees.bplustree.bplustree import BPlusTree
from pystrukts.trees.bplustree.memory import PagedFileMemory
from pystrukts.trees.bplustree.node import LeafRecord
from tests.trees.utils import tmp_btree_file


class TestSuiteBPlusTree(unittest.TestCase):
    """
    B+tree testing suite.
    """

    def test_paged_file_memory_should_allocate_new_empty_page(self):
        """
        PagedFileMemory should create a new empty page.
        """
        with tmp_btree_file() as btree_file:
            # arrange
            memory = self.create_paged_file_memory(btree_file)

            # act
            page_number = memory.allocate_page()

            # assert
            self.assertEqual(page_number, 1)  # page 0 is the tree settings page

            # act - read page
            page_data = memory.read_page(page_number)

            # assert
            expected_page_data = bytes(memory.page_size)

            self.assertEqual(len(page_data), memory.page_size)
            self.assertEqual(page_data.split(b"\n"), expected_page_data.split(b"\n"))

    def test_paged_file_memory_should_write_and_read_pages_from_disk(self):
        """
        PagedFileMemory should write and read pages from disk.
        """
        with tmp_btree_file() as btree_file:
            # arrange
            page_size = len(b"bytearray page 0")
            memory = self.create_paged_file_memory(btree_file, page_size=page_size)

            # act
            memory.write_page(0, b"bytearray page 0")
            memory.write_page(1, b"bytearray page 1")

            # assert
            page_0 = memory.read_page(0)
            page_1 = memory.read_page(1)

            str_0 = page_0.decode("utf-8")
            str_1 = page_1.decode("utf-8")

            self.assertEqual(str_0, "bytearray page 0")
            self.assertEqual(str_1, "bytearray page 1")

    def test_should_read_previous_tree_configuration_stored_on_disk(self):
        """
        Should read previous tree configuration stored on disk.
        """
        with tmp_btree_file() as btree_file:
            # arrange - should store settings on disk from main memory
            BPlusTree(btree_file, page_size=200, max_key_size=7, max_value_size=14)

            # act - should reopen the tree file and fetch the settings from disk this time
            reopened_tree: BPlusTree[int, str] = BPlusTree(btree_file, page_size=200)

            # assert
            self.assertEqual(reopened_tree.memory.last_used_page, 1)
            self.assertEqual(reopened_tree.memory.page_size, 200)
            self.assertEqual(reopened_tree.memory.max_key_size, 7)
            self.assertEqual(reopened_tree.memory.max_value_size, 14)

    def test_should_insert_new_items_into_bptree_without_splitting_root_node(self):
        """
        Should insert new items into a B+tree without splitting the root node.
        """
        with tmp_btree_file() as btree_file:
            # arrange
            tree: BPlusTree[int, str] = BPlusTree(btree_file, page_size=4096, max_key_size=40, max_value_size=100)
            value_5 = "value 5"
            value_10 = "value 10"
            value_15 = "value 15"
            value_4 = "value 4"

            # act
            tree.insert(5, value_5)
            tree.insert(10, value_10)
            tree.insert(15, value_15)
            tree.insert(4, value_4)

            # assert - tree root in memory
            expected_records = [
                LeafRecord(4, value_4),
                LeafRecord(5, value_5),
                LeafRecord(10, value_10),
                LeafRecord(15, value_15),
            ]

            self.assertTrue(tree.root.is_leaf)
            self.assertEqual(tree.root.records_count, 4)
            self.assertListEqual(tree.root.leaf_records, expected_records)
            self.assertEqual(tree.root.next_leaf_page, 0)
            self.assertIsNone(tree.root.next_leaf)

            # act - read from disk the tree node now
            root_from_disk = tree._disk_read(1)  # page 1 is the root (0 is the tree settings)

            # assert - tree root on disk
            self.assertTrue(root_from_disk.is_leaf)
            self.assertEqual(root_from_disk.records_count, 4)
            self.assertListEqual(root_from_disk.leaf_records, expected_records)
            self.assertEqual(root_from_disk.next_leaf_page, 0)
            self.assertIsNone(root_from_disk.next_leaf)

            # act and assert - search the tree for the keys without root splitting
            self.assertEqual(tree.get(15), value_15)
            self.assertEqual(tree.get(4), value_4)

    def test_should_insert_items_on_bplustree_until_root_is_split_and_find_keys_on_the_bplustree(self):
        """
        Should insert items on a B+tree until root is split and find keys on the B+tree.
        """
        with tmp_btree_file() as btree_file:
            # arrange - t == 2 for leaves
            tree: BPlusTree[int, int] = BPlusTree(btree_file, page_size=39, max_key_size=5, max_value_size=5)

            # act - insert until root node is split
            tree.insert(1, 1)
            tree.insert(2, 2)
            tree.insert(3, 3)
            tree.insert(4, 4)

            # assert - root (inner node) and leaf nodes
            self.assertFalse(tree.root.is_leaf)  # after split, root is not a leaf anymore
            self.assertEqual(tree.root.records_count, 1)
            self.assertEqual(tree.root.inner_records[0].key, 2)

            # first child of the root is a leaf node with two keys <= 2: {1: 1, 2: 2}
            self.assertTrue(tree.root.first_node.is_leaf)
            self.assertEqual(tree.root.first_node.records_count, 2)
            self.assertEqual(tree.root.first_node.leaf_records[0].key, 1)
            self.assertEqual(tree.root.first_node.leaf_records[0].value, 1)
            self.assertEqual(tree.root.first_node.leaf_records[1].key, 2)
            self.assertEqual(tree.root.first_node.leaf_records[1].value, 2)

            # second child of the root is a leaf node with two keys > 2: {3: 3, 4: 4}
            self.assertTrue(tree.root.inner_records[0].next_node.is_leaf)
            self.assertEqual(tree.root.inner_records[0].next_node.records_count, 2)

            self.assertEqual(tree.root.inner_records[0].next_node.leaf_records[0].key, 3)
            self.assertEqual(tree.root.inner_records[0].next_node.leaf_records[0].value, 3)

            self.assertEqual(tree.root.inner_records[0].next_node.leaf_records[1].key, 4)
            self.assertEqual(tree.root.inner_records[0].next_node.leaf_records[1].value, 4)

            # act and assert - search for keys in the tree and assert
            self.assertEqual(tree.get(1), 1)
            self.assertEqual(tree.get(2), 2)
            self.assertEqual(tree.get(3), 3)
            self.assertEqual(tree.get(4), 4)
            self.assertIsNone(tree.get(101))
            self.assertIsNone(tree.get(-1))

            # act - load tree from disk
            tree_from_disk: BPlusTree[int, int] = BPlusTree(btree_file)

            # assert - nodes
            self.assertEqual(tree_from_disk.get(1), 1)
            self.assertEqual(tree_from_disk.get(2), 2)
            self.assertEqual(tree_from_disk.get(3), 3)
            self.assertEqual(tree_from_disk.get(4), 4)
            self.assertIsNone(tree_from_disk.get(101))
            self.assertIsNone(tree_from_disk.get(-1))

    def create_paged_file_memory(
        self,
        tree_file: str,
        page_size: int = 4096,
        max_key_size: int = 8,
        max_value_size: int = 8,
        endianness: Endianness = "big",
    ) -> PagedFileMemory:
        return PagedFileMemory(page_size, max_key_size, max_value_size, endianness, tree_file)
