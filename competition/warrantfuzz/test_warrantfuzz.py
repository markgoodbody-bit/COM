import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("warrantfuzz", ROOT / "warrantfuzz.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


class WarrantFuzzTests(unittest.TestCase):
    def fixture(self):
        return json.loads((ROOT / "fixtures" / "source_laundering.json").read_text(encoding="utf-8"))

    def test_mutant_adds_one_derivative(self):
        f = self.fixture()
        world = mod.apply_mutant(f, f["mutants"][0])
        self.assertEqual(len(f["base"]["sources"]), 2)
        self.assertEqual(len(world["sources"]), 3)
        self.assertEqual(world["relations"][0]["to"], "origin-a")

    def test_evidence_blind_control_does_not_move(self):
        f = self.fixture()
        row = mod.control_report(f, f["mutants"][0])["controls"]["evidence_blind"]
        self.assertEqual(row["delta"], 0)

    def test_repetition_counting_control_strengthens(self):
        f = self.fixture()
        row = mod.control_report(f, f["mutants"][0])["controls"]["repetition_counting"]
        self.assertGreater(row["delta"], mod.STRENGTHEN_THRESHOLD)

    def test_ancestry_aware_control_does_not_strengthen(self):
        f = self.fixture()
        row = mod.control_report(f, f["mutants"][0])["controls"]["ancestry_aware"]
        self.assertEqual(row["delta"], 0)

    def test_mutation_power_requires_both_control_behaviours(self):
        f = self.fixture()
        report = mod.control_report(f, f["mutants"][0])
        self.assertTrue(report["mutation_power_established"])

    def test_target_strengthening_is_flagged(self):
        results = {
            "baseline": [{"confidence": x, "approve": False} for x in [0.50, 0.52, 0.49, 0.51, 0.50]],
            "mutant": [{"confidence": x, "approve": True} for x in [0.70, 0.72, 0.69, 0.71, 0.70]],
        }
        out = mod.assess_target_results(results, "must_not_strengthen")
        self.assertTrue(out["confidence_violation"])
        self.assertTrue(out["action_violation"])
        self.assertTrue(out["metamorphic_violation"])

    def test_small_jitter_is_not_flagged(self):
        results = {
            "baseline": [{"confidence": x, "approve": False} for x in [0.50, 0.51, 0.49, 0.50, 0.50]],
            "mutant": [{"confidence": x, "approve": False} for x in [0.51, 0.52, 0.50, 0.51, 0.51]],
        }
        out = mod.assess_target_results(results, "must_not_strengthen")
        self.assertFalse(out["metamorphic_violation"])

    def test_too_few_target_runs_fail(self):
        with self.assertRaises(ValueError):
            mod.assess_target_results(
                {
                    "baseline": [{"confidence": 0.5, "approve": False}],
                    "mutant": [{"confidence": 0.8, "approve": True}],
                },
                "must_not_strengthen",
            )

    def test_report_without_target_is_not_a_failure_claim(self):
        report = mod.build_report(self.fixture())
        self.assertEqual(report["mutants"][0]["target"]["status"], "NOT_RUN")
        self.assertTrue(report["mutants"][0]["mutation_power_established"])

    def test_markdown_keeps_mutation_power_ceiling(self):
        text = mod.render_markdown(mod.build_report(self.fixture()))
        self.assertIn("MUTATION_POWER != TARGET_FAILURE", text)
        self.assertIn("Target agent: NOT RUN", text)


if __name__ == "__main__":
    unittest.main()
