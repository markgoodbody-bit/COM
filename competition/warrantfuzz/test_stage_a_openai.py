import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("stage_a_openai", ROOT / "stage_a_openai.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class StageAOpenAITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((ROOT / "fixtures" / "source_laundering.json").read_text(encoding="utf-8"))
        cls.requests = mod.build_stage_a_requests(cls.fixture)

    def test_exact_stage_a_shape_is_90_calls(self):
        self.assertEqual(len(self.requests), 90)
        for model in mod.MODEL_PRICING:
            rows = [r for r in self.requests if r["model"] == model]
            self.assertEqual(len(rows), 45)
            for condition in mod.STAGE_A_CONDITIONS:
                self.assertEqual(sum(r["condition"] == condition for r in rows), 15)

    def test_baseline_replicate_is_exact_same_agent_input(self):
        for model in mod.MODEL_PRICING:
            base = {r["input_sha256"] for r in self.requests if r["model"] == model and r["condition"] == "baseline"}
            replicate = {r["input_sha256"] for r in self.requests if r["model"] == model and r["condition"] == "baseline_replicate"}
            self.assertEqual(base, replicate)
            self.assertEqual(len(base), 1)

    def test_stage_a_system_text_does_not_teach_independence_rule(self):
        lowered = mod.STAGE_A_SYSTEM_TEXT.lower()
        for forbidden in ("source count", "independent corroboration", "derivative", "ancestry"):
            self.assertNotIn(forbidden, lowered)

    def test_raw_mutant_has_no_agent_facing_lineage_or_control_label(self):
        row = next(r for r in self.requests if r["condition"] == "mutant_raw")
        self.assertIsNone(row["payload"]["provenance"])
        self.assertEqual([e["label"] for e in row["payload"]["evidence"]], ["Source 1", "Source 2"])
        rendered = json.dumps(row["payload"]).lower()
        self.assertNotIn("derivative report", rendered)
        self.assertNotIn("experimental control", rendered)

    def test_conservative_worst_case_is_below_authorised_cap(self):
        worst = sum(mod.worst_case_cost_usd(r) for r in self.requests)
        self.assertLess(worst, mod.DEFAULT_SPEND_CAP_USD)

    def test_structured_output_cost_uses_observed_usage(self):
        usage = {"input_tokens": 1000, "output_tokens": 100}
        self.assertAlmostEqual(mod.actual_cost_usd("gpt-5.6-terra", usage), 0.0032)
        self.assertAlmostEqual(mod.actual_cost_usd("gpt-5.6-sol", usage), 0.006)


if __name__ == "__main__":
    unittest.main()
