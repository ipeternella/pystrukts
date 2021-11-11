"""
Module with tests for grid traveler problems.
"""
import unittest

from pystrukts.classic.dynamic_progamming.grid_traveler import count_ways_grid2d_bottomup
from pystrukts.classic.dynamic_progamming.grid_traveler import count_ways_grid2d_bruteforce
from pystrukts.classic.dynamic_progamming.grid_traveler import count_ways_grid2d_memoized


class DynamicGridTravelerTestSuite(unittest.TestCase):
    """
    Grid traveler problem test suite.
    """

    def test_should_count_ways_grid2d_bruteforce_on_2x3(self):
        """
        Should count the possible ways to travel on a 2D grid 2x3 with the brute-force algorithm.
        """
        # arrange
        m = 2
        n = 3

        # act
        amount_ways = count_ways_grid2d_bruteforce(m, n)

        # assert
        self.assertEqual(amount_ways, 3)

    def test_should_count_ways_grid2d_memoized_on_18x18(self):
        """
        Should quickly compute possible ways for a large grid of 18x18 using memoized optimization.
        """
        # arrange
        m = 18
        n = 18

        # act
        amount_ways = count_ways_grid2d_memoized(m, n)

        # assert
        self.assertEqual(amount_ways, 2333606220)

    def test_should_count_ways_grid2d_bottomup_on_18x18(self):
        """
        Should quickly compute possible ways for a large grid of 18x18 using bottomup optimization.
        """
        # arrange
        m = 18
        n = 18

        # act
        amount_ways = count_ways_grid2d_bottomup(m, n)

        # assert
        self.assertEqual(amount_ways, 2333606220)
