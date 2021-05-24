import pytest

from algorithms.graphs.undirected.adjacency_sets import Graph


@pytest.fixture
def triangular_graph_fixture() -> Graph[str]:
    r"""
    Builds a graph with three vertices and three edges with a triangular form:

      1
     / \
    2 - 3

    [1] -> [2, 3]
    [2] -> [1, 3]
    [3] -> [1, 2]
    """
    graph: Graph[str] = Graph()  # empty graph

    graph.add_edge("1", "2")
    graph.add_edge("1", "3")

    graph.add_edge("2", "1")
    graph.add_edge("2", "3")

    graph.add_edge("3", "1")
    graph.add_edge("3", "2")

    return graph


@pytest.fixture
def triangular_graph_fixture() -> Graph[str]:
    r"""
    Builds a graph with three vertices and three edges with a triangular form:

      1
     / \
    2 - 3

    [1] -> [2, 3]
    [2] -> [1, 3]
    [3] -> [1, 2]
    """
    graph: Graph[str] = Graph()  # empty graph

    graph.add_edge("1", "2")
    graph.add_edge("1", "3")

    graph.add_edge("2", "1")
    graph.add_edge("2", "3")

    graph.add_edge("3", "1")
    graph.add_edge("3", "2")

    return graph


@pytest.fixture
def key_graph_fixture() -> Graph[str]:
    r"""
    Builds a graph fixture with six vertices and seven edges in a format similar
    to a key.

      1
     / \
    2 - 3
     \ /
      4
      | \
      5 - 6

    [1] -> [2, 3]
    [2] -> [1, 3, 4]
    [3] -> [1, 2, 4]
    [4] -> [2, 3, 5, 6]
    [5] -> [4, 6]
    [6] -> [4, 5]
    """
    graph: Graph[str] = Graph()  # empty graph

    graph.add_edge("1", "2")
    graph.add_edge("1", "3")

    graph.add_edge("2", "1")
    graph.add_edge("2", "3")
    graph.add_edge("2", "4")

    graph.add_edge("3", "1")
    graph.add_edge("3", "2")
    graph.add_edge("3", "4")

    graph.add_edge("4", "2")
    graph.add_edge("4", "3")
    graph.add_edge("4", "5")
    graph.add_edge("4", "6")

    graph.add_edge("5", "4")
    graph.add_edge("5", "6")

    graph.add_edge("6", "4")
    graph.add_edge("6", "5")

    return graph
