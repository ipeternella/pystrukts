"""
Module with implementations of linked lists.
"""
from __future__ import annotations

from typing import Generic
from typing import Optional

from pystrukts._types.basic import KT
from pystrukts._types.basic import VT


class LinkedList(Generic[KT, VT]):
    """
    Represents a doubly linked list.
    """

    size: int
    first_node: Optional[Node[KT, VT]]
    last_node: Optional[Node[KT, VT]]

    def __init__(self) -> None:
        self.first_node = None
        self.last_node = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def append(self, key: KT, value: VT) -> None:
        """
        Inserts a new node at the end (right side) of the linked list.
        """
        new_node: Node[KT, VT] = Node(key, value)

        if len(self) == 0:
            self.first_node = new_node
            self.last_node = new_node
        else:
            new_node.previous_node = self.last_node

            self.last_node.next_node = new_node  # type: ignore[union-attr]
            self.last_node = new_node

        self.size += 1

    def prepend(self, key: KT, value: VT) -> None:
        """
        Inserts a new node at the beginning (left side) of the linked list.
        """
        new_node: Node[KT, VT] = Node(key, value)

        if len(self) == 0:
            self.first_node = new_node
            self.last_node = new_node
        else:
            new_node.next_node = self.first_node

            self.first_node.previous_node = new_node  # type: ignore[union-attr]
            self.first_node = new_node

        self.size += 1

    def get(self, key: KT) -> Optional[VT]:
        """
        Looks for a given key on the list. If a node with it is found, it returns the node's value.
        Otherwise, None is returned.
        """
        node_with_key = self._get_node(key)

        if node_with_key is None:
            return None

        return node_with_key.value

    def _get_node(self, key: KT) -> Optional[Node[KT, VT]]:
        current_node: Optional[Node[KT, VT]] = self.first_node

        # traverses list looking for the key
        while current_node is not None:
            if current_node.key == key:
                return current_node

            current_node = current_node.next_node

        return current_node

    def delete(self, key: KT) -> Optional[VT]:
        """
        Deletes a node from the linked list if the key was found on the list. If the node
        was removed, its value is returned. Otherwise, returns None.
        """
        node_for_deletion = self._get_node(key)  # handles len(self) == 0

        if node_for_deletion is None:
            return None

        removed_value = node_for_deletion.value

        # single element lists
        if len(self) == 1:
            self.first_node = None
            self.last_node = None
            del node_for_deletion
            self.size -= 1

            return removed_value

        # bigger lists (len(self) >= 2)
        if self.first_node == node_for_deletion:
            self.first_node = node_for_deletion.next_node
            self.first_node.previous_node.next_node = None  # type: ignore[union-attr]
            self.first_node.previous_node = None  # type: ignore[union-attr]

        elif self.last_node == node_for_deletion:
            self.last_node = node_for_deletion.previous_node
            self.last_node.next_node.previous_node = None  # type: ignore[union-attr]
            self.last_node.next_node = None  # type: ignore[union-attr]

        else:
            # guaranteed that the node_for_deletion will have a previous and next node
            node_for_deletion.previous_node.next_node = node_for_deletion.next_node  # type: ignore[union-attr]
            node_for_deletion.next_node.previous_node = node_for_deletion.previous_node  # type: ignore[union-attr]

        del node_for_deletion
        self.size -= 1

        return removed_value


class Node(Generic[KT, VT]):
    """
    Represents a doubly linked node.
    """

    key: KT
    value: VT
    next_node: Optional[Node[KT, VT]]
    previous_node: Optional[Node[KT, VT]]

    def __init__(self, key: KT, value: VT) -> None:
        self.key = key
        self.value = value
        self.next_node = None
        self.previous_node = None
