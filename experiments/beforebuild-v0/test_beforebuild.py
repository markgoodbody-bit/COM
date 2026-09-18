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

    def test_historical_evidencebridge_routes_to_interoperate(self):
        self.assertEqual(self.by_id["evidencebridge-vs-doubt"]["verdict"], "INTEROPERATE")

    def test_historical_policy_boundary_stops_without_world_failure(self):
        self.assertEqual(self.by_id["policy-boundary-compiler"]["verdict"], "STOP")

    def test_historical_rail_case_earns_bounded_build(self):
        self.assertEqual(self.by_id["rail-accessibility-currentness"]["verdict"], "BUILD")

    def test_no_expected_verdict_is_encoded_in_fixture(self):
        raw = json.dumps(self.data)
        self.assertNotIn("expected_verdict", raw)
        self.assertNotIn('"verdict"', raw)

    def test_no_world_need_beats_attractive_build(self):
        case = copy.deepcopy(next(c for c in self.data["cases"] if c["id"] == "rail-accessibility-currentness"))
        case["id"] = "no-world-need"
        case["world_need"]["observed"] = False
        self.assertEqual(mod.decide(case)["verdict"], "STOP")

    def test_exact_owner_must_be_tested_before_build(self):
        case = copy.deepcopy(next(c for c in self.data["cases"] if c["id"] == "rail-accessibility-currentness"))
        case["id"] = "exact-owner-untested"
        case["owners"][0]["exact_function_match"] = True
        case["owners"][0]["trial"]["executed"] = False
        case["owners"][0]["trial"]["hard_case_results"] = {}
        self.assertEqual(mod.decide(case)["verdict"], "SHRINK")

    def test_clean_full_owner_returns_use_owner(self):
        case = copy.deepcopy(next(c for c in self.data["cases"] if c["id"] == "evidencebridge-vs-doubt"))
        case["id"] = "clean-owner"
        case["owners"][0]["trial"]["material_losses"] = []
        self.assertEqual(mod.decide(case)["verdict"], "USE_OWNER")

    def test_consequential_loss_after_full_pass_forces_contract_repair(self):
        case = copy.deepcopy(next(c for c in self.data["cases"] if c["id"] == "evidencebridge-vs-doubt"))
        case["id"] = "consequential-loss"
        case["owners"][0]["trial"]["material_losses"][0]["consequential_failure_observed"] = True
        self.assertEqual(mod.decide(case)["verdict"], "SHRINK")

    def test_unbounded_build_does_not_earn_build(self):
        case = copy.deepcopy(next(c for c in self.data["cases"] if c["id"] == "rail-accessibility-currentness"))
        case["id"] = "unbounded-build"
        case["smallest_build"]["bounded"] = False
        self.assertEqual(mod.decide(case)["verdict"], "STOP")

    def test_claim_ceiling_remains_historical_calibration(self):
        self.assertIn("historical calibration", self.report["claim_ceiling"])


if __name__ == "__main__":
    unittest.main()
