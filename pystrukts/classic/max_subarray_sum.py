"""
Classic problem for computing max subarray sum.
"""

from typing import List


def max_subarray_sum_iii(numbers: List[int]) -> int:
    """
    Finds subarray with max sum in O(N^3) time complexity.
    """

    n = len(numbers)
    best = 0

    for i in range(0, n):
        for j in range(i, n):
            sum = 0
            for k in range(i, j + 1):
                sum += numbers[k]

            best = max(best, sum)

    return best
