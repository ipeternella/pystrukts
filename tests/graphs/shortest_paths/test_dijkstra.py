"""
Module with tests for Dijkstra's algorithm.
"""
import unittest

from pystrukts.graphs import Graph
from pystrukts.graphs.common import Vertex
from pystrukts.graphs.shortest_paths.dijkstra import dijkstra


class DijkstraShortestPathsTestSuite(unittest.TestCase):
    """
    Test suite for Dijkstra's algorithm for the shortest-paths graphs problem.
    """

    def test_should_run_dijkstras_algorithm_on_graph_without_negative_weight_cycles(self):
        """
        Should run Dijkstra's algorithm on graph without negative weight cycles.
        """
        # arrange
        g: Graph[str] = self.build_weighted_and_directed_graph_1()
        s: Vertex[str] = g.get_vertex("s")

        # act
        dijkstra(g, s)

        # assert
        self.assertEqual(g.get_vertex("s").distance, 0)
        self.assertEqual(g.get_vertex("t").distance, 3)
        self.assertEqual(g.get_vertex("x").distance, 9)
        self.assertEqual(g.get_vertex("y").distance, 5)
        self.assertEqual(g.get_vertex("z").distance, 11)

    def build_weighted_and_directed_graph_1(self) -> Graph[str]:
        g: Graph[str] = Graph(directed=True, weighted=True)

        s = g.add_vertex("s")
        t = g.add_vertex("t")
        x = g.add_vertex("x")
        y = g.add_vertex("y")
        z = g.add_vertex("z")

        g.add_edge(s, t, 3)
        g.add_edge(t, x, 6)
        g.add_edge(t, y, 2)
        g.add_edge(y, t, 1)
        g.add_edge(s, y, 5)
        g.add_edge(x, z, 2)
        g.add_edge(z, x, 7)
        g.add_edge(y, z, 6)
        g.add_edge(y, x, 4)
        g.add_edge(z, s, 3)

        return g
