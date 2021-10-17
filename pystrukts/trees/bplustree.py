"""
Module with a B+tree implementation.
"""
from __future__ import annotations

import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO
from typing import Generic
from typing import Literal
from typing import Optional
from typing import Protocol
from typing import Tuple
from typing import Union
from uuid import uuid4

from pystrukts._types.basic import KT
from pystrukts._types.basic import VT
from pystrukts._types.basic import T

StrPath = Union[str, bytes, os.PathLike]


class Serializer(Protocol[T]):
    """
    Default serialization protocol used by the B+tree.
    """

    def to_bytes(self, object: T) -> bytes:
        """Serializes an object into a byte array."""

    def from_bytes(self, bytes: bytes | bytearray) -> T:
        """Deserializes a byte array back into a Python object."""


class DefaultSerializer(Serializer[T]):
    """
    Default serializer based on stdlib's Pickle to be used in case a customized
    one is not supplied.
    """

    def to_bytes(self, object) -> bytes:
        return pickle.dumps(object)

    def from_bytes(self, bytes: bytes | bytearray) -> T:
        return pickle.loads(bytes)


@dataclass
class PageMemoryLayout:
    page_size: int
    endianness: Literal["little", "big"]
    max_key_size: int
    max_value_size: int

    # last used page
    last_page: int = -1

    # page headers byte sizes
    node_type_header_space: int = 1
    records_count_header_space: int = 4  # int32

    # page payload byte sizes
    node_pointer_space: int = 4  # inner-nodes only
    sibling_pointer_space: int = 4  # leaf-nodes only

    def to_page(self) -> bytes:
        """
        Creates a byte array of the tree memory layout settings to be persisted on disk. The memory
        layout of the byte array is as follows:

        page_size, max_key_size, max_value_size, last_page, padding
        4 bytes, 4 bytes, 4 bytes, 4 bytes, (page_size - 4 * 4) bytes
        """
        page_data = bytes()

        page_data += self.page_size.to_bytes(4, self.endianness)
        page_data += self.max_key_size.to_bytes(4, self.endianness)
        page_data += self.max_value_size.to_bytes(4, self.endianness)
        page_data += self.last_page.to_bytes(4, self.endianness)
        page_data += bytes(self.page_size - len(page_data))  # padding

        return page_data

    @classmethod
    def from_page(cls, data: bytes, endianess: Literal["little", "big"] = "big") -> PageMemoryLayout:
        """
        Reads a tree memory layout settings from a disk byte array.
        """
        page_size = int.from_bytes(data[0:4], endianess)
        max_key_size = int.from_bytes(data[4:8], endianess)
        max_value_size = int.from_bytes(data[8:12], endianess)
        last_page = int.from_bytes(data[12:16], endianess)

        return PageMemoryLayout(page_size, endianess, max_value_size, max_key_size, last_page)


