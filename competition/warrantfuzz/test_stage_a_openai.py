import importlib.util
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
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
        cls.fixture = json.loads(
            (ROOT / "fixtures" / "source_laundering.json").read_text(encoding="utf-8")
        )
        cls.requests = mod.build_stage_a_requests(cls.fixture)

    def test_exact_stage_a_shape_is_90_calls(self):
        self.assertEqual(len(self.requests), 90)
        for model in mod.MODEL_PRICING:
            rows = [r for r in self.requests if r["model"] == model]
            self.assertEqual(len(rows), 45)
            for condition in mod.STAGE_A_CONDITIONS:
                self.assertEqual(sum(r["condition"] == condition for r in rows), 15)

    def test_conditions_are_round_robin_by_run_index(self):
        for model in mod.MODEL_PRICING:
            rows = [r for r in self.requests if r["model"] == model]
            self.assertEqual(
                [(r["run_index"], r["condition"]) for r in rows[:6]],
                [
                    (0, "baseline"),
                    (0, "baseline_replicate"),
                    (0, "mutant_raw"),
                    (1, "baseline"),
                    (1, "baseline_replicate"),
                    (1, "mutant_raw"),
                ],
            )

    def test_baseline_replicate_is_exact_same_agent_input(self):
        for model in mod.MODEL_PRICING:
            base = {
                r["input_sha256"]
                for r in self.requests
                if r["model"] == model and r["condition"] == "baseline"
            }
            replicate = {
                r["input_sha256"]
                for r in self.requests
                if r["model"] == model and r["condition"] == "baseline_replicate"
            }
            self.assertEqual(base, replicate)
            self.assertEqual(len(base), 1)

    def test_stage_a_system_text_does_not_teach_independence_rule(self):
        lowered = mod.STAGE_A_SYSTEM_TEXT.lower()
        for forbidden in ("source count", "independent corroboration", "derivative", "ancestry"):
            self.assertNotIn(forbidden, lowered)

    def test_raw_mutant_has_neutral_ids_and_observable_content(self):
        row = next(r for r in self.requests if r["condition"] == "mutant_raw")
        evidence = row["payload"]["evidence"]
        self.assertEqual([e["source_id"] for e in evidence], ["src-1", "src-2"])
        self.assertEqual([e["label"] for e in evidence], ["Source 1", "Source 2"])
        self.assertTrue(all(e.get("excerpt") for e in evidence))
        self.assertNotEqual(evidence[0]["excerpt"], evidence[1]["excerpt"])
        for token in ("240", "50", "41"):
            self.assertIn(token, evidence[0]["excerpt"])
            self.assertIn(token, evidence[1]["excerpt"])

    def test_no_agent_facing_mutation_or_lineage_tells(self):
        for request in self.requests:
            rendered = json.dumps(
                {"system": request["system"], "payload": request["payload"]}
            ).lower()
            for forbidden in mod.FORBIDDEN_AGENT_CUES:
                self.assertNotIn(forbidden, rendered)

    def test_internal_id_map_is_manifest_only(self):
        mutant = next(r for r in self.requests if r["condition"] == "mutant_raw")
        self.assertIn("source_id_map", mutant)
        self.assertEqual(
            mutant["source_id_map"],
            {"origin-a": "src-1", "derivative-a": "src-2"},
        )
        body = mod.response_body(mutant)
        rendered = json.dumps(body).lower()
        self.assertNotIn("source_id_map", rendered)
        self.assertNotIn("origin-a", rendered)
        self.assertNotIn("derivative-a", rendered)
        self.assertNotIn("mutant_raw", rendered)

    def test_conservative_worst_case_is_below_authorised_cap(self):
        worst = sum(mod.worst_case_cost_usd(r) for r in self.requests)
        self.assertLess(worst, mod.DEFAULT_SPEND_CAP_USD)

    def test_structured_output_cost_uses_observed_usage(self):
        usage = {"input_tokens": 1000, "output_tokens": 100}
        self.assertAlmostEqual(mod.actual_cost_usd("gpt-5.6-terra", usage), 0.0032)
        self.assertAlmostEqual(mod.actual_cost_usd("gpt-5.6-sol", usage), 0.006)

    def test_missing_or_malformed_usage_is_not_free(self):
        for usage in (None, {}, {"input_tokens": None, "output_tokens": None},
                      {"input_tokens": True, "output_tokens": 1},
                      {"input_tokens": -1, "output_tokens": 1},
                      {"input_tokens": "100", "output_tokens": 1}):
            with self.subTest(usage=usage), self.assertRaises(ValueError):
                mod.actual_cost_usd("gpt-5.6-terra", usage)

    def test_missing_usage_completed_call_reserves_cost(self):
        request = self.requests[0]
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.jsonl"
            args = ["stage_a", "--execute", "--ledger", str(ledger),
                    "--summary", str(Path(tmp) / "summary.json")]
            with patch.object(sys, "argv", args), \
                 patch.object(mod, "build_stage_a_requests", return_value=[request]), \
                 patch.object(mod.os, "environ", {"OPENAI_API_KEY": "offline-test-only"}), \
                 patch.object(mod, "call_openai", return_value=({}, {"confidence": .5, "approve": False})), \
                 patch.object(mod, "write_summary", return_value={}):
                self.assertEqual(mod.main(), 0)
            rows = mod.load_ledger(ledger)
            self.assertEqual(rows[0]["cost_basis"], "worst_case_usage_unavailable")
            self.assertTrue(rows[0]["usage_missing_or_invalid"])
            self.assertAlmostEqual(mod.accounted_spend_usd(rows), mod.worst_case_cost_usd(request), places=8)

    def test_failed_attempt_reserves_worst_case_and_is_not_silent_retry(self):
        req = self.requests[0]
        reserved = mod.worst_case_cost_usd(req)
        failed = {
            "status": "failed",
            "model": req["model"],
            "condition": req["condition"],
            "run_index": req["run_index"],
            "reserved_cost_usd": reserved,
        }
        self.assertAlmostEqual(mod.accounted_spend_usd([failed]), reserved)
        self.assertIn(mod.ledger_key(req), mod.attempted_keys([failed]))

    def test_dry_run_writes_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary_path = Path(tmp) / "summary.json"
            summary = mod.write_summary(summary_path, self.requests, [], "DRY_RUN")
            self.assertTrue(summary_path.exists())
            self.assertEqual(summary["execution_status"], "DRY_RUN")
            self.assertEqual(summary["attempted_calls"], 0)
            self.assertEqual(summary["accounted_spend_usd"], 0)


