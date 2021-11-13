"""
Module with tests for shortest-paths graphs problems.
"""
import unittest

from pystrukts.graphs import Graph
from pystrukts.graphs.common import Vertex
from pystrukts.graphs.shortest_paths import bellman_ford


class TestSuiteShortestPathsGraphs(unittest.TestCase):
    """
    Test suite for shortest-paths graphs problems.
    """

    def test_should_run_bellman_ford_without_negative_weight_cycles(self):
        """
        Should run Bellman-Ford without negative weight cycles (algorithm should return True).
        """
        # arrange
        g: Graph[str] = self.build_weighted_and_directed_graph_1()
        s: Vertex[str] = g.get_vertex("s")

        # act
        has_no_negative_weight_cycle = bellman_ford(g, s)

        # assert
        self.assertTrue(has_no_negative_weight_cycle)
        self.assertEqual(g.get_vertex("s").distance, 0)
        self.assertEqual(g.get_vertex("t").distance, 3)
        self.assertEqual(g.get_vertex("x").distance, 9)
        self.assertEqual(g.get_vertex("y").distance, 5)
        self.assertEqual(g.get_vertex("z").distance, 11)

    def test_should_run_bellman_ford_with_negative_weight_cycles(self):
        """
        Should run Bellman-Ford without negative weight cycles (algorithm should return False).
        """
        # arrange
        g: Graph[str] = self.build_negative_weight_cycle_graph()
        s: Vertex[str] = g.get_vertex("s")

        # act
        has_no_negative_weight_cycle = bellman_ford(g, s)

        # assert
        self.assertFalse(has_no_negative_weight_cycle)

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

    def build_negative_weight_cycle_graph(self) -> Graph[str]:
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
        g.add_edge(y, z, 6)
        g.add_edge(y, x, 4)
        g.add_edge(z, s, 3)

        # negative weight cycle
        g.add_edge(x, z, 2)
        g.add_edge(z, x, -7)

        return g
