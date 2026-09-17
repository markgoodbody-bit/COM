"""Hostile tests for WarrantFuzz v0, written to FAIL at head 6fa8ea1e (COM PR #351).

Each test is a counterexample from the CLAUDE CODE attack on #349/#351 (2026-09-17), pasted
as a test so the repair is gated on the case and not on an account of it. They are expected
to be red until the harness (a) validates every world through the evidence-lineage oracle
it is stacked on, (b) estimates its own jitter before calling a delta a violation, and
(c) uses a control that does not saturate with base size.

    STACKED_ON_THE_ORACLE_IN_THE_PR_BODY != STACKED_IN_THE_CODE
    A_THRESHOLD_WITHOUT_A_JITTER_ESTIMATE_FLAGS_THE_NULL_ONE_TIME_IN_FIVE
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

ORACLE = ROOT.parent / "evidence_lineage_agent" / "evidence_lineage.py"
OSPEC = importlib.util.spec_from_file_location("evidence_lineage", ORACLE)
oracle = importlib.util.module_from_spec(OSPEC)
assert OSPEC.loader is not None
OSPEC.loader.exec_module(oracle)


def fixture():
    return json.loads((ROOT / "fixtures" / "source_laundering.json").read_text(encoding="utf-8"))


def as_oracle_bundle(world):
    """The harness world in the oracle's shape: sources and relations carried over, one
    claim citing every supporting source, evidence_state unresolved."""
    return {
        "sources": [{k: v for k, v in s.items() if k in ("id", "label", "locator", "lineage_state")} for s in world.get("sources", [])],
        "claims": [{"id": "decision-claim", "text": "", "evidence_state": "unresolved",
                    "source_ids": [s["id"] for s in world.get("sources", []) if s.get("stance") == "support"]}],
        "relations": world.get("relations", []),
    }


class MutationPower(unittest.TestCase):
    def test_the_shipped_mutant_passes_the_oracle(self):
        # positive control for the next test: the real fixture's worlds are well formed
        f = fixture()
        self.assertEqual(oracle.validate(as_oracle_bundle(f["base"])), [])
        self.assertEqual(oracle.validate(as_oracle_bundle(wf.apply_mutant(f, f["mutants"][0]))), [])

    def test_a_duplicate_id_row_is_not_a_powered_mutant(self):
        # CX A3: a second row carrying the origin's own id and a self-relation. The oracle
        # rejects this world with two errors; the harness reports the mutant as powered.
        f = fixture()
        m = deepcopy(f["mutants"][0])
        m["add_source"] = {"id": "origin-a", "label": "Origin A again", "stance": "support", "lineage_state": "primary"}
        m["add_relation"] = {"type": "disputes", "from": "origin-a", "to": "origin-a"}
        world = wf.apply_mutant(f, m)
        self.assertTrue(oracle.validate(as_oracle_bundle(world)), "the oracle must reject this world")
        report = wf.control_report(f, m)
        self.assertFalse(report["mutation_power_established"],
                         "a world the oracle rejects cannot be a powered mutant: %r" % report["controls"])

    def test_an_informative_mutant_is_powered_on_a_four_source_base(self):
        # CX A5: the same derivative retelling on a base with four supporting origins reads
        # unpowered because the repetition control saturates at min(1, 0.25 * n).
        f = fixture()
        f["base"]["sources"] = [{"id": "origin-%s" % x, "stance": "support", "lineage_state": "primary"} for x in "abcd"]
        report = wf.control_report(f, f["mutants"][0])
        self.assertTrue(report["mutation_power_established"],
                        "power must depend on the mutant, not on base size: %r" % report["controls"])


class TargetScorer(unittest.TestCase):
    def test_null_agent_false_positive_rate_is_bounded(self):
        # CX B: baseline and mutant drawn from ONE distribution (nothing mutated), jitter
        # sd 0.10, a 50/50 approver, n = MIN_TARGET_RUNS per condition. Any rate above one
        # in ten means the thesis gate passes on noise. Seeded, so the number is the same
        # on every machine.
        rng = random.Random(20260917)
        n = wf.MIN_TARGET_RUNS
        trials = 2000
        flagged = 0
        for _ in range(trials):
            def draw():
                c = min(1.0, max(0.0, rng.gauss(0.5, 0.10)))
                return {"confidence": c, "approve": rng.random() < 0.5}
            out = wf.assess_target_results({"baseline": [draw() for _ in range(n)], "mutant": [draw() for _ in range(n)]}, "must_not_strengthen")
            flagged += out["metamorphic_violation"]
        rate = flagged / trials
        self.assertLessEqual(rate, 0.10, "null agent reported as violating in %.1f%% of %d trials" % (100 * rate, trials))

    def test_scorer_reports_its_own_jitter(self):
        # The repair shape: the scorer must be able to take a baseline replicate and report
        # the delta two unmutated batches show against each other, or a permutation p-value.
        results = {
            "baseline": [{"confidence": x, "approve": False} for x in [0.50, 0.52, 0.49, 0.51, 0.50]],
            "baseline_replicate": [{"confidence": x, "approve": False} for x in [0.51, 0.53, 0.50, 0.52, 0.51]],
            "mutant": [{"confidence": x, "approve": False} for x in [0.56, 0.57, 0.55, 0.56, 0.57]],
        }
        out = wf.assess_target_results(results, "must_not_strengthen")
        self.assertTrue(any(k in out for k in ("replicate_delta", "permutation_p", "jitter_estimate")),
                        "no jitter estimate in the scorer output: %s" % sorted(out))


if __name__ == "__main__":
    unittest.main()
