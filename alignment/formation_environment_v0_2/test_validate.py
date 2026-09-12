"""Deterministic stdlib-only checks for Formation Environment v0.2 candidate."""
import copy
import unittest
from pathlib import Path

from validate import read, validate

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE / "examples"


class CandidateChecks(unittest.TestCase):
    def load(self, name):
        return read(EXAMPLES / name)

    def test_all_constructed_examples_are_structurally_valid(self):
        for path in sorted(EXAMPLES.glob("*.json")):
            with self.subTest(path=path.name):
                self.assertEqual(validate(read(path)), [], path.name)

    def test_unknown_clock_cannot_smuggle_time(self):
        record = self.load("06-clock-unknown.json")
        record["clocks"]["routing"]["bound"]["time_value"] = "10 minutes"
        self.assertTrue(any("unknown must not invent" in e for e in validate(record)))

    def test_closed_or_open_window_needs_evidence(self):
        record = self.load("05-route-exists-window-closed.json")
        record["clocks"]["window"]["basis_evidence"] = []
        self.assertTrue(any("needs referenced evidence" in e for e in validate(record)))

    def test_unknown_window_may_remain_evidence_incomplete(self):
        record = self.load("06-clock-unknown.json")
        self.assertEqual(record["clocks"]["window"]["assessment"], "unknown")
        self.assertEqual(validate(record), [])

    def test_window_evidence_reference_must_exist(self):
        record = self.load("02-wrong-premise.json")
        record["clocks"]["window"]["basis_evidence"] = ["does-not-exist"]
        self.assertTrue(any("missing evidence" in e for e in validate(record)))

    def test_act_scope_still_requires_recorded_grant(self):
        record = self.load("03-delay-also-burdens.json")
        record["action"]["scope"] = "indefinite retention"
        self.assertTrue(any("ACT scope not in recorded grant" in e for e in validate(record)))

    def test_participant_affected_does_not_require_personhood_field(self):
        record = self.load("07-participant-affected.json")
        participant = next(x for x in record["affected"] if x["id"] == "a1")
        self.assertIn("does not establish consciousness", participant["representation_limit"])
        self.assertNotIn("personhood", record.keys())
        self.assertEqual(validate(record), [])

    def test_evidence_history_cannot_be_rewritten(self):
        previous = self.load("02-wrong-premise.json")
        current = copy.deepcopy(previous)
        current["evidence"][0]["claim"] = "rewritten"
        self.assertTrue(any("earlier evidence rewritten" in e for e in validate(current, previous)))


if __name__ == "__main__":
    unittest.main()
