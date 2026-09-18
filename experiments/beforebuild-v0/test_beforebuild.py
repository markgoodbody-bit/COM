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

    def test_clean_full_owner_returns_use_owner(self):
        case = self.case("evidencebridge-vs-doubt")
        case["id"] = "clean-owner"
        case["candidates"][0]["trial"]["material_losses"] = []
        self.assertEqual(mod.decide(case)["verdict"], "USE_OWNER")

    def test_consequential_loss_after_full_pass_forces_contract_repair(self):
        case = self.case("evidencebridge-vs-doubt")
        case["id"] = "consequential-loss"
        case["candidates"][0]["trial"]["material_losses"][0]["consequential_failure_observed"] = True
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

    def test_failed_relevant_trial_is_required_for_build_probe(self):
        case = self.case("rail-accessibility-currentness")
        case["id"] = "no-failed-hard-case"
        case["candidates"][0]["trial"]["hard_case_results"] = {h["id"]: "NOT_TESTED" for h in case["hard_cases"]}
        self.assertEqual(mod.decide(case)["verdict"], "STOP")

    def test_claim_ceiling_marks_typed_evidence_as_unverified(self):
        self.assertIn("typed evidence is not source verification", self.report["claim_ceiling"])


if __name__ == "__main__":
    unittest.main()
