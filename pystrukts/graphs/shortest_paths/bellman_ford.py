"""
Module with the Bellman-Ford algorithm for the single-source shortest-path problem.
"""
from pystrukts.graphs.common import Graph
from pystrukts.graphs.common import Vertex


def bellman_ford(graph: Graph, source: Vertex) -> bool:
    """
    Bellman-Ford algorithm for finding the shortest-path on a weighted and directed graph.
    Returns True if there are NO negative-weight cycles on the graph. Otherwise, returns False.
    """
    if source.key not in graph.vertices:
        raise ValueError(f"Source vertex: {source} not found in the graph!")

    graph.reset()
    source.distance = 0

    for edge in graph.edges.values():
        graph.relax(edge.source, edge.destination, edge.weight)  # type: ignore

    for edge in graph.edges.values():
        if edge.destination.distance > edge.source.distance + edge.weight:  # type: ignore
            return False

    return True
