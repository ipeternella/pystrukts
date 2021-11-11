"""
Module with a rot-cutting problem.

Problem:
    Compute the maximum revenue obtained by cutting up a rod of given length
    and sellings its cut pieces based on the prices given by the prices argument.
    The rod can only be divided into integral pieces (integers), so min. length == 1.
    The prices list must be of size length + 1 (to include the price zero at ix == 0).

    Example:
                                   v˜˜˜˜ each ix holds the price of a rod of ix length!
    >>> cut_rod_max_revenue(4, [0, 1, 5, 8, 9])
    >>> 10  # maximum revenue
"""

from typing import Dict
from typing import List


class PriceListLengthMismatch(Exception):
    """
    Raised when the prices list is too short for the given rod length.
    """


def cut_rod_max_revenue(length: int, prices: List[int]) -> int:
    """
    Naive/brute-force solution for the rod cutting problem.
    """
    if len(prices) < length + 1:
        raise PriceListLengthMismatch

    if length == 0:
        return prices[0]

    if length == 1:
        return prices[1]

    max_revenue = 0

    for i in range(1, length + 1):  # goes until length
        max_revenue = max(max_revenue, prices[i] + cut_rod_max_revenue(length - i, prices))

    return max_revenue


def cut_rod_max_revenue_memoized(length: int, prices: List[int]) -> int:
    """
    Optimized version of the cut_rod_max_revenue function using memoization (top-down approach).
    """
    if len(prices) < length + 1:
        raise PriceListLengthMismatch

    def cut_rot_helper(length: int, memory: Dict[int, int]) -> int:
        if length in memory:
            return memory[length]

        if length == 0:
            return prices[0]

        if length == 1:
            return prices[1]

        max_revenue = 0

        # overlapping subproblems
        for i in range(1, length + 1):  # goes until length
            max_revenue = max(max_revenue, prices[i] + cut_rot_helper(length - i, memory))

        # caching of solved problems
        memory[length] = max_revenue
        return max_revenue

    return cut_rot_helper(length, dict())


def cut_rod_max_revenue_bottomup(length: int, prices: List[int]) -> int:
    """
    Optimized version of the cut_rod_max_revenue using tabulation.
    """
    if len(prices) < length + 1:
        raise PriceListLengthMismatch

    solutions = [prices[0], prices[1]] + [0] * (length - 1)

    # here i becomes the "new length" of a smaller rod subproblem until we reach the target length
    for i in range(1, length + 1):
        # solve the smaller rod subproblem with previously tabulated solutions
        max_revenue = 0

        for j in range(1, i + 1):
            max_revenue = max(max_revenue, prices[j] + solutions[i - j])

        solutions[i] = max_revenue

    return solutions[length]
