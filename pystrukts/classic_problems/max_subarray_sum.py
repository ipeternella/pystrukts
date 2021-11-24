"""
Classic problem for computing max subarray sum.
"""

from typing import List


def max_subarray_sum(numbers: List[int]) -> int:
    """
    Finds subarray with max sum in O(N) time complexity, often known
    as the Kadane's algorithm.
    """
    n = len(numbers)
    best = 0
    sum_value = 0

    for i in range(0, n):
        sum_value = max(numbers[i], sum_value + numbers[i])  # keeps adding to the sum unless value drops
        best = max(best, sum_value)

    return best


def max_subarray_sum_ii(numbers: List[int]) -> int:
    """
    Finds subarray with max sum in O(N^2) time complexity.
    """
    n = len(numbers)
    best = 0

    for i in range(0, n):
        sum_value = 0

        for j in range(i, n):
            sum_value += numbers[j]  # eventually decreases, but best is saved
            best = max(best, sum_value)

    return best


def max_subarray_sum_iii(numbers: List[int]) -> int:
    """
    Finds subarray with max sum in O(N^3) time complexity.
    """
    n = len(numbers)
    best = 0

    for i in range(0, n):
        for j in range(i, n):
            sum_value = 0
            # sums subarray marked by i .. j
            for k in range(i, j + 1):
                sum_value += numbers[k]

            best = max(best, sum_value)

    return best
