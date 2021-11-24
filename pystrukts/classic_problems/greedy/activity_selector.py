"""
Module with the activity selector problem.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Activity:
    """
    Models an activity which starts and finishes at integer hours.
    The activities are sorted based on the 'finishes_at' property.
    """

    starts_at: int
    finishes_at: int

    def __lt__(self, other: Activity):
        return self.finishes_at < other.finishes_at


def select_compatible_activities(activities: List[Activity]) -> List[Activity]:
    """
    Computes the maximum compatible activities using a greedy algorithm.

    a0 = Activity(starts_at=1, finishes_at=4)
    a1 = Activity(starts_at=3, finishes_at=5)
    a2 = Activity(starts_at=0, finishes_at=6)
    a3 = Activity(starts_at=5, finishes_at=7)

    >>> select_compatible_activities([a0, a1, a2, a3])
    >>> [a0, a3]
    """
    # activities are sorted (asc) in terms of the 'finishes_at' time
    sorted_activities = sorted(activities)
    compatible_activities = [sorted_activities[0]]
    greedy_choice = sorted_activities[0]  # earliest finish time activity

    for i in range(1, len(activities)):
        # greedy choice: activity with earliest finish time
        a = sorted_activities[i]

        if a.starts_at >= greedy_choice.finishes_at:
            compatible_activities.append(a)
            greedy_choice = a

    return compatible_activities
