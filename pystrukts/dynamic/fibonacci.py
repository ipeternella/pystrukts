"""
Module with fibonacci computation problems which can be solved with dynamic programming.
"""

from typing import Dict
from typing import Optional


def fibonacci_bruteforce(n: int) -> int:
    """
    Brute-force recursive solution for computing the n-th Fibonacci number.
    Time complexity: O(2 ^ n).
    """
    if n == 0:
        return 0

    if n <= 2:
        return 1

    return fibonacci_bruteforce(n - 1) + fibonacci_bruteforce(n - 2)


def fibonacci_memoized(n: int, memory: Optional[Dict[int, int]] = None) -> int:
    """
    Optimized version of the n-th Fibonacci number computation with memoization.
    Time complexity: O(n).
    """
    # memoization
    if memory is None:
        memory = dict()

    if n in memory:
        return memory[n]

    # trivial cases
    if n == 0:
        return 0

    if n <= 2:
        return 1

    # recursion
    memory[n] = fibonacci_memoized(n - 1, memory) + fibonacci_memoized(n - 2, memory)
    return memory[n]


def fibonacci_bottomup(n: int) -> int:
    """
    Optimized version of the n-th Fibonacci number computation with tabulation.
    """
    # initialization of (n + 1) elements: [0, 1, 1, ...] to store the previous solutions
    solutions = [0, 1, 1] + [0] * (n - 1)

    # loop for solving from bottom up
    for i in range(0, n - 1):
        solutions[i + 2] = solutions[i] + solutions[i + 1]

    return solutions[n]
