"""
Module with undirected graph implementations.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple

from pystrukts._types.basic import T


class Vertex(Generic[T]):
    key: T
    adjacent: List[Vertex[T]] = list()

    def __init__(self, key: T) -> None:
        self.key = key
        self.adjacent = list()


@dataclass
class Edge(Generic[T]):
    source: Vertex[T]
    destination: Vertex[T]
    weight: int


class Graph(Generic[T]):
    """
    Represents an undirected graph implemented with adjacency lists style but
    slightly modified to use adjacency sets (hash sets) to improve look up operations.
    """

    vertices: Dict[T, Vertex[T]]
    edges: Dict[Tuple[Vertex[T], Vertex[T]], Edge[T]]

    def __init__(self) -> None:
        self.vertices = dict()
        self.edges = dict()

    @property
    def total_vertices(self) -> int:
        return len(self.vertices)

    @property
    def total_edges(self) -> int:
        return len(self.edges)

    def get_vertex(self, key: T) -> Optional[Vertex[T]]:
        return self.vertices.get(key)

    def get_edge(self, vertex_1: Vertex[T], vertex_2: Vertex[T]) -> Optional[Edge[T]]:
        edge = self.edges.get((vertex_1, vertex_2))

        if edge is None:
            edge = self.edges.get((vertex_2, vertex_1))

        return edge

    def add_vertex(self, vertex: Vertex[T]) -> None:
        self.vertices[vertex.key] = vertex

    def add_edge(self, source: Vertex[T], destination: Vertex[T], weight: int = 1) -> None:
        if source.key not in self.vertices:
            raise ValueError("Vertex 1 was not found in the graph!")

        if destination.key not in self.vertices:
            raise ValueError("Vertex 2 was not found in the graph!")

        if (source, destination) in self.edges or (destination, source) in self.edges:
            raise ValueError("Edge already exists in the graph!")

        self.edges[(source, destination)] = Edge(source, destination, weight)
        self.vertices[source.key].adjacent.append(destination)
        self.vertices[destination.key].adjacent.append(source)
