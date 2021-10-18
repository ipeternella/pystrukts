import unittest

from pystrukts._types.basic import Endianness
from pystrukts.trees.bplustree.bplustree import BPlusTree
from pystrukts.trees.bplustree.memory import PagedFileMemory
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
            # arrange - should store settings on disk
            BPlusTree(btree_file, page_size=200, max_key_size=7, max_value_size=14)

            # act
            reopened_tree: BPlusTree[int, str] = BPlusTree(btree_file, page_size=200)

            # assert
            self.assertEqual(reopened_tree.memory.last_used_page, 1)
            self.assertEqual(reopened_tree.memory.page_size, 200)
            self.assertEqual(reopened_tree.memory.max_key_size, 7)
            self.assertEqual(reopened_tree.memory.max_value_size, 14)

    def create_paged_file_memory(
        self,
        tree_file: str,
        page_size: int = 4096,
        max_key_size: int = 8,
        max_value_size: int = 8,
        endianness: Endianness = "big",
    ) -> PagedFileMemory:
        return PagedFileMemory(page_size, max_key_size, max_value_size, endianness, tree_file)
