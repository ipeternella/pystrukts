"""
Utility functions used for testing trees.
"""
import os
from contextlib import contextmanager
from typing import Optional
from uuid import uuid4


@contextmanager
def tmp_btree_file(tmp_file_name: Optional[str] = None):
    """
    Temporarily creates a test index name which is deleted at the end of the context manager.
    """
    tmp_file_name = tmp_file_name if tmp_file_name is not None else f"tmp-btree-{uuid4().hex}.db"

    try:
        # return control back to the test
        yield tmp_file_name
    finally:
        # final cleaning if needed
        if os.path.exists(tmp_file_name):
            os.remove(tmp_file_name)
