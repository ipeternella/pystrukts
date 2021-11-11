"""
Module with coin summation problem.

Problem:
    Given a set of coin values {C1, C2, ..., Cn} and target sum, n,
    count the min required amount of coins to reach the sum or -1 if
    the sum is not possible.
"""
import sys
from typing import Dict
from typing import List

INF = sys.maxsize


def minimize_coins_memoized(target: int, coins: List[int]) -> int:
    """
    Dynamic programming solution using memoization.
    """

    def minimize_coins_helper(target: int, coins: List[int], memory: Dict[int, int]) -> int:
        min_coins = INF

        if target in memory:
            return memory[target]

        if target == 0:
            return 0

        if target < 0:
            return INF  # impossible path

        for coin in coins:
            min_coins = min(min_coins, minimize_coins_helper(target - coin, coins, memory) + 1)

        memory[target] = min_coins
        return min_coins

    min_coins = minimize_coins_helper(target, coins, dict())
    return min_coins if min_coins != INF else -1


def minimize_coins_bottomup(target: int, coins: List[int]) -> int:
    """
    Dynamic programming solution using tabulation.
    """
    state = [INF] * (target + 1)  # min() requires INF initilization as new values are always less than INF
    state[0] = 0
    coins = sorted(coins)

    for local_target in range(0, target + 1):
        for coin in coins:

            if local_target - coin >= 0:
                state[local_target] = min(state[local_target], state[local_target - coin] + 1)

    return state[target] if state[target] != INF else -1
