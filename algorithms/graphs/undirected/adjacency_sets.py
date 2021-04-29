"""
Module with Graph implementations using adjacent sets (faster than adjacency lists) along with hashmaps (symbol tables)
in order to allow graph vertices to have diff types than traditional integer values.
"""
from __future__ import annotations

from typing import Dict
from typing import Generic
from typing import Optional
from typing import Set
from typing import TypeVar

from algorithms.graphs.exceptions import VertexNotFoundError

T = TypeVar("T")


class Graph(Generic[T]):
    """
    A Graph implementation using adjacent sets and hashmaps (symbol tables). An adjacency list is used
    to prevent repeated edges between vertices (parallel edges).
    """

    _vertices_count: int  # total amount of vertices (nodes)
    _edges_count: int  # total amount of edges
    _vertices: Dict[T, Set[T]]  # adjacency set

    def __init__(self) -> None:
        self._vertices_count = 0
        self._edges_count = 0
        self._vertices = {}  # symbol table / hashmap

    def _get_adjacent_set(self, vertex: T) -> Optional[Set[T]]:
        if vertex in self._vertices:
            return self._vertices[vertex]

        return None

    def _create_adjacent_set(self, vertex: T) -> Set[T]:
        new_adj_set: Set[T] = set()
        self._vertices[vertex] = new_adj_set

        return new_adj_set

    @property
    def vertices(self) -> int:
        return self._vertices_count

    @property
    def edges(self) -> int:
        return self._edges_count

    def adjacent(self, vertex: T) -> Set[T]:
        adj_set = self._get_adjacent_set(vertex)

        if adj_set is None:
            raise VertexNotFoundError(vertex)

        return adj_set

    def add_edge(self, vertex_1: T, vertex_2: T) -> None:
        adj_set_1 = self._get_adjacent_set(vertex_1)
        adj_set_2 = self._get_adjacent_set(vertex_2)

        # create new adj set if the vertex is not in the graph already
        if adj_set_1 is None:
            self._vertices_count += 1  # new vertex in the graph
            adj_set_1 = self._create_adjacent_set(vertex_1)

        if adj_set_2 is None:
            self._vertices_count += 1
            adj_set_2 = self._create_adjacent_set(vertex_2)

        # if one vertex does not reference the other -> new edge will be added!
        if vertex_1 not in adj_set_2:
            self._edges_count += 1

        adj_set_1.add(vertex_2)
        adj_set_2.add(vertex_1)

    def __len__(self) -> int:
        return self._vertices_count
