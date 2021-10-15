import unittest

from pystrukts.trees.bplustree import BPlusTree
from tests.trees.utils import tmp_btree_file


class TestSuiteBPlusTree(unittest.TestCase):
    """
    B+tree testing suite.
    """

    def test_should_write_and_read_bplustree_pages_from_disk(self):
        """
        Should write and read B+tree pages from disk.
        """
        with tmp_btree_file() as btree_file:
            # arrange
            page_data = b"hello world 1"
            page_size = len(page_data)
            tree = BPlusTree(btree_file, page_size=page_size)

            # act
            tree.memory_storage.write_page(0, b"hello world 1")
            tree.memory_storage.write_page(1, b"hello world 2")

            page_0 = tree.memory_storage.read_page(0)
            page_1 = tree.memory_storage.read_page(1)

            # assert
            str_0 = page_0.decode("utf-8")
            str_1 = page_1.decode("utf-8")

            self.assertEqual(str_0, "hello world 1")
            self.assertEqual(str_1, "hello world 2")
