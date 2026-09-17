import importlib.util
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("reader_use_v3", ROOT / "reader_use_pack_v3.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class ReaderUsePackV3Tests(unittest.TestCase):
    def setUp(self):
        self.scored = [c for c in mod.base.CASES if c["primary_scored"]]

    def test_schedules_balance_case_and_position_by_condition(self):
        schedules = mod.build_schedules(self.scored)
        self.assertEqual(len(schedules), 6)
        mod._assert_balanced(schedules, self.scored)
        for schedule in schedules:
            self.assertEqual(len(schedule["cases"]), 9)
            self.assertEqual({x["position"] for x in schedule["cases"]}, set(range(1, 10)))
            counts = {condition: 0 for condition in mod.CONDITIONS}
            for item in schedule["cases"]:
                counts[item["condition"]] += 1
            self.assertEqual(counts, {"FULL": 3, "EXCERPT": 3, "LENS": 3})

    def test_two_fixed_orders_with_three_rotations_each(self):
        schedules = mod.build_schedules(self.scored)
        order = lambda schedule: [x["case_id"] for x in schedule["cases"]]
        self.assertEqual(order(schedules[0]), order(schedules[1]))
        self.assertEqual(order(schedules[1]), order(schedules[2]))
        self.assertEqual(order(schedules[3]), order(schedules[4]))
        self.assertEqual(order(schedules[4]), order(schedules[5]))
        self.assertNotEqual(order(schedules[0]), order(schedules[3]))

    def test_every_scored_case_has_route_linked_key(self):
        scored_ids = {c["case_id"] for c in self.scored}
        self.assertEqual(set(mod.ROUTE_BUNDLES), scored_ids)
        for case_id, bundles in mod.ROUTE_BUNDLES.items():
            self.assertTrue(bundles, case_id)
            for bundle in bundles:
                self.assertEqual(
                    set(bundle),
                    {"next_step", "actor", "channel", "object_layer", "status"},
                    case_id,
                )

    def test_ns_and_i_complaints_route_does_not_borrow_human_handoff_channel(self):
        bundles = mod.ROUTE_BUNDLES["nsi-polyai"]
        complaint = next(b for b in bundles if "complaints process" in b["next_step"])
        self.assertEqual(complaint["channel"], "NOT STATED")
        self.assertNotEqual(complaint["channel"], "in-channel human-agent request")

    def test_emitted_key_has_one_route_linked_scoring_source(self):
        # Exercise serialization, not just the ROUTE_BUNDLES constant. Synthetic
        # validated rows avoid network/source dependencies in this regression.
        rows = [(case, {"fields": {"appeals_review": {
            "section_present": case["primary_scored"], "matches": []
        }}}, b"") for case in mod.base.CASES]
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(mod.base, "validate", return_value=rows), \
                 patch.object(mod.base, "full_surface", return_value=b"fixture"):
                _, key = mod.build({}, Path(directory), Path(directory))
        for case in key["cases"]:
            self.assertNotIn("component_rules", case)
        nsi = next(case for case in key["cases"] if case["case_id"] == "nsi-polyai")
        complaints = next(bundle for bundle in nsi["route_bundles"]
                          if "complaints process" in bundle["next_step"])
        self.assertEqual(complaints["channel"], "NOT STATED")

    def test_lens_no_longer_generates_negative_token_evidence(self):
        row = {
            "fields": {
                "appeals_review": {
                    "section_present": True,
                    "matches": [{
                        "text": "A customer may ask for a human adviser.",
                        "contact_tokens": {"hrefs": [], "urls_in_text": [], "emails": [], "phones": []},
                    }],
                }
            }
        }
        case = {"title": "Synthetic"}
        lens = mod.lens_surface(case, row).decode()
        excerpt = mod.base.excerpt_surface(case, row).decode()
        self.assertIn("A customer may ask for a human adviser.", lens)
        self.assertIn("A customer may ask for a human adviser.", excerpt)
        self.assertNotIn("No link, URL, email or phone-like token was observed", lens)
        # An arm-specific warning also changes the task, even without an absence claim.
        paragraphs = lambda page: re.findall(r"<p\b[^>]*>(.*?)</p>", page, re.S)
        self.assertEqual(paragraphs(excerpt), paragraphs(lens))

    def test_lens_and_excerpt_expose_same_token_values(self):
        row = {
            "fields": {
                "appeals_review": {
                    "section_present": True,
                    "matches": [{
                        "text": "Email review@example.gov.uk or see https://example.gov.uk/review.",
                        "contact_tokens": {
                            "hrefs": [],
                            "urls_in_text": ["https://example.gov.uk/review"],
                            "emails": ["review@example.gov.uk"],
                            "phones": [],
                        },
                    }],
                }
            }
        }
        case = {"title": "Synthetic"}
        lens = mod.lens_surface(case, row).decode()
        excerpt = mod.base.excerpt_surface(case, row).decode()
        for value in ("review@example.gov.uk", "https://example.gov.uk/review"):
            self.assertIn(value, lens)
            self.assertIn(value, excerpt)


if __name__ == "__main__":
    unittest.main()
