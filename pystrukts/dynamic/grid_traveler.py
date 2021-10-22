"""
Module with grid-traveling problems which can be solved with dynamic programming.
"""

from typing import Dict
from typing import Optional
from typing import Tuple

Pair = Tuple[int, int]


def count_possible_ways_grid2D_bruteforce(m: int, n: int) -> int:
    """
    Given a 2D (m x n) grid that one wants to travel from top-left corner to the
    bottom-right corner and the restriction that it's only possible to move down
    or right, this procedure computes the amount of possible ways to reach the
    bottom-right destination.

    This algorithm is the naive/brute-force solution and will get stuck for larger
    inputs as the time complexity is O(2 ^ (n + m)).
    """
    if m == 0 or n == 0:
        return 0

    if m == 1 or n == 1:
        return 1

    return count_possible_ways_grid2D_bruteforce(m, n - 1) + count_possible_ways_grid2D_bruteforce(m - 1, n)


def count_possible_ways_grid2D_memoized(m: int, n: int, memory: Optional[Dict[Pair, int]] = None) -> int:
    """
    Optimization of the 2D grid traveler problem using memoization.
    """
    pair = (m, n)

    # memoization
    if memory is None:
        memory = dict()

    if memo := memory.get(pair):
        return memo

    # trivial cases
    if m == 0 or n == 0:
        return 0

    if m == 1 or n == 1:
        return 1

    # recursion
    memory[pair] = count_possible_ways_grid2D_memoized(m, n - 1, memory) + count_possible_ways_grid2D_memoized(
        m - 1, n, memory
    )

    return memory[pair]
