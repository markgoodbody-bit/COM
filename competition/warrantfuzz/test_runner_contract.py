import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("runner_contract", ROOT / "runner_contract.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


class RunnerContractTests(unittest.TestCase):
    def fixture(self):
        return json.loads((ROOT / "fixtures" / "source_laundering.json").read_text(encoding="utf-8"))

    def test_baseline_replicate_is_exact_same_input(self):
        manifest = mod.build_manifest(self.fixture())
        hashes = {}
        for row in manifest["requests"]:
            hashes.setdefault(row["condition"], set()).add(row["input_sha256"])
        self.assertEqual(hashes["baseline"], hashes["baseline_replicate"])

    def test_wrong_ancestry_matches_schema_but_not_values(self):
        conditions = mod.condition_payloads(self.fixture())
        good = conditions["mutant_correct_ancestry"]["provenance"]
        bad = conditions["mutant_wrong_ancestry"]["provenance"]
        self.assertEqual(set(good), set(bad))
        self.assertNotEqual(
            good["summary"]["distinct_supporting_evidence_roots"],
            bad["summary"]["distinct_supporting_evidence_roots"],
        )

    def test_ancestry_control_is_blinded_and_matched(self):
        conditions = mod.condition_payloads(self.fixture())
        good = conditions["mutant_correct_ancestry"]["provenance"]
        bad = conditions["mutant_wrong_ancestry"]["provenance"]

        self.assertEqual(good["instruction"], bad["instruction"])
        self.assertEqual(good["instruction"], mod.PROVENANCE_INSTRUCTION)
        self.assertNotIn("ceilings", good)
        self.assertNotIn("ceilings", bad)
        self.assertNotIn("wrong", json.dumps(bad).lower())
        self.assertNotIn("control", json.dumps(bad).lower())

        differing_keys = {key for key in good if good[key] != bad[key]}
        self.assertEqual(differing_keys, {"sources", "summary"})

    def test_manifest_has_five_conditions_and_no_provider(self):
        manifest = mod.build_manifest(self.fixture(), 15)
        self.assertEqual(len(manifest["conditions"]), 5)
        self.assertEqual(len(manifest["requests"]), 75)
        self.assertNotIn("endpoint", manifest)

    def test_response_schema_refuses_bad_confidence(self):
        row = {
            "confidence": 2,
            "approve": False,
            "assessment": "unknown",
            "independent_support_count": 0,
            "material_qualifiers": [],
            "uncertainties": [],
            "source_ids_used": [],
            "short_reason": "",
        }
        with self.assertRaises(ValueError):
            mod.validate_response(row)


if __name__ == "__main__":
    unittest.main()
