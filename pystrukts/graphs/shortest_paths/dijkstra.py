"""
Module with Dijkstra's algorithm for finding shortest-paths on directed and
non-negatively weighted graphs.
"""
from pystrukts.graphs.common import Graph
from pystrukts.graphs.common import Vertex
from pystrukts.queues.min_priority_queue import MinPriorityQueue


def dijkstra(graph: Graph, source: Vertex) -> None:
    """
    Dijkstra's algorithm for finding shortest paths. Notice that the graph
    cannot have any negative weights (unlike Bellman-Ford algorithm).
    """
    if source.key not in graph.vertices:
        raise ValueError(f"Source vertex: {source} not found in the graph!")

    min_queue: MinPriorityQueue[Vertex] = MinPriorityQueue()

    graph.reset()
    source.distance = 0  # all vertices being with INF distance, except the source

    for vertex in graph.vertices.values():
        min_queue.enqueue(vertex.distance, vertex)

    while min_queue.is_empty() is False:
        min_distance_vertex: Vertex = min_queue.dequeue()  # type: ignore

        for dest_vertex in min_distance_vertex.adjacent:
            edge = graph.get_edge(min_distance_vertex, dest_vertex)
            graph.relax(min_distance_vertex, dest_vertex, edge.weight)  # type: ignore
