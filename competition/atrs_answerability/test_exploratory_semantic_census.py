import copy
import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("atrs_exploratory", ROOT / "exploratory_semantic_census.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)

EXPECTED_COUNTS = {
    "AMBIGUOUS": 4,
    "DATA_RIGHTS": 2,
    "EXPLANATION_ONLY": 2,
    "HELP_FEEDBACK": 41,
    "INTERNAL_REVIEW": 28,
    "IN_CHANNEL_HANDOFF": 9,
    "NO_SEPARATE": 71,
    "PLANNED_NOT_OPERATING": 1,
    "PROCESS_REFERENCE": 42,
    "PUBLIC_INITIATION": 33,
    "REFUSAL_OR_OPT_OUT": 3,
    "SELF_CORRECTION": 7,
}


def synthetic_report():
    records = []
    for i in range(152):
        present = i < 151
        records.append({
            "title": f"synthetic-{i:03d}",
            "url": f"https://example.test/{i:03d}",
            "source_sha256": hashlib.sha256(f"source-{i}".encode()).hexdigest(),
            "fields": {
                "appeals_review": {
                    "section_present": present,
                    "match_count": 1 if present else 0,
                    "contains_none_or_na_phrase": False,
                    "syntactic_contact_token_present": False,
                    "matches": ([{
                        "level": "h3",
                        "heading": "3.5 - Appeals and review",
                        "text": f"evidence {i}",
                        "characters": len(f"evidence {i}"),
                        "contains_none_or_na_phrase": False,
                        "contact_tokens": {
                            "hrefs": [], "urls_in_text": [], "emails": [], "phones": [],
                            "syntactic_contact_token_present": False,
                        },
                    }] if present else []),
                }
            },
        })
    return {"records": records}


class ExploratoryCodingStructureTests(unittest.TestCase):
    def test_label_schema_is_exact(self):
        self.assertEqual(set(mod.LABELS), set(EXPECTED_COUNTS))

    def test_all_151_indices_are_covered(self):
        covered = set()
        for label, indices in mod.LABEL_INDICES.items():
            self.assertEqual(len(indices), len(set(indices)), label)
            self.assertTrue(all(0 <= i < mod.EXPECTED_APPEALS for i in indices))
            covered.update(indices)
        self.assertEqual(covered, set(range(mod.EXPECTED_APPEALS)))

    def test_label_counts_are_frozen(self):
        actual = {label: len(indices) for label, indices in mod.LABEL_INDICES.items()}
        self.assertEqual(actual, EXPECTED_COUNTS)

    def test_status_and_ceilings_preserve_exploratory_boundary(self):
        self.assertIn("EXPLORATORY", " ".join(mod.CEILINGS))
        self.assertIn("FRAMEWORK_LABEL != VALIDATED_CLASSIFICATION", mod.CEILINGS)
        self.assertIn("LABELS_MAY_CO_OCCUR", mod.CEILINGS)
        self.assertEqual(mod.LABEL_UNIT, "proposition_within_field")
        self.assertIn("PLANNED_PROCESS != OPERATING_ROUTE", mod.CEILINGS)
        self.assertIn("ACTOR_SCOPE_MATTERS", mod.CEILINGS)

    def test_evidence_digest_rejects_changed_text(self):
        report = synthetic_report()
        appeals = mod.appeals_rows(report)
        old_title = mod.EXPECTED_APPEALS_TITLE_SEQUENCE_SHA256
        old_evidence = mod.EXPECTED_APPEALS_EVIDENCE_SHA256
        try:
            mod.EXPECTED_APPEALS_TITLE_SEQUENCE_SHA256 = hashlib.sha256(
                "\n".join(r["title"] for r in appeals).encode()
            ).hexdigest()
            mod.EXPECTED_APPEALS_EVIDENCE_SHA256 = mod.appeals_evidence_digest(report)
            mod.encode(report)
            altered = copy.deepcopy(report)
            altered["records"][0]["fields"]["appeals_review"]["matches"][0]["text"] = "changed"
            with self.assertRaises(ValueError):
                mod.encode(altered)
        finally:
            mod.EXPECTED_APPEALS_TITLE_SEQUENCE_SHA256 = old_title
            mod.EXPECTED_APPEALS_EVIDENCE_SHA256 = old_evidence


if __name__ == "__main__":
    unittest.main()
