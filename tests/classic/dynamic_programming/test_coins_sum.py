"""
Module with tests for the coin sum problem.
"""
import unittest

from pystrukts.classic.dynamic_progamming.coin_sum import minimize_coins_bottomup
from pystrukts.classic.dynamic_progamming.coin_sum import minimize_coins_memoized


class CoinsSumProblemTestSuite(unittest.TestCase):
    """
    Coins sum problem test suite.
    """

    def test_should_minimize_coins_memoized(self):
        """
        Should minimize coins for target 10 using the memoized algorithm.
        """
        # arrange
        coins = [1, 4, 3]
        target = 10

        # act
        min_coins = minimize_coins_memoized(target, coins)

        # assert
        self.assertEqual(min_coins, 3)

    def test_should_not_find_solution_minimize_coins_memoized(self):
        """
        Should not minimize coins for target 5.
        """
        # arrange
        coins = [2, 6, 7]
        target = 5

        # act
        min_coins = minimize_coins_memoized(target, coins)

        # assert
        self.assertEqual(min_coins, -1)

    def test_should_minimize_coins(self):
        """
        Should minimize coins for target 10.
        """
        # arrange
        coins = [1, 4, 3]
        target = 10

        # act
        min_coins = minimize_coins_bottomup(target, coins)

        # assert
        self.assertEqual(min_coins, 3)

        # arrange
        coins = [2, 6, 7]
        target = 5

        # act
        min_coins = minimize_coins_bottomup(target, coins)

        # assert
        self.assertEqual(min_coins, -1)

    def test_should_not_find_solution_for_minimize_coins(self):
        """
        Should not minimize coins for target 5.
        """
        # arrange
        coins = [2, 6, 7]
        target = 5

        # act
        min_coins = minimize_coins_bottomup(target, coins)

        # assert
        self.assertEqual(min_coins, -1)

    def test_should_minimize_coins_with_single_coin(self):
        """
        Should minimize coins for target 10.
        """
        # arrange
        coins = [1, 4, 3]
        target = 4

        # act
        min_coins = minimize_coins_bottomup(target, coins)

        # assert
        self.assertEqual(min_coins, 1)
