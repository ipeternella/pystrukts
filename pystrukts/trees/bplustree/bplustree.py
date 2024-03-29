"""
Module with a B+tree implementation.
"""
from __future__ import annotations

from typing import Generic
from typing import Optional
from typing import Tuple

from pystrukts._types.basic import Endianness
from pystrukts._types.basic import StrPath
from pystrukts._types.comparable import KT
from pystrukts._types.comparable import VT
from pystrukts.trees.bplustree.memory import PagedFileMemory
from pystrukts.trees.bplustree.node import BPTNode
from pystrukts.trees.bplustree.node import InnerRecord
from pystrukts.trees.bplustree.node import LeafRecord
from pystrukts.trees.bplustree.serializers import DefaultSerializer
from pystrukts.trees.bplustree.serializers import Serializer
from pystrukts.trees.bplustree.settings import INNER_NODE_HEADERS_SPACE
from pystrukts.trees.bplustree.settings import LEAF_NODES_HEADERS_SPACE
from pystrukts.trees.bplustree.settings import NODE_POINTER_BYTE_SPACE


class BPlusTree(Generic[KT, VT]):
    """
    Class that represents a B+tree.
    """

    root: BPTNode[KT, VT]
    memory: PagedFileMemory
    inner_degree: int
    leaf_degree: int

    key_serializer: Serializer[KT]
    value_serializer: Serializer[VT]
    endianness: Endianness = "big"

    def __init__(
        self,
        tree_file: Optional[StrPath] = None,
        key_serializer: Optional[Serializer[KT]] = None,
        value_serializer: Optional[Serializer[VT]] = None,
        page_size: int = 4096,
        max_key_size: int = 8,
        max_value_size: int = 32,
    ) -> None:
        self.key_serializer = key_serializer if key_serializer is not None else DefaultSerializer[KT]()
        self.value_serializer = value_serializer if value_serializer is not None else DefaultSerializer[VT]()
        self.memory = PagedFileMemory(page_size, max_key_size, max_value_size, self.endianness, tree_file)
        self.inner_degree = self._compute_inner_degree()
        self.leaf_degree = self._compute_leaf_degree()

        if self.memory.is_new_file:
            self.root = self._create_root()
        else:
            self.root = self._read_root()

    def insert(self, key: KT, value: VT) -> None:
        """
        Inserts a new key and value on the B+tree. Splits the root node or children nodes
        as the max number of keys are exceeded on the nodes according to the tree's degree.
        """
        if self._is_full(self.root):
            old_root = self.root

            # new root is never a leaf node
            new_root = self._create_node(is_leaf=False)
            self.root = new_root
            self._swap_pages(old_root, new_root)  # swap disk pages so that the new root stays on page 1

            # first node pointer is always created upon inner split
            new_root.first_node = old_root
            new_root.first_node_page = old_root.disk_page

            # splits the new root's child (old root) which is full to add the new key/value
            self._split_child(new_root, old_root, 0)
            self._insert_non_full(new_root, key, value)
        else:
            self._insert_non_full(self.root, key, value)

    def get(self, key: KT) -> Optional[VT]:
        """
        Looks for a key on the B+tree. If it's not found, returns None.
        """
        result = self._get(self.root, key)

        if result is not None:
            node, i = result  # only leaf nodes can contain values, so we have a leaf node
            return node.leaf_records[i].value

        return None

    def _get(self, node: BPTNode[KT, VT], key: KT) -> Optional[Tuple[BPTNode[KT, VT], int]]:
        """
        Finds a leaf node along with it's corresponding index int of its 'leaf_records' array
        containg the record with the value associated with the given key. If no such node is found,
        returns None.
        """
        i = 0

        if node.is_leaf:
            while i < node.records_count and key > node.leaf_records[i].key:
                i += 1

            if i < node.records_count and key == node.leaf_records[i].key:
                return node, i

            return None

        # inner node searching
        while i < node.records_count and key > node.inner_records[i].key:
            i += 1

        # here we have an inner node, if i == 0, it's smaller than all keys
        # so look at the first child page (out of the inner_records)
        if i == 0:
            next_node_page = node.first_node_page
            next_node = node.first_node
        else:
            i -= 1  # [!]: key is bigger than first page keys, but inner_records starts at i == 0

            next_node_page = node.inner_records[i].next_node_page
            next_node = node.inner_records[i].next_node

        # check if the next inner node is in memory
        if next_node is not None:
            return self._get(next_node, key)

        # if not in memory, read it from disk and perform recursion
        return self._get(self._disk_read(next_node_page), key)

    def _disk_write(self, node: BPTNode[KT, VT]) -> None:
        """
        Writes a given node to disk according to its page attribute by calling the memory allocator.
        """
        node_page = node.disk_page
        node_data = node.to_page(
            self.memory.page_size, self.memory.max_key_size, self.memory.max_value_size, self.endianness
        )
        self.memory.write_page(node_page, node_data)

    def _disk_read(self, node_page: int) -> BPTNode[KT, VT]:
        """
        Reads a given node from disk according to its page attribute by calling the memory allocator.
        """
        page_data = self.memory.read_page(node_page)

        node_from_disk: BPTNode[KT, VT] = BPTNode(True, node_page, self.key_serializer, self.value_serializer)
        node_from_disk.load_from_page(page_data, self.memory.max_key_size, self.memory.max_value_size, self.endianness)

        return node_from_disk

    def _is_full(self, node: BPTNode[KT, VT]) -> bool:
        """
        Checks if the given node is full of keys according to the tree's degree which takes
        into account the disk page sizes.
        """
        degree = self.leaf_degree if node.is_leaf else self.inner_degree

        return node.records_count == 2 * degree - 1

    def _insert_non_full(self, node: BPTNode[KT, VT], key: KT, value: VT) -> None:
        """
        Inserts a new key into a non-full node or raise an exception.
        """
        # starts at the end of the inserted keys so far
        i = node.records_count - 1

        if node.is_leaf:
            new_record = LeafRecord(key, value)

            # finds final sorted position of the key (notice we need to do i + 1 after the loop)
            while i >= 0 and key < node.leaf_records[i].key:
                i -= 1

            # shift keys right to find a new spot for the new key
            node.leaf_records.insert(i + 1, new_record)

            self._disk_write(node)
        else:
            while i >= 0 and key < node.inner_records[i].key:
                i -= 1

            child_node_page = node.inner_records[i].next_node_page
            child_node = self._disk_read(child_node_page)
            node.inner_records[i].next_node = child_node

            if self._is_full(child_node):
                self._split_child(node, child_node, i)
                if key > node.inner_records[i].key:
                    i += 1

            # as splitting adds a new key in the current node, refetch child
            child_node_page = node.inner_records[i].next_node_page
            child_node = self._disk_read(child_node_page)
            node.inner_records[i].next_node = child_node

            self._insert_non_full(child_node, key, value)

    def _split_child(self, parent_node: BPTNode[KT, VT], child_node: BPTNode[KT, VT], i: int) -> None:
        """
        Splits the child according to whether it is a leaf or inner node. Notice that the parent node must
        be an inner node or it would not have children.
        """
        if child_node.is_leaf:
            self._split_leaf_child(parent_node, child_node, i)
        else:
            self._split_inner_child(parent_node, child_node, i)

    def _split_inner_child(self, parent_node: BPTNode[KT, VT], child_node: BPTNode[KT, VT], i: int) -> None:
        """
        Splits the i-th full child of the given parent node. Notice that the parent node, as it has a child, is
        an inner node (non-leaf) but the child itself can either be a leaf or an inner-node.
        """
        new_node = self._create_node(is_leaf=False)  # creates a new inner node
        degree = self.inner_degree

        # copies lower part of the full child node to the new node
        for j in range(0, degree - 1):
            record = child_node.inner_records[degree + j]
            new_node.inner_records.append(InnerRecord(record.key, record.next_node_page, record.next_node))

            # removes copied nodes from child node
            child_node.leaf_records.pop(degree + j)

        # inserts new key into the non-full inner node parent and make it point to the new node
        parent_node.inner_records.insert(
            i, InnerRecord(child_node.inner_records[degree - 1].key, new_node.disk_page, new_node)
        )
        child_node.inner_records.pop(degree - 1)  # removes the split key from the child to 'pass' it to the parent

        # disk persistance of the split
        self._disk_write(child_node)
        self._disk_write(new_node)
        self._disk_write(parent_node)

    def _split_leaf_child(self, parent_node: BPTNode[KT, VT], child_node: BPTNode[KT, VT], i: int) -> None:
        """
        Splits the i-th full child of the given parent node. Notice that the parent node, as it has a child, is
        an inner node and never a leaf node.
        """
        new_node = self._create_node(is_leaf=True)
        degree = self.leaf_degree

        # copies lower part of the full child node to the new node
        for j in range(0, degree - 1):
            record = child_node.leaf_records[degree + j]
            new_node.leaf_records.append(LeafRecord(record.key, record.value))

            # removes copied nodes from child node
            child_node.leaf_records.pop(degree + j)

        # inserts new key into the non-full inner node parent and make it point to the new node
        parent_node.inner_records.insert(
            i, InnerRecord(child_node.leaf_records[degree - 1].key, new_node.disk_page, new_node)
        )

        # disk persistance of the split
        self._disk_write(child_node)
        self._disk_write(new_node)
        self._disk_write(parent_node)

    def _compute_inner_degree(self) -> int:
        """
        Computes the degree (t) of the B+tree in order to use to decide when a given node is full or not. Here
        the degree of the tree is computed based on the amount of records that are able to fit a single disk page.

        Maximum allowed keys for any node: (2*t - 1) keys and 2*t children
        Minimum allowed keys for any node: (t - 1) keys and t children

        2*t - 1 == "max keys in node on a single page" -> 2*t - 1 == free_page_size / each_record_size and solve for t
        """
        page_headers_size = INNER_NODE_HEADERS_SPACE
        each_record_size = NODE_POINTER_BYTE_SPACE + self.memory.max_key_size
        free_page_size = self.memory.page_size - page_headers_size
        degree = int((free_page_size / each_record_size + 1) / 2)  # max amount of keys in inner nodes

        if degree <= 0:
            raise ValueError(
                "Impossible disk page memory layout for inner nodes: B+tree's degree <= 0! Please, "
                "increase the page size or reduce the max key value size."
            )

        return degree

    def _compute_leaf_degree(self) -> int:
        """
        Computes the degree (t) of the B+tree for leaf nodes as their memory layout is different than inner nodes as
        key values take up more space. As a consequence, a leaf node becomes full with less records than an inner
        code and, as such, has a different degree.
        """
        page_headers_size = LEAF_NODES_HEADERS_SPACE
        each_record_size = self.memory.max_key_size + self.memory.max_value_size
        free_page_size = self.memory.page_size - page_headers_size
        degree = int((free_page_size / each_record_size + 1) / 2)

        if degree <= 0:
            raise ValueError(
                "Impossible disk page memory layout for leaf nodes: B+tree's degree <= 0! Please, "
                "increase the page size or reduce the max key value size."
            )

        return degree

    def _create_node(self, is_leaf: bool) -> BPTNode[KT, VT]:
        """
        Allocates a new free disk page and instantiates a new node instance. The new node contains reference to
        its new disk page.
        """
        new_page_number = self.memory.allocate_page()
        new_empty_node: BPTNode[KT, VT] = BPTNode(is_leaf, new_page_number, self.key_serializer, self.value_serializer)

        return new_empty_node

    def _swap_pages(self, node_1: BPTNode[KT, VT], node_2: BPTNode[KT, VT]) -> None:
        """
        Swaps disk pages between two nodes. Notice that this mutates the two node's disk_page property.
        """
        disk_page_1 = node_1.disk_page
        node_1.disk_page = node_2.disk_page
        node_2.disk_page = disk_page_1

        self._disk_write(node_1)
        self._disk_write(node_2)

    def _create_root(self) -> BPTNode[KT, VT]:
        """
        Creates a new root for the B+tree (when the B+tree's file is new).
        """
        page_number = self.memory.allocate_page()

        root = BPTNode(True, page_number, self.key_serializer, self.value_serializer)
        self._disk_write(root)

        return root

    def _read_root(self) -> BPTNode[KT, VT]:
        """
        Reads a previous root of the B+tree from it's B+tree file.
        """
        return self._disk_read(1)  # root is always stored on page 1 (page 0 for tree metadata)
