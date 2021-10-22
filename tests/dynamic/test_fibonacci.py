"""
Module with tests for fibonacci computation problems.
"""
import unittest

from pystrukts.dynamic.fibonacci import fibonacci_bruteforce
from pystrukts.dynamic.fibonacci import fibonacci_memoized


class DynamicFibonacciTestSuite(unittest.TestCase):
    """
    Fibonacci computation test suite.
    """

    def test_should_compute_fibonacci_numbers_bruteforce(self):
        """
        Should compute some fibonacci numbers using the brute-force method.
        """
        # arrange
        n_1 = 4
        n_2 = 6
        n_3 = 7

        # act
        fibo_1 = fibonacci_bruteforce(n_1)
        fibo_2 = fibonacci_bruteforce(n_2)
        fibo_3 = fibonacci_bruteforce(n_3)

        # assert
        self.assertEqual(fibo_1, 3)
        self.assertEqual(fibo_2, 8)
        self.assertEqual(fibo_3, 13)

    def test_should_compute_fibonacci_numbers_memoized(self):
        """
        Should compute some fibonacci numbers using the memoized version.
        """
        # arrange
        n = 50

        # act
        fibo = fibonacci_memoized(n)

        # assert
        self.assertEqual(fibo, 12586269025)
