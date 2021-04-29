"""
Module with tests for the undirected graphs based on adjacency sets.
"""
import pytest

from algorithms.graphs.exceptions import VertexNotFoundError
from algorithms.graphs.undirected.adjacency_sets import Graph


@pytest.fixture
def triangular_graph_fixture() -> Graph[str]:
    """
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


def test_should_create_new_graph_5_vertices_6_edges():
    r"""
    Expected graph:

      1
     / \
    2 - 3 - 5
     \ /
      4

    [1] -> [2, 3]
    [2] -> [1, 3, 4]
    [3] -> [1, 2, 4, 5]
    [4] -> [2, 3]
    [5] -> [3]
    """
    # arrange
    graph: Graph[str] = Graph()

    # act
    # [1] -> [2, 3]
    graph.add_edge("1", "2")
    graph.add_edge("1", "3")

    # [2] -> [1, 3, 4]
    graph.add_edge("2", "1")
    graph.add_edge("2", "3")
    graph.add_edge("2", "4")

    # [3] -> [1, 2, 4, 5]
    graph.add_edge("3", "1")
    graph.add_edge("3", "2")
    graph.add_edge("3", "4")
    graph.add_edge("3", "5")

    # [4] -> [2, 3]
    graph.add_edge("4", "2")
    graph.add_edge("4", "3")

    # [5] -> [3]
    graph.add_edge("5", "3")

    # assert
    assert graph.vertices == 5
    assert graph.edges == 6

    assert graph.adjacent("1") == {"2", "3"}
    assert graph.adjacent("2") == {"1", "3", "4"}
    assert graph.adjacent("3") == {"1", "2", "4", "5"}
    assert graph.adjacent("4") == {"2", "3"}
    assert graph.adjacent("5") == {"3"}


def test_should_create_new_graph_5_vertices_8_edges():
    r"""
    Expected graph:

      1 \
     / \  \
    2 - 3 - 5
     \ /  /
      4 /

    [1] -> [2, 3, 5]
    [2] -> [1, 3, 4]
    [3] -> [1, 2, 4, 5]
    [4] -> [2, 3, 5]
    [5] -> [1, 3, 4]
    """
    # arrange
    graph: Graph[str] = Graph()

    # act
    # [1] -> [2, 3]
    graph.add_edge("1", "2")
    graph.add_edge("1", "3")

    # [2] -> [1, 3, 4]
    graph.add_edge("2", "1")
    graph.add_edge("2", "3")
    graph.add_edge("2", "4")

    # [3] -> [1, 2, 4, 5]
    graph.add_edge("3", "1")
    graph.add_edge("3", "2")
    graph.add_edge("3", "4")
    graph.add_edge("3", "5")
    graph.add_edge("3", "5")  # parallel edge: should not be added to graph

    # [4] -> [2, 3]
    graph.add_edge("4", "2")
    graph.add_edge("4", "3")

    # [5] -> [3]
    graph.add_edge("5", "1")
    graph.add_edge("5", "3")
    graph.add_edge("5", "4")
    graph.add_edge("5", "4")  # parallel edge: should not be added to graph

    # assert
    assert graph.vertices == 5
    assert graph.edges == 8

    assert graph.adjacent("1") == {"2", "3", "5"}
    assert graph.adjacent("2") == {"1", "3", "4"}
    assert graph.adjacent("3") == {"1", "2", "4", "5"}
    assert graph.adjacent("4") == {"2", "3", "5"}
    assert graph.adjacent("5") == {"1", "3", "4"}


def test_should_raise_exception_when_vertex_not_found_for_adjacency(triangular_graph_fixture: Graph[str]):
    # arrange
    graph = triangular_graph_fixture

    # act and assert
    assert graph.adjacent("1") == {"2", "3"}
    assert graph.adjacent("2") == {"1", "3"}
    assert graph.adjacent("3") == {"1", "2"}

    with pytest.raises(VertexNotFoundError):
        graph.adjacent("5")
