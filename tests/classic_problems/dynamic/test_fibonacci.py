"""
Module with tests for fibonacci computation problems.
"""
import unittest

from pystrukts.classic_problems.dynamic.fibonacci import fibonacci_bottomup
from pystrukts.classic_problems.dynamic.fibonacci import fibonacci_bruteforce
from pystrukts.classic_problems.dynamic.fibonacci import fibonacci_memoized


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
        Should compute some fibonacci numbers using the memoized optimization.
        """
        # arrange
        n = 50

        # act
        fibo = fibonacci_memoized(n)

        # assert
        self.assertEqual(fibo, 12586269025)

    def test_should_compute_fibonacci_numbers_bottomup(self):
        """
        Should compute some fibonacci numbers using the bottomup optimization.
        """
        # arrange
        n_1 = 0
        n_2 = 1
        n_3 = 2
        n_4 = 6
        n_5 = 7
        n_6 = 50

        # act
        fibo_1 = fibonacci_bottomup(n_1)
        fibo_2 = fibonacci_bottomup(n_2)
        fibo_3 = fibonacci_bottomup(n_3)
        fibo_4 = fibonacci_bottomup(n_4)
        fibo_5 = fibonacci_bottomup(n_5)
        fibo_6 = fibonacci_bottomup(n_6)

        # assert
        self.assertEqual(fibo_1, 0)
        self.assertEqual(fibo_2, 1)
        self.assertEqual(fibo_3, 1)
        self.assertEqual(fibo_4, 8)
        self.assertEqual(fibo_5, 13)
        self.assertEqual(fibo_6, 12586269025)
