"""
Module with grid-traveling problems which can be solved with dynamic programming.

Problem:
    Given a 2D (m x n) grid that one wants to travel from top-left corner to the
    bottom-right corner and the restriction that it's only possible to move down
    or right, compute the amount of possible ways to reach the bottom-right destination.
"""

from typing import Dict
from typing import Tuple

Pair = Tuple[int, int]


def count_ways_grid2d_bruteforce(m: int, n: int) -> int:
    """
    Naive/brute-force solution for the 2D grid traveler problem. It will "get stuck" for larger
    inputs as the time complexity is O(2 ^ (n + m)).
    """
    if m == 0 or n == 0:
        return 0

    if m == 1 or n == 1:
        return 1

    return count_ways_grid2d_bruteforce(m, n - 1) + count_ways_grid2d_bruteforce(m - 1, n)


def count_ways_grid2d_memoized(m: int, n: int) -> int:
    """
    Optimization of the 2D grid traveler problem using memoization.
    """

    def count_ways_grid2d_helper(m: int, n: int, memory: Dict[Pair, int]) -> int:
        pair = (m, n)

        if pair in memory:
            return memory[pair]

        if m == 0 or n == 0:
            return 0

        if m == 1 or n == 1:
            return 1

        memory[pair] = count_ways_grid2d_helper(m, n - 1, memory) + count_ways_grid2d_helper(m - 1, n, memory)
        return memory[pair]

    return count_ways_grid2d_helper(m, n, dict())


def count_ways_grid2d_bottomup(m: int, n: int) -> int:
    """
    Optimization of the 2D grid traveler problem using tabulation.
    """
    solutions = [[0] * (n + 1) for _ in range(m + 1)]  # 2d tabulation
    solutions[0][1] = 1  # this OR [1][0] must be 1 (never both)

    for row in range(1, m + 1):
        for col in range(1, n + 1):
            solutions[row][col] = solutions[row - 1][col] + solutions[row][col - 1]

    return solutions[m][n]
