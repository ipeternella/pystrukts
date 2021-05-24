"""
Module with tests for the Depth First Algorithm.
"""

import pytest

from algorithms.graphs.exceptions import VertexNotFoundError
from algorithms.graphs.undirected.adjacency_sets import Graph
from algorithms.graphs.undirected.depth_first_search import DepthFirstSearch


def test_should_depth_first_search_a_triangular_graph(triangular_graph_fixture: Graph[str]):
    # arrange
    graph = triangular_graph_fixture
    source_vertex = "1"  # entry point of the graph

    # act
    dfs_results = DepthFirstSearch(graph, source_vertex)

    # assert
    assert dfs_results.visited("1") is True
    assert dfs_results.visited("2") is True
    assert dfs_results.visited("3") is True
    assert dfs_results.visited("5") is False  # not inside the graph
    assert dfs_results.count() == 3


def test_should_depth_first_search_a_key_graph(key_graph_fixture: Graph[str]):
    # arrange
    graph = key_graph_fixture
    source_vertex = "5"  # entry point of the graph

    # act
    dfs_results = DepthFirstSearch(graph, source_vertex)

    # assert
    assert dfs_results.visited("1") is True
    assert dfs_results.visited("2") is True
    assert dfs_results.visited("3") is True
    assert dfs_results.visited("4") is True
    assert dfs_results.visited("5") is True
    assert dfs_results.visited("6") is True
    assert dfs_results.visited("7") is False  # not inside the graph
    assert dfs_results.count() == 6


def test_should_raise_exception_in_depth_first_search_graph_if_source_vertex_is_not_found(
    triangular_graph_fixture: Graph[str],
):
    # arrange
    graph = triangular_graph_fixture
    unknown_source_vertex = "NOT_FOUND"  # entry point of the graph

    # act & assert
    with pytest.raises(VertexNotFoundError):
        DepthFirstSearch(graph, unknown_source_vertex)
