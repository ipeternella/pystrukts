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


@dataclass(frozen=True)
class PageMemoryLayout:
    page_size: int
    max_key_size: int
    max_value_size: int
    endianness: Literal["little", "big"]

    # page headers byte sizes (in bytes)
    node_type_header_space: int = 1
    records_count_header_space: int = 4  # int32

    # page payload byte sizes
    node_pointer_space: int = 4  # inner-nodes only
    sibling_pointer_space: int = 4  # leaf-nodes only


class PagedFileMemory:
    """
    Represents a file that is used as the memory storage for the B+tree. It's used
    to manipulate (read, write) pages to disk.
    """

    last_page: int
    tree_file: BinaryIO
    memory_layout: PageMemoryLayout

    def __init__(
        self,
        page_size: int,
        max_value_size: int,
        max_key_size: int,
        endianness: Literal["little", "big"],
        tree_file: Optional[StrPath] = None,
    ) -> None:
        self.tree_file, is_new_tree = self._open_tree_file(tree_file)
        self.memory_layout = PageMemoryLayout(page_size, max_key_size, max_value_size, endianness)

        if is_new_tree:
            self.last_page = 0
            # persist tree settings on disk
        else:
            # read last page from disk's tree file
            # read settings from tree file's first page
            pass

    def read_page(self, page_number: int) -> bytes:
        """
        Reads a disk page from the tree file.
        """
        page_start = page_number * self.memory_layout.page_size
        page_end = page_start + self.memory_layout.page_size
        data = bytes()

        # sets file's stream cursor at the beginning of the page
        page_cursor = self.tree_file.seek(page_start)

        # read() may return less bytes than expected, so we iterate until
        # the cursor position is at the end of the page
        while page_cursor != page_end:
            data += self.tree_file.read(page_end - page_cursor)  # reading moves cursor forward
            page_cursor = self.tree_file.tell()

        return data

    def write_page(self, page: int, data: bytes) -> None:
        """
        Writes a full disk block to the tree file.
        """
        stream_bytes = len(data)
        flushed_bytes = 0

        if stream_bytes != self.memory_layout.page_size:
            raise ValueError(
                f"Page write received stream data of {stream_bytes} bytes "
                f"which is not the current page size of {self.memory_layout.page_size} bytes!"
            )

        page_start = page * self.memory_layout.page_size

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

    def _save_tree_settings(self) -> None:
        pass


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
        self.memory = PagedFileMemory(page_size, max_key_size, max_value_size, endianness, tree_file)
        self.degree = self._compute_tree_degree()

    def _compute_tree_degree(self) -> int:
        pass
