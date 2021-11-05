"""
Module with tests for common graph algorithms.
"""
import unittest

from pystrukts.graphs import Edge
from pystrukts.graphs import Graph
from pystrukts.graphs import VertexColor


class TestSuiteGraph(unittest.TestCase):
    """
    Test suite for common graph algorithms.
    """

    def test_should_create_empty_graph(self):
        """
        Should create an empty graph.
        """
        # arrange and act
        g: Graph[str] = Graph()

        # assert
        self.assertEqual(g.edges, dict())
        self.assertEqual(g.vertices, dict())
        self.assertEqual(g.total_vertices, 0)
        self.assertEqual(g.total_edges, 0)

    def test_should_add_vertices_and_edges_to_graph(self):
        r"""
        Should add vertices and edges to an undirected graph:

           1
         /   \
        2 --- 3
        """
        # arrange
        g: Graph[int] = Graph()

        # act
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_vertex(3)

        # assert
        vertex_1 = g.get_vertex(1)
        vertex_2 = g.get_vertex(2)
        vertex_3 = g.get_vertex(3)

        self.assertEqual(g.total_vertices, 3)
        self.assertEqual(g.total_edges, 0)
        self.assertEqual(vertex_1.color, VertexColor.WHITE)
        self.assertEqual(vertex_2.color, VertexColor.WHITE)
        self.assertEqual(vertex_3.color, VertexColor.WHITE)

        # act
        g.add_edge(vertex_1, vertex_2)
        g.add_edge(vertex_1, vertex_3)
        g.add_edge(vertex_2, vertex_3)

        # assert
        self.assertEqual(g.total_edges, 3)
        self.assertEqual(vertex_1, g.get_vertex(1))
        self.assertEqual(vertex_2, g.get_vertex(2))
        self.assertEqual(vertex_3, g.get_vertex(3))

        expected_edge12 = Edge(vertex_1, vertex_2, 1)
        expected_edge13 = Edge(vertex_1, vertex_3, 1)
        expected_edge23 = Edge(vertex_2, vertex_3, 1)

        edge_12 = g.get_edge(vertex_1, vertex_2)
        edge_13 = g.get_edge(vertex_1, vertex_3)
        edge_23 = g.get_edge(vertex_2, vertex_3)

        self.assertEqual(edge_12, expected_edge12)
        self.assertEqual(edge_13, expected_edge13)
        self.assertEqual(edge_23, expected_edge23)

    def test_should_run_bfs_using_graph_1(self):
        """
        Should run BFS using graph 1.
        """
        # arrange
        g = self.create_graph_1()
        vertex_1 = g.get_vertex(1)

        # act
        g.bfs(source=vertex_1)

        # assert
        vertex_2 = g.get_vertex(2)
        vertex_3 = g.get_vertex(2)

        self.assertEqual(vertex_1.color, VertexColor.BLACK)
        self.assertEqual(vertex_2.color, VertexColor.BLACK)
        self.assertEqual(vertex_3.color, VertexColor.BLACK)

        self.assertEqual(vertex_1.distance, 0)
        self.assertEqual(vertex_2.distance, 1)
        self.assertEqual(vertex_3.distance, 1)

        self.assertIsNone(vertex_1.parent)
        self.assertEqual(vertex_2.parent, vertex_1)
        self.assertEqual(vertex_3.parent, vertex_1)

    def test_should_run_dfs_using_graph_1(self):
        """
        Should run DFS using graph 1.
        """
        # arrange
        g = self.create_graph_1()

        # act
        g.dfs()

        # assert
        vertex_1 = g.get_vertex(1)
        vertex_2 = g.get_vertex(2)
        vertex_3 = g.get_vertex(3)

        self.assertEqual(vertex_1.color, VertexColor.BLACK)
        self.assertEqual(vertex_2.color, VertexColor.BLACK)
        self.assertEqual(vertex_3.color, VertexColor.BLACK)

        self.assertIsNone(vertex_1.parent)
        self.assertEqual(vertex_2.parent, vertex_1)
        self.assertEqual(vertex_3.parent, vertex_2)  # vertex_1 will be gray, so vertex_3's parent is vertex_1

    def create_graph_1(self) -> Graph[int]:
        r"""
        Creates testing graph 1 (triangular):

           1
         /   \
        2 --- 3
        """
        g: Graph[int] = Graph()

        g.add_vertex(1)
        g.add_vertex(2)
        g.add_vertex(3)

        vertex_1 = g.get_vertex(1)
        vertex_2 = g.get_vertex(2)
        vertex_3 = g.get_vertex(3)

        g.add_edge(vertex_1, vertex_2)  # type: ignore
        g.add_edge(vertex_1, vertex_3)  # type: ignore
        g.add_edge(vertex_2, vertex_3)  # type: ignore

        return g
