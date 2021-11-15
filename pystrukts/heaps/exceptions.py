"""
Exceptions raised by heaps.
"""


class EmptyHeap(Exception):
    """
    Exception raised when an impossible operation is performed on an empty heap.
    """


class ValueAlreadyExistsOnHeap(Exception):
    """
    Exception raised when a value already exists on the heap which only allows
    unique values.
    """
