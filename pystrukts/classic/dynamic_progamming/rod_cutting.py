"""
Module with a rot-cutting problem.
"""

from typing import Dict
from typing import List


def cut_rod_max_revenue(length: int, prices: List[int]) -> int:
    """
    Computes the maximum revenue obtained by cutting up a rod of given length
    and sellings its cut pieces based on the prices given by the prices argument.
    The rod can only be divided into integral pieces (integers), so min. length == 1.
    The prices list must be of size length + 1 (to include the price zero at ix == 0).

    Example:
                                   v˜˜˜˜ each ix holds the price of a rod of ix length!
    >>> cut_rod_max_revenue(4, [0, 1, 5, 8, 9])
    >>> 10  # maximum revenue
    """
    if len(prices) < length + 1:
        raise ValueError("Prices list is too short for the given rod length.")

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
        raise ValueError("Prices list is too short for the given rod length.")

    def cut_rot_aux(length: int, memory: Dict[int, int]) -> int:
        """
        Helper closure which adds a memory argument for the memoization technique.
        """
        # memo
        if length in memory:
            return memory[length]

        # trivial solutions
        if length == 0:
            return prices[0]

        if length == 1:
            return prices[1]

        max_revenue = 0

        # overlapping subproblems
        for i in range(1, length + 1):  # goes until length
            max_revenue = max(max_revenue, prices[i] + cut_rot_aux(length - i, memory))

        # caching of solved problems
        memory[length] = max_revenue
        return max_revenue

    return cut_rot_aux(length, dict())


def cut_rod_max_revenue_bottomup(length: int, prices: List[int]) -> int:
    """
    Optimized version of the cut_rod_max_revenue using a bottomup approach.
    """
    if len(prices) < length + 1:
        raise ValueError("Prices list is too short for the given rod length.")

    max_revenues = [prices[0], prices[1]] + [0] * (length - 1)

    # here i becomes the "new length" of a smaller rod subproblem
    for i in range(1, length + 1):
        max_revenue = 0

        # solve the smaller rod subproblem by looking up the 'max_revenues' previous solutions
        for j in range(1, i + 1):
            max_revenue = max(max_revenue, prices[j] + max_revenues[i - j])

        max_revenues[i] = max_revenue

    return max_revenues[length]
