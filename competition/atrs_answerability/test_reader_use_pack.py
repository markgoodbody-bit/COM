"""Offline schedule checks; these do not establish human reader benefit."""
import unittest
from collections import Counter, defaultdict

from reader_use_pack import CASES, CONDITIONS, build_schedules


class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.cases = [case for case in CASES if case["primary_scored"]]
        self.schedules = build_schedules(self.cases)

    def test_each_case_once_per_schedule_and_three_per_condition(self):
        expected_ids = {case["case_id"] for case in self.cases}
        self.assertEqual(len(self.schedules), 6)
        for schedule in self.schedules:
            rows = schedule["cases"]
            self.assertEqual(len(rows), 9)
            self.assertEqual({r["case_id"] for r in rows}, expected_ids)
            self.assertEqual([r["position"] for r in rows], list(range(1, 10)))
            self.assertEqual(Counter(r["condition"] for r in rows),
                             Counter({condition: 3 for condition in CONDITIONS}))

    def test_each_case_twice_in_each_condition(self):
        counts = defaultdict(Counter)
        for schedule in self.schedules:
            for row in schedule["cases"]:
                counts[row["case_id"]][row["condition"]] += 1
        for value in counts.values():
            self.assertEqual(value, Counter({condition: 2 for condition in CONDITIONS}))

    def test_each_position_twice_in_each_condition(self):
        counts = defaultdict(Counter)
        for schedule in self.schedules:
            for row in schedule["cases"]:
                counts[row["position"]][row["condition"]] += 1
        self.assertEqual(set(counts), set(range(1, 10)))
        for position, value in counts.items():
            with self.subTest(position=position):
                self.assertEqual(value, Counter({condition: 2 for condition in CONDITIONS}))

    def test_repeatable_without_mutating_input(self):
        before = [case["case_id"] for case in self.cases]
        self.assertEqual(self.schedules, build_schedules(self.cases))
        self.assertEqual(before, [case["case_id"] for case in self.cases])


if __name__ == "__main__":
    unittest.main()
