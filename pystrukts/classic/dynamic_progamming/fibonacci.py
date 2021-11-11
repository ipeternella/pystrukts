"""
Module with fibonacci computation problems which can be solved with dynamic programming.

Problem:
    Compute the n-th Fibonacci number.
"""

from typing import Dict


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


def fibonacci_memoized(n: int) -> int:
    """
    Optimized version of the n-th Fibonacci number computation with memoization.
    Time complexity: O(n).
    """

    def fibonacci_helper(n: int, memory: Dict[int, int]) -> int:
        if n in memory:
            return memory[n]

        if n == 0:
            return 0

        if n <= 2:
            return 1

        memory[n] = fibonacci_helper(n - 1, memory) + fibonacci_helper(n - 2, memory)
        return memory[n]

    return fibonacci_helper(n, dict())


def fibonacci_bottomup(n: int) -> int:
    """
    Optimized version of the n-th Fibonacci number computation with tabulation. Notice
    that iterative solutions (bottomup approach) usually offers lower constant factors.
    """
    # initialization of (n + 1) solutions 0 .. n
    solutions = [0, 1, 1] + [0] * (n - 2)

    for i in range(0, n - 1):
        solutions[i + 2] = solutions[i] + solutions[i + 1]

    return solutions[n]
