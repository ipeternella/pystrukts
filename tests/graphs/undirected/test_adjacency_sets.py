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

    assert graph.get_adjacent_vertices("1") == {"2", "3"}
    assert graph.get_adjacent_vertices("2") == {"1", "3", "4"}
    assert graph.get_adjacent_vertices("3") == {"1", "2", "4", "5"}
    assert graph.get_adjacent_vertices("4") == {"2", "3"}
    assert graph.get_adjacent_vertices("5") == {"3"}

    assert graph.has_vertex("1")
    assert graph.has_vertex("2")
    assert graph.has_vertex("3")
    assert graph.has_vertex("4")
    assert graph.has_vertex("5")
    assert graph.has_vertex("6") is False

    assert graph.has_edge("1", "2")
    assert graph.has_edge("1", "3")

    assert graph.has_edge("2", "1")
    assert graph.has_edge("2", "3")
    assert graph.has_edge("2", "4")

    assert graph.has_edge("3", "1")
    assert graph.has_edge("3", "2")
    assert graph.has_edge("3", "4")
    assert graph.has_edge("3", "5")

    assert graph.has_edge("4", "2")
    assert graph.has_edge("4", "3")

    assert graph.has_edge("5", "3")

    assert graph.has_edge("5", "1") is False
    assert graph.has_edge("5", "4") is False
    assert graph.has_edge("2", "5") is False


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

    assert graph.get_adjacent_vertices("1") == {"2", "3", "5"}
    assert graph.get_adjacent_vertices("2") == {"1", "3", "4"}
    assert graph.get_adjacent_vertices("3") == {"1", "2", "4", "5"}
    assert graph.get_adjacent_vertices("4") == {"2", "3", "5"}
    assert graph.get_adjacent_vertices("5") == {"1", "3", "4"}

    assert graph.has_edge("5", "1")
    assert graph.has_edge("5", "3")
    assert graph.has_edge("5", "4")
    assert graph.has_edge("5", "2") is False


def test_should_raise_exception_when_vertex_not_found_for_adjacency(triangular_graph_fixture: Graph[str]):
    # arrange
    graph = triangular_graph_fixture

    # act and assert
    assert graph.get_adjacent_vertices("1") == {"2", "3"}
    assert graph.get_adjacent_vertices("2") == {"1", "3"}
    assert graph.get_adjacent_vertices("3") == {"1", "2"}

    with pytest.raises(VertexNotFoundError):
        graph.get_adjacent_vertices("5")
