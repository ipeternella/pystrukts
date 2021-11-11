"""
Module with tests for the rod cutting problem.
"""
import unittest

from pystrukts.classic.dynamic_progamming.rod_cutting import cut_rod_max_revenue
from pystrukts.classic.dynamic_progamming.rod_cutting import cut_rod_max_revenue_bottomup
from pystrukts.classic.dynamic_progamming.rod_cutting import cut_rod_max_revenue_memoized


class RodCuttingDynamicTestSuite(unittest.TestCase):
    """
    Rod cutting problem test suite.
    """

    def test_should_compute_max_revenue_of_given_cut_rod(self):
        """
        Should compute the max revenue of a given cut rot.
        """
        # arrange
        length = 4
        prices = [0, 1, 5, 8, 9]  # length + 1 prices always

        # act
        max_revenue = cut_rod_max_revenue(length, prices)

        # assert
        self.assertEqual(max_revenue, 10)

    def test_should_compute_max_revenue_of_large_rod_memoized(self):
        """
        Should compute the max revenue of a large rod with the memoized optimization.
        """
        # arrange - large rod: 500 inches, for exemple
        length = 500
        prices = list(range(0, 501))

        # act
        max_revenue = cut_rod_max_revenue_memoized(length, prices)

        # assert
        self.assertEqual(max_revenue, 500)

    def test_should_compute_max_revenue_of_large_rod_bottomup(self):
        """
        Should compute the max revenue of a large rod with the bottomup optimization.
        """
        # arrange - large rod: 500 inches, for exemple
        length = 500
        prices = list(range(0, 501))

        # act
        max_revenue = cut_rod_max_revenue_bottomup(length, prices)

        # assert
        self.assertEqual(max_revenue, 500)
