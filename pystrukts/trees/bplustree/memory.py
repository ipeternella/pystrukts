"""
Disk memory-related structures used by the B+tree.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import BinaryIO
from typing import Optional
from typing import Tuple
from typing import Union
from uuid import uuid4

from pystrukts._types.basic import Endianness
from pystrukts._types.basic import StrPath
from pystrukts.trees.bplustree.settings import MAX_KEY_SIZE_BYTE_SPACE
from pystrukts.trees.bplustree.settings import MAX_VALUE_SIZE_BYTE_SPACE
from pystrukts.trees.bplustree.settings import PAGE_SIZE_BYTE_SPACE


class PagedFileMemory:
    """
    Represents a file that is used as the memory storage for the B+tree. It's used
    to manipulate (read, write) pages to disk.
    """

    # tree file
    tree_file: BinaryIO
    tree_file_path: StrPath
    is_new_file: bool

    # page metadata (tree settings)
    page_size: int
    max_key_size: int
    max_value_size: int
    last_used_page: int = -1  # first metadata writing increments to 0
    endianness: Endianness

    def __init__(
        self,
        page_size: int = 4096,
        max_key_size: int = 8,
        max_value_size: int = 32,
        endianness: Endianness = "big",
        tree_file: Optional[StrPath] = None,
    ) -> None:
        self.tree_file, self.is_new_file = self._open_tree_file(tree_file)
        self.tree_file_path = self.tree_file.name
        self.endianness = endianness

        if self.is_new_file:
            self.page_size = page_size
            self.max_key_size = max_key_size
            self.max_value_size = max_value_size
            self._write_page_metadata_to_disk()
        else:
            self._read_page_metadata_from_disk()

    def allocate_page(self) -> int:
        """
        Allocates a new page on disk and returns the page number reference.
        """
        empty_page = bytes(self.page_size)
        self.last_used_page += 1
        self.write_page(self.last_used_page, empty_page)

        return self.last_used_page

    def read_page(self, page_number: int, page_size: Optional[int] = None) -> bytearray:
        """
        Reads a disk page from the tree file.
        """
        page_size = page_size if page_size is not None else self.page_size

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

    def write_page(self, page: int, data: Union[bytes, bytearray], page_size: Optional[int] = None) -> None:
        """
        Writes a full disk block to the tree file.
        """
        page_size = page_size if page_size is not None else self.page_size
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

    def _write_page_metadata_to_disk(self):
        """
        Creates a byte array of the tree memory disk paging metadada (settings) to be persisted on disk.
        The memory layout of the byte array is as follows:

        page_size, max_key_size, max_value_size, padding
        4 bytes, 4 bytes, 4 bytes, 4 bytes, (page_size - 4 * 3) bytes
        """
        metadata_page_number = self.allocate_page()  # increments self.last_used_page to 0
        page_data = bytes()

        page_data += self.page_size.to_bytes(PAGE_SIZE_BYTE_SPACE, self.endianness)
        page_data += self.max_key_size.to_bytes(MAX_KEY_SIZE_BYTE_SPACE, self.endianness)
        page_data += self.max_value_size.to_bytes(MAX_VALUE_SIZE_BYTE_SPACE, self.endianness)
        page_data += bytes(self.page_size - len(page_data))  # padding

        self.write_page(metadata_page_number, page_data)

    def _read_page_metadata_from_disk(self):
        """
        Reads a tree memory layout settings from a disk byte array.
        """
        # reads incomplete page in order to fetch page size first
        incomplete_first_page = self.read_page(0, PAGE_SIZE_BYTE_SPACE)
        self.page_size = int.from_bytes(incomplete_first_page, self.endianness)

        # after having page size, reads the complete settings page
        full_page = self.read_page(0)

        # reads the incremental memory layout
        start = PAGE_SIZE_BYTE_SPACE
        end = start + MAX_KEY_SIZE_BYTE_SPACE
        self.max_key_size = int.from_bytes(full_page[start:end], self.endianness)

        start = end
        end += MAX_VALUE_SIZE_BYTE_SPACE
        self.max_value_size = int.from_bytes(full_page[start:end], self.endianness)

        self.last_used_page = int(os.path.getsize(self.tree_file_path) / self.page_size) - 1  # pages are zero-indexed