class PagedFileMemory:
    """
    Represents a file that is used as the memory storage for the B+tree. It's used
    to manipulate (read, write) pages to disk.
    """

    tree_file: BinaryIO
    memory_layout: PageMemoryLayout

    def __init__(
        self,
        page_size: int,
        endianness: Literal["little", "big"],
        max_key_size: int = 0,
        max_value_size: int = 0,
        tree_file: Optional[StrPath] = None,
    ) -> None:
        self.tree_file, is_new_tree = self._open_tree_file(tree_file)

        if is_new_tree:
            self.memory_layout = PageMemoryLayout(page_size, endianness, max_key_size, max_value_size)

            page_number = self.allocate_node()
            page_data = self.memory_layout.to_page()

            self.write_page(page_number, page_data)
        else:
            # no memory layout exists so far, so explicity pass the page_size and endianness
            page_data = self.read_page(0, page_size)
            self.memory_layout = PageMemoryLayout.from_page(page_data, endianness)

    def allocate_node(self) -> int:
        """
        Allocates a new page on disk and returns the page number reference.
        """
        empty_page = bytes(self.memory_layout.page_size)
        self.memory_layout.last_page += 1
        self.write_page(self.memory_layout.last_page, empty_page)

        return self.memory_layout.last_page

    def read_page(self, page_number: int, page_size: Optional[int] = None) -> bytearray:
        """
        Reads a disk page from the tree file.
        """
        page_size = page_size if page_size is not None else self.memory_layout.page_size

        page_start = page_number * page_size
        page_end = page_start + page_size
        data = bytearray()

        # sets file's stream cursor at the beginning of the page
        page_cursor = self.tree_file.seek(page_start)

        # read() may return less bytes than expected, so we iterate until
        # the cursor position is at the end of the page
        while page_cursor != page_end:
            data += self.tree_file.read(page_end - page_cursor)  # reading moves cursor forward
            page_cursor = self.tree_file.tell()

        return data

    def write_page(self, page: int, data: bytes | bytearray, page_size: Optional[int] = None) -> None:
        """
        Writes a full disk block to the tree file.
        """
        page_size = page_size if page_size is not None else self.memory_layout.page_size
        stream_bytes = len(data)
        flushed_bytes = 0

        if stream_bytes != page_size:
            raise ValueError(
                f"Page write received stream data of {stream_bytes} bytes "
                f"which is not the current page size of {page_size} bytes!"
            )

        page_start = page * page_size

        # sets stream cursor position
        self.tree_file.seek(page_start)

        # write() may actually write less than stream_bytes, so we iterate to guarantee full write
        while flushed_bytes < stream_bytes:
            flushed_bytes += self.tree_file.write(data[flushed_bytes:])

    def _open_tree_file(self, file_path: Optional[StrPath]) -> Tuple[BinaryIO, bool]:
        """
        Opens or creates a tree file in 'b' (binary) mode to avoid any platform-specific decoding at all and
        returns a file descriptor object and whether the file was created or not.
        """
        if file_path is None:
            file_name = f"bptree-{uuid4().hex}.db"
            file_path = Path().absolute().joinpath(file_name)

        if os.path.exists(file_path):
            tree_fd = open(file_path, "r+b", buffering=0)

            return tree_fd, False

        tree_fd = open(file_path, "x+b", buffering=0)  # creates file it doesn't exist
        return tree_fd, True


class BPlusTree(Generic[KT, VT]):
    """
    Class that represents a B+tree.
    """

    degree: int
    memory: PagedFileMemory
    key_serializer: Serializer[KT]
    value_serializer: Serializer[VT]

    def __init__(
        self,
        tree_file: Optional[StrPath] = None,
        key_serializer: Optional[Serializer[KT]] = None,
        value_serializer: Optional[Serializer[VT]] = None,
        page_size: int = 4096,
        max_key_size: int = 8,
        max_value_size: int = 32,
        endianness: Literal["little", "big"] = "big",
    ) -> None:
        self.key_serializer = key_serializer if key_serializer is not None else DefaultSerializer[KT]()
        self.value_serializer = value_serializer if value_serializer is not None else DefaultSerializer[VT]()
        self.memory = PagedFileMemory(page_size, endianness, max_key_size, max_value_size, tree_file)
        self.degree = self._compute_degree()

    def _compute_degree(self) -> int:
        page_headers_size = (
            self.memory.memory_layout.node_type_header_space + self.memory.memory_layout.records_count_header_space
        )
        each_record_size = self.memory.memory_layout.node_pointer_space + self.memory.memory_layout.max_key_size
        free_page_size = self.memory.memory_layout.page_size - page_headers_size

        # 2*t - 1 == "max keys in node on a single page" -> 2*t - 1 == free_page_size / each_record_size and solve for t
        degree = int((free_page_size / each_record_size + 1) / 2)  # max amount of keys in inner nodes

        if degree <= 0:
            raise ValueError(
                "Impossible disk page memory layout: B+tree's degree <= 0! Please, "
                "increase the page size or reduce the max key value size."
            )

        return degree
