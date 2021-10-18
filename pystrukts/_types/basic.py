"""
Module with basic type definitions.
"""

import os
from typing import Literal
from typing import TypeVar
from typing import Union

StrPath = Union[str, bytes, os.PathLike]
Endianness = Literal["little", "big"]

T = TypeVar("T")  # pylint: disable=invalid-name
KT = TypeVar("KT")  # pylint: disable=invalid-name
VT = TypeVar("VT")  # pylint: disable=invalid-name
