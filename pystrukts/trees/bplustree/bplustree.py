"""
Module with a B+tree implementation.
"""
from __future__ import annotations

from typing import Generic
from typing import Optional

from pystrukts._types.basic import KT
from pystrukts._types.basic import VT
from pystrukts._types.basic import Endianness
from pystrukts._types.basic import StrPath
from pystrukts.trees.bplustree.memory import PagedFileMemory
from pystrukts.trees.bplustree.node import BPTNode
from pystrukts.trees.bplustree.serializers import DefaultSerializer
from pystrukts.trees.bplustree.serializers import Serializer
from pystrukts.trees.bplustree.settings import NODE_POINTER_BYTE_SPACE
from pystrukts.trees.bplustree.settings import NODE_TYPE_BYTE_SPACE
from pystrukts.trees.bplustree.settings import RECORDS_COUNT_BYTE_SPACE


class BPlusTree(Generic[KT, VT]):
    """
    Class that represents a B+tree.
    """

    memory: PagedFileMemory
    degree: int
    root: BPTNode[KT, VT]
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
        self.degree = self._compute_degree()

        if self.memory.is_new_file:
            self.root = self._create_root()
        else:
            self.root = self._read_root()

    def _compute_degree(self) -> int:
        page_headers_size = NODE_TYPE_BYTE_SPACE + RECORDS_COUNT_BYTE_SPACE
        each_record_size = NODE_POINTER_BYTE_SPACE + self.memory.max_key_size
        free_page_size = self.memory.page_size - page_headers_size

        # 2*t - 1 == "max keys in node on a single page" -> 2*t - 1 == free_page_size / each_record_size and solve for t
        degree = int((free_page_size / each_record_size + 1) / 2)  # max amount of keys in inner nodes

        if degree <= 0:
            raise ValueError(
                "Impossible disk page memory layout: B+tree's degree <= 0! Please, "
                "increase the page size or reduce the max key value size."
            )

        return degree

    def _create_root(self) -> BPTNode:
        root = BPTNode(True, self.key_serializer, self.value_serializer)

        page_number = self.memory.allocate_page()
        root_data = root.to_page(
            self.memory.page_size, self.memory.max_key_size, self.memory.max_value_size, self.endianness
        )
        self.memory.write_page(page_number, root_data)

        return root

    def _read_root(self) -> BPTNode:
        page_data = self.memory.read_page(1)  # page 0 is for tree metadata

        loaded_root: BPTNode[KT, VT] = BPTNode(True, self.key_serializer, self.value_serializer)
        loaded_root.load_from_page(page_data, self.memory.max_key_size, self.memory.max_value_size, self.endianness)

        return loaded_root
