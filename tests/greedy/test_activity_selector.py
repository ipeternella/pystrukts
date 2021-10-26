"""
Module with tests for fibonacci computation problems.
"""
import unittest

from pystrukts.greedy.activity_selector import Activity
from pystrukts.greedy.activity_selector import select_compatible_activities


class ActivitySelectorGreedyTestSuite(unittest.TestCase):
    """
    Activity selector problem test suite.
    """

    def test_should_select_maximum_compatible_activities(self):
        """
        Should select the maximum set of compatible activities.
        """
        # arrange
        activities = self.build_four_activities()

        # act
        compatible_activities = select_compatible_activities(activities)

        # assert
        expected_activities = [Activity(1, 4), Activity(5, 7)]
        self.assertEqual(compatible_activities, expected_activities)

    def test_should_select_maximum_compatible_activities_longer(self):
        """
        Should select the maximum set of compatible activities for longer list of activities.
        """
        # arrange
        activities = self.build_ten_activities()

        # act
        compatible_activities = select_compatible_activities(activities)

        # assert
        expected_activities = [Activity(1, 4), Activity(5, 7), Activity(8, 11), Activity(12, 16)]
        self.assertEqual(compatible_activities, expected_activities)

    def build_four_activities(self):
        return [
            Activity(starts_at=1, finishes_at=4),
            Activity(starts_at=3, finishes_at=5),
            Activity(starts_at=0, finishes_at=6),
            Activity(starts_at=5, finishes_at=7),
        ]

    def build_ten_activities(self):
        return [
            Activity(starts_at=1, finishes_at=4),
            Activity(starts_at=3, finishes_at=5),
            Activity(starts_at=0, finishes_at=6),
            Activity(starts_at=5, finishes_at=7),
            Activity(starts_at=3, finishes_at=9),
            Activity(starts_at=5, finishes_at=9),
            Activity(starts_at=6, finishes_at=10),
            Activity(starts_at=8, finishes_at=11),
            Activity(starts_at=8, finishes_at=12),
            Activity(starts_at=2, finishes_at=14),
            Activity(starts_at=12, finishes_at=16),
        ]
