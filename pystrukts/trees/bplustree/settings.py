"""
Module with settings for the B+tree structure.
"""

# paged file memory layout: tree metadata page
PAGE_SIZE_BYTE_SPACE: int = 4
MAX_KEY_SIZE_BYTE_SPACE: int = 4
MAX_VALUE_SIZE_BYTE_SPACE: int = 4

# paged file memory layout: file page header settings
NODE_TYPE_BYTE_SPACE: int = 1
RECORDS_COUNT_BYTE_SPACE: int = 4  # int32

# paged file memory layout: file page payload settings
NODE_POINTER_BYTE_SPACE: int = 4
