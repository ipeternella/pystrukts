"""
Module with fibonacci computation problems which can be solved with dynamic programming.
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


def fibonacci_memoized(n: int, memory: Dict[int, int] = dict()) -> int:
    """
    Optimized version of the n-th Fibonacci number computation with memoization.
    Time complexity: O(n).
    """
    if memo := memory.get(n):
        return memo

    if n == 0:
        return 0

    if n <= 2:
        return 1

    memory[n] = fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)
    return memory[n]
