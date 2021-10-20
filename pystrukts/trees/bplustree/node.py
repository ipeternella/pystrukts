"""
Module with a B+tree implementation.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Generic
from typing import List
from typing import Optional
from typing import Union

from pystrukts._types.basic import KT
from pystrukts._types.basic import VT
from pystrukts._types.basic import Endianness
from pystrukts.trees.bplustree.serializers import DefaultSerializer
from pystrukts.trees.bplustree.serializers import Serializer
from pystrukts.trees.bplustree.settings import NODE_POINTER_BYTE_SPACE
from pystrukts.trees.bplustree.settings import NODE_TYPE_BYTE_SPACE
from pystrukts.trees.bplustree.settings import RECORDS_COUNT_BYTE_SPACE

StrPath = Union[str, bytes, os.PathLike]


@dataclass
class InnerRecord(Generic[KT, VT]):
    key: KT
    next_node_page: int
    next_node: Optional[BPTNode[KT, VT]]  # if None, use the next page number to read from disk


@dataclass
class LeafRecord(Generic[KT, VT]):
    key: KT
    value: VT


class BPTNode(Generic[KT, VT]):
    """
    Represents a node (leaf or inner) of a B+tree which carries leaf or inned node records.
    """

    # node metadata
    disk_page: int
    is_leaf: bool

    # serializers
    key_serializer: Serializer[KT]
    value_serializer: Serializer[VT]

    # inner node properties
    inner_records: List[InnerRecord[KT, VT]]
    first_node_page: int
    first_node: Optional[BPTNode[KT, VT]]

    # leaf node properties
    leaf_records: List[LeafRecord[KT, VT]]
    next_leaf_page: int
    next_leaf: Optional[BPTNode[KT, VT]]

    def __init__(
        self,
        is_leaf: bool = True,
        disk_page: int = 0,
        key_serializer: Serializer[KT] = DefaultSerializer(),
        value_serializer: Serializer[VT] = DefaultSerializer(),
    ) -> None:
        # node metadata
        self.disk_page = disk_page
        self.is_leaf = is_leaf

        # serializers
        self.key_serializer = key_serializer
        self.value_serializer = value_serializer

        # inner nodes
        self.inner_records = list()
        self.first_node = None
        self.first_node_page = 0

        # leaf nodes
        self.leaf_records = list()
        self.next_leaf_page = 0
        self.next_leaf = None

    @property
    def records_count(self) -> int:
        if self.is_leaf:
            return len(self.leaf_records)

        return len(self.inner_records)

    def to_page(self, page_size: int, max_key_size: int, max_value_size: int, endianness: Endianness) -> bytes:
        """
        Creates a byte array of the node following given memory layout.
        """
        page_data = bytes()

        # page headers
        page_data += self.is_leaf.to_bytes(NODE_TYPE_BYTE_SPACE, endianness)
        page_data += self.records_count.to_bytes(RECORDS_COUNT_BYTE_SPACE, endianness)

        if self.is_leaf:
            page_data += self._serialize_leaf_node(max_key_size, max_value_size, endianness)
        else:
            page_data += self._serialize_inner_node(max_key_size, endianness)

        page_data += bytes(page_size - len(page_data))  # final padding to fit a disk page

        return page_data

    def load_from_page(
        self,
        data: bytes,
        max_key_size: int,
        max_value_size: int,
        endianess: Endianness,
    ) -> None:
        start = 0
        end = start + NODE_TYPE_BYTE_SPACE
        self.is_leaf = bool(bool.from_bytes(data[start:end], endianess))

        start = end
        end += RECORDS_COUNT_BYTE_SPACE
        records_count = int.from_bytes(data[start:end], endianess)

        if self.is_leaf:
            start = end
            end += NODE_POINTER_BYTE_SPACE
            self.next_leaf_page = int.from_bytes(data[start:end], endianess)

            for _ in range(0, records_count):
                start = end
                end += max_key_size
                key = self.key_serializer.from_bytes(data[start:end])

                start = end
                end += max_value_size
                value = self.value_serializer.from_bytes(data[start:end])

                self.leaf_records.append(LeafRecord(key, value))
        else:
            start = end
            end += NODE_POINTER_BYTE_SPACE
            self.first_node_page = int.from_bytes(data[start:end], endianess)

            for _ in range(0, records_count):
                start = end
                end += NODE_POINTER_BYTE_SPACE
                next_node_page = int.from_bytes(data[start:end], endianess)

                start = end
                end += max_key_size
                key = self.key_serializer.from_bytes(data[start:end])

                self.inner_records.append(InnerRecord(key, next_node_page, None))

    def _serialize_leaf_node(self, max_key_size: int, max_value_size: int, endianness: Endianness) -> bytes:
        leaf_data = bytes()
        leaf_data += self.next_leaf_page.to_bytes(NODE_POINTER_BYTE_SPACE, endianness)

        # leaf_records must be in sorted order
        for record in self.leaf_records:
            key_data = self.key_serializer.to_bytes(record.key)
            value_data = self.value_serializer.to_bytes(record.value)

            if len(key_data) > max_key_size:
                raise ValueError(f"key: {record.key} size exceeds max key size: {max_key_size}")

            if len(value_data) > max_value_size:
                raise ValueError(f"value: {record.value} size exceeds max value size: {max_value_size}")

            leaf_data += key_data
            leaf_data += bytes(max_key_size - len(key_data))  # padding

            leaf_data += value_data
            leaf_data += bytes(max_value_size - len(value_data))  # padding

        return leaf_data

    def _serialize_inner_node(self, max_key_size: int, endianness: Endianness) -> bytes:
        inner_data = bytes()
        inner_data += self.next_leaf_page.to_bytes(NODE_POINTER_BYTE_SPACE, endianness)

        # page payload
        for inner_record in self.inner_records:
            inner_data += inner_record.next_node_page.to_bytes(NODE_POINTER_BYTE_SPACE, endianness)
            key_data = self.key_serializer.to_bytes(inner_record.key)

            if len(key_data) > max_key_size:
                raise ValueError(f"key: {inner_record.key} size exceeds max key size: {max_key_size}")

            inner_data += key_data
            inner_data += bytes(max_key_size - len(key_data))  # padding

        return inner_data
