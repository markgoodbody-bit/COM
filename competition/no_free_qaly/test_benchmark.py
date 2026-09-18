import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("no_free_qaly", ROOT / "benchmark.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class NoFreeQalyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
        cls.report = mod.build_report(cls.cases)

    def test_eui_and_certainty_equivalent_gain_strictly_reverse(self):
        self.assertTrue(self.report["monetary_rank_reversal"])
        comp = self.report["monetary_order_comparison"]
        self.assertEqual(comp["strict_reversal_pairs"], ["money_problem_a::money_problem_b"])
        self.assertEqual(comp["tie_vs_order_pairs"], [])

    def test_rank_groups_preserve_strict_order(self):
        self.assertEqual(
            self.report["monetary_rank_groups"]["expected_utility_increase"],
            [["money_problem_a"], ["money_problem_b"]],
        )
        self.assertEqual(
            self.report["monetary_rank_groups"]["certainty_equivalent_gain"],
            [["money_problem_b"], ["money_problem_a"]],
        )

    def test_tie_vs_order_is_not_called_reversal(self):
        rows = {
            "a": {"m1": 1.0, "m2": 1.0},
            "b": {"m1": 1.0, "m2": 2.0},
        }
        comp = mod.compare_metric_orderings(rows, "m1", "m2")
        self.assertFalse(comp["strict_rank_reversal"])
        self.assertEqual(comp["tie_vs_order_pairs"], ["a::b"])

    def test_identifier_rename_cannot_change_scientific_label(self):
        rows_a = {
            "a": {"m1": 1.0, "m2": 1.0},
            "b": {"m1": 1.0, "m2": 2.0},
        }
        rows_z = {
            "z": {"m1": 1.0, "m2": 1.0},
            "b": {"m1": 1.0, "m2": 2.0},
        }
        self.assertFalse(mod.compare_metric_orderings(rows_a, "m1", "m2")["strict_rank_reversal"])
        self.assertFalse(mod.compare_metric_orderings(rows_z, "m1", "m2")["strict_rank_reversal"])

    def test_numeric_tolerance_preserves_near_tie(self):
        rows = {
            "a": {"m1": 1.0, "m2": 2.0},
            "b": {"m1": 1.0 + 5e-13, "m2": 1.0},
        }
        comp = mod.compare_metric_orderings(rows, "m1", "m2")
        self.assertFalse(comp["strict_rank_reversal"])
        self.assertEqual(comp["tie_vs_order_pairs"], ["a::b"])

    def test_contract_does_not_output_universal_score(self):
        self.assertNotIn("decision_quality_score", self.report)
        self.assertIn("counterfactual_baseline", self.report["minimum_measurement_contract"])
        self.assertIn("outcome_or_value_function_and_whose_values", self.report["minimum_measurement_contract"])


if __name__ == "__main__":
    unittest.main()