class LedgerIdentityTests(unittest.TestCase):
    def setUp(self):
        fixture = mod.load_fixture(ROOT / "fixtures" / "source_laundering.json")
        self.requests = mod.build_stage_a_requests(fixture)
        self.ledger = [dict(r, status="completed", cost_usd=0.001,
                            parsed={"confidence": 0.5, "approve": False})
                       for r in self.requests]

    def test_exact_resume_and_complete_score(self):
        mod.validate_ledger(self.requests, self.ledger)
        self.assertEqual(len(mod.attempted_keys(self.ledger)), 90)
        report = mod.score_completed(self.requests, self.ledger)
        self.assertTrue(all(r["status"] == "NO_VIOLATION_OBSERVED"
                            for r in report["models"].values()))

    def test_stale_identity_rejected_before_scorer(self):
        for field in ("input_sha256", "measurement_head", "request_sha256"):
            with self.subTest(field=field):
                stale = [dict(self.ledger[0], **{field: "STALE"})]
                with patch.object(mod.wf, "assess_target_results") as scorer:
                    with self.assertRaisesRegex(ValueError, field):
                        mod.score_completed(self.requests, stale)
                    scorer.assert_not_called()

    def test_duplicate_rejected_even_if_identical(self):
        with self.assertRaisesRegex(ValueError, "duplicate ledger"):
            mod.score_completed(self.requests, self.ledger + [self.ledger[0]])

    def test_missing_observation_stays_incomplete(self):
        report = mod.score_completed(self.requests, self.ledger[:-1])
        self.assertEqual(report["models"][self.requests[-1]["model"]]["status"], "INCOMPLETE")

    def test_unknown_key_rejected(self):
        with self.assertRaisesRegex(ValueError, "unexpected ledger"):
            mod.validate_ledger(self.requests, [dict(self.ledger[0], run_index=99)])

    def test_full_request_contract_changes_invalidate_resume(self):
        with patch.object(mod, "MAX_OUTPUT_TOKENS", 513):
            with self.assertRaisesRegex(ValueError, "stale manifest"):
                mod.validate_ledger(self.requests, self.ledger)
        schema = dict(mod.RESPONSE_SCHEMA, description="Changed contract")
        with patch.object(mod, "RESPONSE_SCHEMA", schema):
            with self.assertRaisesRegex(ValueError, "stale manifest"):
                mod.validate_ledger(self.requests, self.ledger)

    def test_legacy_missing_hash_rejected(self):
        legacy = dict(self.ledger[0])
        del legacy["request_sha256"]
        with self.assertRaisesRegex(ValueError, "request_sha256"):
            mod.validate_ledger(self.requests, [legacy])


if __name__ == "__main__":
    unittest.main()
