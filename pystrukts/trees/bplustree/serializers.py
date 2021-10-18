"""
Serializers of the B+tree used to perform disk operations.
"""
import pickle
from typing import Protocol
from typing import Union

from pystrukts._types.basic import T


class Serializer(Protocol[T]):
    """
    Default serialization protocol used by the B+tree.
    """

    def to_bytes(self, object: T) -> bytes:
        """Serializes an object into a byte array."""

    def from_bytes(self, bytes: Union[bytes, bytearray]) -> T:
        """Deserializes a byte array back into a Python object."""


class DefaultSerializer(Serializer[T]):
    """
    Default serializer based on stdlib's Pickle to be used in case a customized
    one is not supplied.
    """

    def to_bytes(self, object) -> bytes:
        return pickle.dumps(object)

    def from_bytes(self, bytes: Union[bytes, bytearray]) -> T:
        return pickle.loads(bytes)
