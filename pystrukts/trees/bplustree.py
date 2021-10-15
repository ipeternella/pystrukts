"""
Module with a B+tree implementation.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import BinaryIO
from typing import Generic
from typing import Literal
from typing import Optional
from typing import Tuple
from typing import Union
from uuid import uuid4

from pystrukts._types.comparable import KT
from pystrukts._types.comparable import VT

StrPath = Union[str, bytes, os.PathLike]


class NodeType(Enum):
    """
    B+tree node type: inner or leaf.
    """

    INNER = 1
    LEAF = 2


@dataclass(frozen=True)
class BPlusTreeSettings:
    # configurable settings
    page_size: int
    min_degree: int
    max_key_size: int
    max_value_size: int
    endianness: Literal["little", "big"]

    # constant settings like byte sizes for different tree entities
    DEFAULT_PAGE_SIZE: int = 4096
    DEFAULT_MIN_DEGREE: int = 2
    DEFAULT_ENDIANNESS: Literal["little", "big"] = "big"

    KEY_BYTES_SIZE: int = 8
    VALUE_BYTES_SIZE: int = 32


class DiskStorage:
    """
    Represents a file that is used as the main memory storage for the B+tree. It's used
    to manipulate (read, write) pages to disk.
    """

    last_page: int
    tree_fd: BinaryIO
    tree_settings: BPlusTreeSettings

    def __init__(
        self,
        tree_settings: BPlusTreeSettings,
        tree_file: Optional[StrPath] = None,
    ) -> None:
        self.tree_fd, new_tree = self._open_tree_file(tree_file)

        if new_tree:
            self.last_page = 0
            self.tree_settings = tree_settings
            # persist tree settings on disk
        else:
            # read last page from disk's tree file
            # read settings from tree file's first page
            pass

    def read_page(self, page_number: int) -> bytes:
        """
        Reads a disk page from the tree file.
        """
        page_start = page_number * self.tree_settings.page_size
        page_end = page_start + self.tree_settings.page_size
        data = bytes()

        # sets file's stream cursor at the beginning of the page
        page_cursor = self.tree_fd.seek(page_start)

        # read() may return less bytes than expected, so we iterate until
        # the cursor position is at the end of the page
        while page_cursor != page_end:
            data += self.tree_fd.read(page_end - page_cursor)  # reading moves cursor forward
            page_cursor = self.tree_fd.tell()

        return data

    def write_page(self, page: int, data: bytes) -> None:
        """
        Writes a full disk block to the tree file.
        """
        stream_bytes = len(data)
        flushed_bytes = 0

        if stream_bytes != self.tree_settings.page_size:
            raise ValueError(
                f"Page write received stream data of {stream_bytes} bytes "
                f"which is not the current page size of {self.tree_settings.page_size} bytes!"
            )

        page_start = page * self.tree_settings.page_size

        # sets stream cursor position
        self.tree_fd.seek(page_start)

        # write() may actually write less than stream_bytes, so we iterate to guarantee full write
        while flushed_bytes < stream_bytes:
            flushed_bytes += self.tree_fd.write(data[flushed_bytes:])

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

    page_size: int
    settings: BPlusTreeSettings
    memory_storage: DiskStorage

    def __init__(
        self,
        tree_file: Optional[StrPath] = None,
        min_degree: int = BPlusTreeSettings.DEFAULT_MIN_DEGREE,
        page_size: int = BPlusTreeSettings.DEFAULT_PAGE_SIZE,
        key_size: int = BPlusTreeSettings.KEY_BYTES_SIZE,
        value_size: int = BPlusTreeSettings.VALUE_BYTES_SIZE,
        endianness: Literal["little", "big"] = BPlusTreeSettings.DEFAULT_ENDIANNESS,
    ) -> None:
        self.settings = BPlusTreeSettings(
            page_size=page_size,
            min_degree=min_degree,
            max_key_size=key_size,
            max_value_size=value_size,
            endianness=endianness,
        )
        self.memory_storage = DiskStorage(self.settings, tree_file)
