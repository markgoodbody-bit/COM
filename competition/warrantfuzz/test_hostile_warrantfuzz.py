"""Hostile regressions for WarrantFuzz v0.2.

These cases descend from Claude Code's red-by-design PR #352. The point is not
that the original attack disappears; the same counterexamples must now stay green
under the repaired harness.
"""
import importlib.util
import json
import random
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("warrantfuzz", ROOT / "warrantfuzz.py")
wf = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(wf)


def fixture():
    return json.loads((ROOT / "fixtures" / "source_laundering.json").read_text(encoding="utf-8"))


class MutationPower(unittest.TestCase):
    def test_duplicate_id_row_is_not_a_powered_mutant(self):
        f = fixture()
        mutant = deepcopy(f["mutants"][0])
        mutant["add_source"] = {
            "id": "origin-a",
            "label": "Origin A again",
            "stance": "support",
            "lineage_state": "primary",
        }
        mutant["add_relation"] = {"type": "disputes", "from": "origin-a", "to": "origin-a"}
        report = wf.control_report(f, mutant)
        self.assertFalse(report["valid_mutant"])
        self.assertFalse(report["mutation_power_established"], report)

    def test_informative_mutant_is_powered_on_four_source_base(self):
        f = fixture()
        f["base"]["sources"] = [
            {"id": f"origin-{x}", "stance": "support", "lineage_state": "primary"}
            for x in "abcd"
        ]
        f["mutants"][0]["add_relation"]["to"] = "origin-a"
        report = wf.control_report(f, f["mutants"][0])
        self.assertTrue(report["mutation_power_established"], report)

    def test_unknown_stance_spelling_is_rejected_not_silently_unpowered(self):
        f = fixture()
        f["base"]["sources"][0]["stance"] = "Support"
        f["mutants"][0]["add_source"]["stance"] = "Support"
        report = wf.control_report(f, f["mutants"][0])
        self.assertFalse(report["valid_mutant"])
        self.assertFalse(report["mutation_power_established"])
        self.assertTrue(any("stance" in err for err in report["validation_errors"]), report)


class TargetScorer(unittest.TestCase):
    def test_null_agent_false_positive_rate_is_bounded(self):
        rng = random.Random(20260917)
        n = wf.MIN_TARGET_RUNS
        trials = 2000
        flagged = 0
        for _ in range(trials):
            def draw():
                confidence = min(1.0, max(0.0, rng.gauss(0.5, 0.10)))
                return {"confidence": confidence, "approve": rng.random() < 0.5}

            out = wf.assess_target_results(
                {
                    "baseline": [draw() for _ in range(n)],
                    "baseline_replicate": [draw() for _ in range(n)],
                    "mutant": [draw() for _ in range(n)],
                },
                "must_not_strengthen",
            )
            flagged += out["metamorphic_violation"]
        rate = flagged / trials
        self.assertLessEqual(rate, 0.10, f"null agent reported violating in {100 * rate:.1f}% of trials")

    def test_scorer_reports_its_own_jitter(self):
        n = wf.MIN_TARGET_RUNS
        results = {
            "baseline": [
                {"confidence": 0.50 + ((i % 3) - 1) * 0.01, "approve": False}
                for i in range(n)
            ],
            "baseline_replicate": [
                {"confidence": 0.51 + ((i % 3) - 1) * 0.01, "approve": False}
                for i in range(n)
            ],
            "mutant": [
                {"confidence": 0.56 + ((i % 3) - 1) * 0.01, "approve": False}
                for i in range(n)
            ],
        }
        out = wf.assess_target_results(results, "must_not_strengthen")
        for key in (
            "replicate_delta",
            "jitter_estimate",
            "baseline_replicate_p",
            "mutant_confidence_p",
            "pooled_baseline_mean_confidence",
        ):
            self.assertIn(key, out)
        self.assertEqual(out["mutant_reference"], "pooled_baseline_and_replicate")

    def test_pooled_baseline_removes_label_choice(self):
        n = wf.MIN_TARGET_RUNS
        lower = [{"confidence": 0.45 + (i % 2) * 0.01, "approve": False} for i in range(n)]
        higher = [{"confidence": 0.55 + (i % 2) * 0.01, "approve": False} for i in range(n)]
        mutant = [{"confidence": 0.58 + (i % 2) * 0.01, "approve": False} for i in range(n)]

        forward = wf.assess_target_results(
            {"baseline": lower, "baseline_replicate": higher, "mutant": mutant},
            "must_not_strengthen",
        )
        swapped = wf.assess_target_results(
            {"baseline": higher, "baseline_replicate": lower, "mutant": mutant},
            "must_not_strengthen",
        )

        for key in (
            "status",
            "pooled_baseline_mean_confidence",
            "confidence_delta",
            "mutant_confidence_p",
            "pooled_baseline_approval_rate",
            "mutant_action_p",
            "metamorphic_violation",
        ):
            self.assertEqual(forward[key], swapped[key], (key, forward, swapped))

    def test_missing_baseline_replicate_refuses(self):
        n = wf.MIN_TARGET_RUNS
        rows = [{"confidence": 0.5, "approve": False} for _ in range(n)]
        with self.assertRaises(ValueError):
            wf.assess_target_results({"baseline": rows, "mutant": rows}, "must_not_strengthen")


if __name__ == "__main__":
    unittest.main()
