"""
Module with DFS algorithm implementation.
"""
from __future__ import annotations

from typing import Generic
from typing import Set
from typing import TypeVar

from algorithms.graphs.exceptions import VertexNotFoundError
from algorithms.graphs.undirected.adjacency_sets import Graph

T = TypeVar("T")


class DepthFirstSearch(Generic[T]):
    """
    Recursive implementation of a DFS algorithm that works on a graph G given a source vertex S to start
    the searching algorithm. If the source vertex does not exist in the graph, VertexNotFoundError is
    raised. A class is required in order to sustain DFS results to be queried by the user such as visited,
    count, etc.
    """

    _visited_vertices: Set[T]  # set of marked vertices (if not inside: not marked)

    def __init__(self, graph: Graph[T], source_vertex: T) -> None:
        # self._visited_vertices = [False] * graph.vertices
        self._visited_vertices = set()

        if not graph.has_vertex(source_vertex):
            raise VertexNotFoundError()

        # source vertex exists, recursively traverse adj sets from the graph
        self._depth_first_search(graph, source_vertex)

    def _depth_first_search(self, graph: Graph[T], vertex: T) -> None:
        # base case: already visited this node
        if vertex in self._visited_vertices:
            return

        # first time seeing this node! Mark it as visited now!
        self._visited_vertices.add(vertex)
        adjacent_vertices = graph.get_adjacent_vertices(vertex)

        # reduced problem: recursion
        for adjacent_vertex in adjacent_vertices:
            self._depth_first_search(graph, adjacent_vertex)

    def visited(self, vertex: T) -> bool:
        """
        Checks if the vertex is within the Graph by using a depth first approach.

        Notice that the hashmap used by the graph.has_vertex() method is more efficient, but
        this is a different approach.
        """
        return vertex in self._visited_vertices

    def count(self) -> int:
        """
        Returns the amount of vertices within the graph.
        """
        return len(self._visited_vertices)
