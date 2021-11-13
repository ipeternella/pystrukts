"""
Module with graph implementations.
"""
from __future__ import annotations
from __future__ import with_statement

import sys
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple

from pystrukts._types.basic import T
from pystrukts.queues import Queue

INF = sys.maxsize


class VertexColor(Enum):
    """
    Represents each color possibility that vertex node can have. This is used
    by BFS and DFS algorithms.
    """

    WHITE = 1  # not visited
    GRAY = 2  # visited but adjacent vertices not enqueued for analysis
    BLACK = 3  # visited and adjacent vertices have been enqueued for analysis: finished!


class Vertex(Generic[T]):
    """
    Represents a vertex in a graph.
    """

    key: T
    adjacent: List[Vertex[T]] = list()

    # properties for BFS and DFS
    color: VertexColor
    parent: Optional[Vertex[T]]

    distance: int  # distance for BFS
    start: float  # find time (epoch) for DFS
    end: float  # end time (epoch) for DFS

    def __init__(self, key: T) -> None:
        self.key = key
        self.adjacent = list()

        # bfs and dfs
        self.color = VertexColor.WHITE
        self.parent = None

        # bfs
        self.distance = INF

        # dfs
        self.start = 0.0
        self.end = 0.0

    def __repr__(self) -> str:
        return f"<Vertex: {self.key}, color: {self.color}>"


@dataclass
class Edge(Generic[T]):
    """
    Represents an edge (connection) between two vertices in a graph.
    """

    source: Vertex[T]
    destination: Vertex[T]
    weight: Optional[int]


class Graph(Generic[T]):
    """
    Represents a graph implemented with adjacency lists. The edges are represented using
    a specific Edge class and stored on a hashmap composed of tuples of vertices pairs.
    """

    vertices: Dict[T, Vertex[T]]
    edges: Dict[Tuple[Vertex[T], Vertex[T]], Edge[T]]
    directed: bool
    weighted: bool

    def __init__(self, directed: bool = False, weighted: bool = False) -> None:
        self.vertices = dict()
        self.edges = dict()
        self.directed = directed
        self.weighted = weighted

    @property
    def total_vertices(self) -> int:
        """
        Returns the amount of vertices in the graph.
        """
        return len(self.vertices)

    @property
    def total_edges(self) -> int:
        """
        Returns the amount of edges in the graph.
        """
        return len(self.edges)

    def get_vertex(self, key: T) -> Optional[Vertex[T]]:
        """
        Returns a vertex of the graph if it was found. Otherwise, returns None.
        """
        return self.vertices.get(key)

    def get_edge(self, source: Vertex[T], dest: Vertex[T]) -> Optional[Edge[T]]:
        """
        Returns an edge of the graph based on the two given vertices. If the edge is not found,
        returns None.
        """
        edge = self.edges.get((source, dest))

        # in directed graphs the order source -> dest matter so we either find it here or not
        if self.directed:
            return edge

        # for non-directed graphs the order source -> dest does NOT matter so we also try to reverse vertices
        if edge is None:
            edge = self.edges.get((dest, source))

        return edge

    def add_vertex(self, key: T) -> Vertex[T]:
        """
        Adds a new vertex to the graph with the given key. The node is disconnected from any other
        vertices of the graph. To add connections between vertices, use the add_edge method. Returns the
        created vertex.
        """
        self.vertices[key] = Vertex(key)

        return self.vertices[key]

    def add_edge(self, source: Vertex[T], destination: Vertex[T], weight: Optional[int] = None) -> None:
        """
        Adds an edge (connection) between two vertices of the graph. If the vertices are not found, it raises a
        ValueError. The edges can optionally be weighted. If the edge is already present in the graph, it also
        raises a ValueError.
        """
        if self.weighted and weight is None:
            raise ValueError("Weighted graph needs a weight for each edge added to the graph!")

        if source.key not in self.vertices:
            raise ValueError(f"Source vertex with key {source.key} was not found in the graph!")

        if destination.key not in self.vertices:
            raise ValueError(f"Destination vertex with {destination.key} was not found in the graph!")

        if (source, destination) in self.edges:
            raise ValueError("Edge already exists in the graph!")

        # non-directed graphs can only have one edge between two vertices
        # directed graphs can have two edges depending on the source
        if not self.directed and (destination, source) in self.edges:
            raise ValueError("Edge already exists in the graph!")

        weight = weight if self.weighted else None
        self.edges[(source, destination)] = Edge(source, destination, weight)
        self.vertices[source.key].adjacent.append(destination)
        self.vertices[destination.key].adjacent.append(source)

    def relax(self, source: Vertex[T], dest: Vertex[T], weight: int) -> None:
        """
        "Relaxes" the constraint given by dest.distance <= source.distance + weight.
        """
        if dest.distance > source.distance + weight:
            dest.distance = source.distance + weight
            dest.parent = source

    def reset(self) -> None:
        """
        Resets all the graph's vertices to its default properties such as their colors, distances and other BFS
        and DFS properties.
        """
        for _, vertex in self.vertices.items():
            self._reset_vertex(vertex)

    def _reset_vertex(self, vertex: Vertex[T]) -> None:
        vertex.color = VertexColor.WHITE
        vertex.parent = None
        vertex.distance = INF
        vertex.start = 0.0
        vertex.end = 0.0

    def bfs(self, source: Vertex[T]) -> None:
        """
        Breadth-first (BFS) algorithm for traversing/exploring the graph from a given source vertex. If such source
        is not found, it raises ValueError. Vertices that are not on any path starting from the source vertex are not
        traversed (unlike in DFS which may uses several source vertices).
        """
        if source.key not in self.vertices:
            raise ValueError(f"Vertice with key {source.key} was not found in the graph!")

        self.reset()  # reset graph's vertices back to their original state

        source.color = VertexColor.GRAY
        source.distance = 0
        source.parent = None

        queue: Queue[T, Vertex[T]] = Queue()
        queue.enqueue(source.key, source)

        while queue.is_empty() is False:
            current_vertex: Vertex[T] = queue.dequeue()  # type: ignore
            adjacent_vertices = current_vertex.adjacent

            for next_vertex in adjacent_vertices:

                if next_vertex.color == VertexColor.WHITE:
                    next_vertex.color = VertexColor.GRAY
                    next_vertex.parent = current_vertex
                    next_vertex.distance = current_vertex.distance + 1  # breadth first
                    queue.enqueue(next_vertex.key, next_vertex)

            current_vertex.color = VertexColor.BLACK

    def dfs(self) -> None:
        """
        Depth-first (DFS) algorithm for traversing the graph. Unlike BFS whose source vertex is fixed, DFS will
        traverse all vertices so many sources can possibly be used in a way that even disconnected vertices (or
        disconnected parts of the graph) will be traversed.
        """
        self.reset()  # reset graph's vertices back to their original state

        # traverses all vertices in the graph
        for _, vertex in self.vertices.items():
            if vertex.color == VertexColor.WHITE:
                self._dfs(vertex)

    def _dfs(self, current: Vertex[T]) -> None:
        """
        Helper procedure for the recursive DFS algorithm.
        """
        current.start = time.time()
        current.color = VertexColor.GRAY

        for vertex in current.adjacent:
            if vertex.color == VertexColor.WHITE:
                vertex.parent = current
                self._dfs(vertex)

        current.color = VertexColor.BLACK
        current.end = time.time()
