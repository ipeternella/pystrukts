"""
Module with tests for the classic max subarray problem algorithms.
"""
import unittest
from typing import List

from pystrukts.classic.max_subarray_sum import max_subarray_sum_iii


class ClassicMaxSubArrayTestSuite(unittest.TestCase):
    """
    Test suite for the classic problem of max subarray sum.
    """

    def test_should_find_max_subarray_iii(self):
        # arrange
        numbers = self.create_list_1()

        # act
        max_sum = max_subarray_sum_iii(numbers)

        # assert
        self.assertEqual(max_sum, 10)

    def create_list_1() -> List[int]:
        """
        Creates a list whose max subarray is [2, 4, -3, 5, 2] and
        whose sum == 10.
        """

        return [-1, 2, 4, -3, 5, 2, -5, 2]
