"""
Serializers of the B+tree used to perform disk operations.
"""
import pickle
from typing import Protocol
from typing import Union

from pystrukts._types.basic import Endianness
from pystrukts._types.basic import T


class Serializer(Protocol[T]):
    """
    Default serialization protocol used by the B+tree.
    """

    def to_bytes(self, object: T) -> bytes:
        """Serializes an object into a byte array."""

    def from_bytes(self, some_bytes: Union[bytes, bytearray]) -> T:
        """Deserializes a byte array back into a Python object."""


class StrSerializer(Serializer[str]):
    """
    String serializer.
    """

    encoding = "utf-8"

    def to_bytes(self, string: str) -> bytes:
        return string.encode(self.encoding)

    def from_bytes(self, some_bytes: Union[bytes, bytearray]) -> str:
        return some_bytes.decode(self.encoding)


class IntSerializer(Serializer[int]):
    """
    Int serializer.
    """

    endianness: Endianness = "big"

    def to_bytes(self, some_int: int) -> bytes:
        return some_int.to_bytes(4, self.endianness)

    def from_bytes(self, some_bytes: Union[bytes, bytearray]) -> int:
        return int.from_bytes(some_bytes, self.endianness)


class DefaultSerializer(Serializer[T]):
    """
    Default serializer based on stdlib's Pickle to be used in case a customized
    one is not supplied.
    """

    def to_bytes(self, object) -> bytes:
        return pickle.dumps(object)

    def from_bytes(self, bytes: Union[bytes, bytearray]) -> T:
        return pickle.loads(bytes)
