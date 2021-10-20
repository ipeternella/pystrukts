"""
Module with settings for the B+tree structure.

Metadata page memory layout:

+------------------------- disk page size -------------------------+
| page_size_space |  key_size_space |  value_size_space |  unused  |
|     4 byte      |     4 bytes     |    4 bytes        |    ...   |
+------------------------------------------------------------------+

Inner nodes memory layout:

+------------------------------- disk page size ------------------------------- ... -+
| node_type |  records_count | first_node_pointer | node_pointer |    key    |  ...  |
|   1 byte  |     4 bytes    |       4 bytes      |   4 bytes    |  K bytes  |  ...  |
+-------------------------------------------------------------------------------...--+
 ^~~~~~~~~~~~~~~~~~ page headers ~~~~~~~~~~~~~~~~^ ^~~~ each inner record ~~~~^

where K = user-defined max key size (which must fit the page size)

Leaf nodes have a different memory layout, so the max. amount of children (2*degree - 1)
it can sustain is different than inner nodes (that only stores keys and node pointers):

+-------------------------------- disk page size ---------------------------- ... -+
| node_type |  records_count |  next_leaf_pointer |    key    |   value    |  ...  |
|   1 byte  |     4 bytes    |       4 bytes      |  K bytes  |   V bytes  |  ...  |
+-----------------------------------------------------------------------------...--+
^~~~~~~~~~~~~~~~~~~ page headers ~~~~~~~~~~~~~~~~^ ^~~ each leaf record ~~~^

where K = user-defined max key size, V = user-defined max value size
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

# inner nodes
INNER_NODE_HEADERS_SPACE = NODE_TYPE_BYTE_SPACE + RECORDS_COUNT_BYTE_SPACE

# leaf nodes
LEAF_NODES_HEADERS_SPACE = NODE_TYPE_BYTE_SPACE + RECORDS_COUNT_BYTE_SPACE + NODE_POINTER_BYTE_SPACE
