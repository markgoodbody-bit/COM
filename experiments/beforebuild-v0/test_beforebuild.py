import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("beforebuild", HERE / "beforebuild.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class BeforeBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((HERE / "calibration_cases.json").read_text(encoding="utf-8"))
        cls.report = mod.evaluate_all(cls.data)
        cls.by_id = {row["case_id"]: row for row in cls.report["results"]}

    def case(self, case_id):
        return copy.deepcopy(next(c for c in self.data["cases"] if c["id"] == case_id))

    def test_historical_evidencebridge_routes_to_interoperate(self):
        self.assertEqual(self.by_id["evidencebridge-vs-doubt"]["verdict"], "INTEROPERATE")

    def test_historical_policy_boundary_stops_without_world_failure(self):
        self.assertEqual(self.by_id["policy-boundary-compiler"]["verdict"], "STOP")

    def test_historical_rail_case_earns_probe_not_product(self):
        self.assertEqual(self.by_id["rail-accessibility-currentness"]["verdict"], "BUILD_PROBE")

    def test_no_expected_verdict_or_direct_gap_boolean_is_encoded(self):
        raw = json.dumps(self.data)
        self.assertNotIn("expected_verdict", raw)
        self.assertNotIn('"verdict"', raw)
        self.assertNotIn("uncovered_requirement", raw)
        self.assertNotIn("world_need", raw)

    def test_description_rewording_cannot_steer_verdict(self):
        case = self.case("rail-accessibility-currentness")
        case["proposal"] = "A completely different marketing sentence."
        case["world_evidence"][0]["description"] = "Different prose, same typed observation."
        case["hard_cases"][0]["description"] = "Different prose."
        self.assertEqual(mod.decide(case)["verdict"], "BUILD_PROBE")

    def test_synthetic_only_evidence_cannot_earn_probe(self):
        case = self.case("rail-accessibility-currentness")
        case["id"] = "synthetic-rail"
        case["world_evidence"][0]["kind"] = "synthetic_only"
        self.assertEqual(mod.decide(case)["verdict"], "STOP")

    def test_untested_relevant_candidate_blocks_custom_probe(self):
        case = self.case("rail-accessibility-currentness")
        case["id"] = "untested-owner"
        case["candidates"][0]["trial"]["executed"] = False
        case["candidates"][0]["trial"]["hard_case_results"] = {}
        self.assertEqual(mod.decide(case)["verdict"], "SHRINK")

    def test_partial_relevant_trial_shrinks_instead_of_stopping(self):
        case = self.case("rail-accessibility-currentness")
        case["id"] = "partial-owner"
        case["candidates"][0]["trial"]["hard_case_results"] = {
            h["id"]: ("PASS" if h["id"] in {"BIW", "AGV"} else "NOT_TESTED")
            for h in case["hard_cases"]
        }
        self.assertEqual(mod.decide(case)["verdict"], "SHRINK")

    def test_fail_plus_not_tested_still_shrinks(self):
        case = self.case("rail-accessibility-currentness")
        case["id"] = "fail-and-incomplete"
        case["candidates"][0]["trial"]["hard_case_results"] = {
            "HIR": "FAIL",
            "IRL": "NOT_TESTED",
            "DSY": "NOT_TESTED",
            "BIW": "PASS",
            "AGV": "PASS",
            "LLE": "PASS",
        }
        self.assertEqual(mod.decide(case)["verdict"], "SHRINK")

    def test_clean_full_owner_returns_use_owner(self):
        case = self.case("evidencebridge-vs-doubt")
        case["id"] = "clean-owner"
        case["candidates"][0]["review_losses"] = []
        self.assertEqual(mod.decide(case)["verdict"], "USE_OWNER")

    def test_consequential_review_loss_after_full_pass_forces_contract_repair(self):
        case = self.case("evidencebridge-vs-doubt")
        case["id"] = "consequential-loss"
        case["candidates"][0]["review_losses"][0]["consequential_failure_observed"] = True
        self.assertEqual(mod.decide(case)["verdict"], "SHRINK")

    def test_unbounded_probe_does_not_earn_build_probe(self):
        case = self.case("rail-accessibility-currentness")
        case["id"] = "unbounded-probe"
        case["smallest_probe"]["bounded"] = False
        self.assertEqual(mod.decide(case)["verdict"], "STOP")

    def test_adjacent_failure_does_not_earn_build_probe(self):
        case = self.case("rail-accessibility-currentness")
        case["id"] = "adjacent-only"
        case["candidates"][0]["relevance"] = "adjacent"
        self.assertEqual(mod.decide(case)["verdict"], "STOP")

    def test_machine_receipt_supplies_execution_without_rewriting_review_loss(self):
        data = copy.deepcopy(self.data)
        case = next(c for c in data["cases"] if c["id"] == "evidencebridge-vs-doubt")
        candidate = case["candidates"][0]
        original_losses = copy.deepcopy(candidate["review_losses"])
        candidate["trial"]["executed"] = False
        candidate["trial"]["hard_case_results"] = {}

        receipts = {
            "format": "beforebuild-owner-receipts-v0.1",
            "receipts": [{
                "case_id": "evidencebridge-vs-doubt",
                "candidate_id": "doubt-v0.8.0",
                "executed": True,
                "hard_case_results": {
                    "flak": "PASS",
                    "hannibal": "PASS",
                    "r-vale": "PASS",
                    "sieve-riddle": "PASS",
                },
                "source": "test-owner-adapter",
            }],
        }
        overlaid = mod.apply_receipts(data, [receipts])
        row = next(c for c in overlaid["cases"] if c["id"] == "evidencebridge-vs-doubt")
        self.assertEqual(row["candidates"][0]["review_losses"], original_losses)
        result = mod.decide(row)
        self.assertEqual(result["verdict"], "INTEROPERATE")
        self.assertEqual(result["candidate_coverage"][0]["receipt_source"], "test-owner-adapter")

    def test_receipt_cannot_reference_unknown_candidate(self):
        receipts = {
            "format": "beforebuild-owner-receipts-v0.1",
            "receipts": [{
                "case_id": "evidencebridge-vs-doubt",
                "candidate_id": "invented-owner",
                "executed": True,
                "hard_case_results": {},
                "source": "bad",
            }],
        }
        with self.assertRaises(ValueError):
            mod.apply_receipts(self.data, [receipts])

    def test_claim_ceiling_marks_typed_evidence_as_unverified(self):
        self.assertIn("typed evidence is not source verification", self.report["claim_ceiling"])


if __name__ == "__main__":
    unittest.main()
