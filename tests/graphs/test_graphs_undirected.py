"""
Module with tests for undirected graphs.
"""
import unittest

from pystrukts.graphs.undirected import Edge
from pystrukts.graphs.undirected import Graph
from pystrukts.graphs.undirected import Vertex


class TestSuiteGraph(unittest.TestCase):
    """
    Test suite for undirected graphs.
    """

    def test_should_create_empty_undirected_graph(self):
        """
        Should create an empty undirected graph.
        """
        # arrange and act
        g: Graph[str] = Graph()

        # assert
        self.assertEqual(g.edges, dict())
        self.assertEqual(g.vertices, dict())
        self.assertEqual(g.total_vertices, 0)
        self.assertEqual(g.total_edges, 0)

    def test_should_add_vertices_and_edges_to_undirected_graph(self):
        r"""
        Should add vertices and edges to undirected graph:

             1
           /   \
          2 --- 3
        """
        # arrange
        g: Graph[int] = Graph()

        vertex_1 = Vertex(1)
        vertex_2 = Vertex(2)
        vertex_3 = Vertex(3)

        # act
        g.add_vertex(vertex_1)
        g.add_vertex(vertex_2)
        g.add_vertex(vertex_3)

        # assert
        self.assertEqual(g.total_vertices, 3)
        self.assertEqual(g.total_edges, 0)

        # act
        g.add_edge(vertex_1, vertex_2)
        g.add_edge(vertex_1, vertex_3)
        g.add_edge(vertex_2, vertex_3)

        # assert
        self.assertEqual(g.total_edges, 3)
        self.assertEqual(vertex_1, g.vertices[vertex_1.key])
        self.assertEqual(vertex_2, g.vertices[vertex_2.key])
        self.assertEqual(vertex_3, g.vertices[vertex_3.key])

        expected_edge12 = Edge(vertex_1, vertex_2, 1)
        expected_edge13 = Edge(vertex_1, vertex_3, 1)
        expected_edge23 = Edge(vertex_2, vertex_3, 1)

        edge_12 = g.edges[(vertex_1, vertex_2)]
        edge_13 = g.edges[(vertex_1, vertex_3)]
        edge_23 = g.edges[(vertex_2, vertex_3)]

        self.assertEqual(edge_12, expected_edge12)
        self.assertEqual(edge_13, expected_edge13)
        self.assertEqual(edge_23, expected_edge23)
