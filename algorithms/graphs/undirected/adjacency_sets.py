"""
Module with Graph implementations using adjacent sets (faster than adjacency lists) along with hashmaps
(symbol tables) in order to allow graph vertices to have diff types than traditional integer values.
"""
from __future__ import annotations

from typing import Dict
from typing import Generic
from typing import Set
from typing import TypeVar

from algorithms.graphs.exceptions import VertexNotFoundError

T = TypeVar("T")


class Graph(Generic[T]):
    """
    A Graph implementation using adjacent sets and hashmaps (symbol tables). An adjacency set is used
    to prevent repeated edges between vertices (parallel edges -- anomally).
    """

    _vertices_count: int  # total amount of vertices (nodes)
    _edges_count: int  # total amount of edges
    _vertices: Dict[T, Set[T]]  # vertex-to-adjacent-vertices mapping

    def __init__(self) -> None:
        self._vertices_count = 0
        self._edges_count = 0
        self._vertices = {}  # symbol table / hashmap

    @property
    def vertices(self) -> int:
        return self._vertices_count

    @property
    def edges(self) -> int:
        return self._edges_count

    def has_vertex(self, vertex: T) -> bool:
        """
        Returns True if a given vertex is in the graph (vertex is in the inner hashmap of vertices).
        Otherwise, returns False.
        """
        return vertex in self._vertices

    def get_vertex(self, vertex: T) -> T:
        """
        Returns a vertex from the graph if it exists. If it does not, then VertexNotFoundError is raised.
        """
        if self.has_vertex(vertex):
            return vertex

        raise VertexNotFoundError()

    def get_adjacent_vertices(self, vertex: T) -> Set[T]:
        """
        Retrives a set of the adjacent vertices of a given vertex. Raises VertexNotFoundError
        if the vertex cannot be found in the graph.
        """
        if not self.has_vertex(vertex):
            raise VertexNotFoundError(vertex)

        return self._vertices[vertex]

    def add_vertex(self, new_vertex: T) -> None:
        """
        Adds a new vertex to the graph if it does not already exists. If it already exists, then
        nothing is done.
        """
        if not self.has_vertex(new_vertex):
            self._vertices_count += 1
            self._create_adjacent_set(new_vertex)

    def has_edge(self, vertex_1: T, vertex_2: T) -> bool:
        """
        Returns True if there's an edge between the two vertices. If the vertices do not exist, naturally
        this method returns False as there can be no edge without one of the vertices.
        """
        if not self.has_vertex(vertex_1) or not self.has_vertex(vertex_2):
            return False

        return vertex_1 in self.get_adjacent_vertices(vertex_2)

    def add_edge(self, vertex_1: T, vertex_2: T) -> None:
        """
        Adds a new connection (edge) between two vertices in the graph. If the vertices do not exist,
        then they are created and then connected. If they exist, just the edge connection is made.
        """
        if self.has_edge(vertex_1, vertex_2):
            return  # edge already exists, return (no edge anomalies are allowed with adjacency sets)

        if not self.has_vertex(vertex_1):
            self.add_vertex(vertex_1)

        if not self.has_vertex(vertex_2):
            self.add_vertex(vertex_2)

        # vertices and adjacent vertices are expected to exist from here on
        adj_set_1 = self.get_adjacent_vertices(vertex_1)
        adj_set_2 = self.get_adjacent_vertices(vertex_2)

        # adds the new edge between the two vertices
        self._edges_count += 1
        adj_set_1.add(vertex_2)
        adj_set_2.add(vertex_1)

    def _create_adjacent_set(self, vertex: T) -> Set[T]:
        """
        Adds a new vertex and an empty adjacency set to the vertex-to-adjacent-vertices hashmap.
        """
        new_adj_set: Set[T] = set()
        self._vertices[vertex] = new_adj_set

        return new_adj_set
