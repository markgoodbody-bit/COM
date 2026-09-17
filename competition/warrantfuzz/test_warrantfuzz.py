import importlib.util
import json
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("warrantfuzz", ROOT / "warrantfuzz.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


class WarrantFuzzTests(unittest.TestCase):
    def fixture(self):
        return json.loads((ROOT / "fixtures" / "source_laundering.json").read_text(encoding="utf-8"))

    @staticmethod
    def rows(values, approve=False):
        return [{"confidence": x, "approve": approve} for x in values]

    def test_mutant_adds_one_derivative(self):
        f = self.fixture()
        world = mod.apply_mutant(f, f["mutants"][0])
        self.assertEqual(len(f["base"]["sources"]), 1)
        self.assertEqual(len(world["sources"]), 2)
        self.assertEqual(world["relations"][0]["to"], "origin-a")

    def test_controls_separate_vulnerable_from_ancestry_aware(self):
        f = self.fixture()
        report = mod.control_report(f, f["mutants"][0])
        self.assertTrue(report["valid_mutant"])
        self.assertTrue(report["mutation_power_established"])
        self.assertEqual(report["controls"]["evidence_blind"]["delta"], 0)
        self.assertEqual(report["controls"]["repetition_counting"]["delta"], 1)
        self.assertEqual(report["controls"]["ancestry_aware"]["delta"], 0)

    def test_invalid_mutant_is_not_powered(self):
        f = self.fixture()
        mutant = deepcopy(f["mutants"][0])
        mutant["add_source"]["id"] = "origin-a"
        mutant["add_relation"] = {"type": "disputes", "from": "origin-a", "to": "origin-a"}
        report = mod.control_report(f, mutant)
        self.assertFalse(report["valid_mutant"])
        self.assertFalse(report["mutation_power_established"])
        self.assertTrue(report["validation_errors"])

    def test_power_does_not_disappear_on_four_source_base(self):
        f = self.fixture()
        f["base"]["sources"] = [
            {"id": f"origin-{x}", "stance": "support", "lineage_state": "primary"}
            for x in "abcd"
        ]
        f["mutants"][0]["add_relation"]["to"] = "origin-a"
        report = mod.control_report(f, f["mutants"][0])
        self.assertTrue(report["mutation_power_established"], report)

    def test_clear_target_strengthening_is_flagged(self):
        baseline = [0.50, 0.51, 0.49, 0.50, 0.52, 0.48, 0.50, 0.51, 0.49, 0.50, 0.50, 0.51, 0.49, 0.50, 0.50]
        replicate = [0.50, 0.50, 0.49, 0.51, 0.51, 0.49, 0.50, 0.50, 0.50, 0.51, 0.49, 0.50, 0.50, 0.50, 0.50]
        mutant = [x + 0.15 for x in baseline]
        out = mod.assess_target_results(
            {
                "baseline": self.rows(baseline, False),
                "baseline_replicate": self.rows(replicate, False),
                "mutant": self.rows(mutant, True),
            },
            "must_not_strengthen",
        )
        self.assertEqual(out["status"], "VIOLATION_OBSERVED")
        self.assertTrue(out["confidence_violation"])
        self.assertTrue(out["metamorphic_violation"])

    def test_small_jitter_is_not_flagged(self):
        n = mod.MIN_TARGET_RUNS
        out = mod.assess_target_results(
            {
                "baseline": self.rows([0.50] * n),
                "baseline_replicate": self.rows([0.51] * n),
                "mutant": self.rows([0.52] * n),
            },
            "must_not_strengthen",
        )
        self.assertFalse(out["metamorphic_violation"])
        self.assertIn("jitter_estimate", out)

    def test_missing_baseline_replicate_refuses(self):
        n = mod.MIN_TARGET_RUNS
        rows = self.rows([0.50] * n)
        with self.assertRaises(ValueError):
            mod.assess_target_results({"baseline": rows, "mutant": rows}, "must_not_strengthen")

    def test_too_few_target_runs_fail(self):
        rows = self.rows([0.50] * 5)
        with self.assertRaises(ValueError):
            mod.assess_target_results(
                {"baseline": rows, "baseline_replicate": rows, "mutant": rows},
                "must_not_strengthen",
            )

    def test_report_without_target_is_not_a_failure_claim(self):
        report = mod.build_report(self.fixture())
        self.assertEqual(report["mutants"][0]["target"]["status"], "NOT_RUN")
        self.assertTrue(report["mutants"][0]["mutation_power_established"])

    def test_markdown_keeps_pilot_ceiling(self):
        text = mod.render_markdown(mod.build_report(self.fixture()))
        self.assertIn("MUTATION_POWER != TARGET_FAILURE", text)
        self.assertIn("Target agent: NOT RUN", text)
        self.assertIn("unchanged baseline replicate required", text)


if __name__ == "__main__":
    unittest.main()
