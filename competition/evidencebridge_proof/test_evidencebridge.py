import copy
import unittest
from pathlib import Path

from evidencebridge import EvidenceBridgeError, analyze_bundle, load_bundle, render_html, validate_bundle

ROOT = Path(__file__).resolve().parent

class EvidenceBridgeProofTests(unittest.TestCase):
    def fixture(self, name):
        return load_bundle(ROOT / "fixtures" / f"{name}.json")

    def test_flak_repetition_is_not_support(self):
        result = analyze_bundle(self.fixture("flak"))[0]
        self.assertEqual(result.verdict, "ASSERTED_BUT_UNSUPPORTED_IN_CHECKED_SOURCES")
        self.assertEqual(result.support_groups, ())
        self.assertEqual(set(result.dependent_restatements), {"p-article-restates", "p-summary-restates"})
        self.assertIn("p-army-nearby", result.limits)

    def test_hannibal_translation_does_not_become_greek_literal(self):
        by_id = {r.claim_id: r for r in analyze_bundle(self.fixture("hannibal"))}
        greek = by_id["c-greek-literal"]
        self.assertEqual(greek.verdict, "UNRESOLVED")
        self.assertEqual(greek.support_groups, ())
        self.assertIn("p-translation-renders", greek.limits)
        self.assertTrue(any("Greek source literal" in x for x in greek.unknowns))

    def test_hannibal_source_criticism_remains_attributed(self):
        by_id = {r.claim_id: r for r in analyze_bundle(self.fixture("hannibal"))}
        claim = by_id["c-sosylus"]
        self.assertEqual(claim.verdict, "UNRESOLVED")
        self.assertIn("p-polybius-criticises", claim.limits)

    def test_r_vale_remains_unresolved_with_reported_contradiction(self):
        result = analyze_bundle(self.fixture("r-vale"))[0]
        self.assertEqual(result.verdict, "UNRESOLVED_WITH_REPORTED_CONTRADICTION")
        self.assertEqual(result.support_groups, ())
        self.assertIn("p-source-c-distinct", result.contradictions)
        self.assertTrue(any("one maker or two" in x for x in result.unknowns))

    def test_html_is_auditable(self):
        page = render_html(self.fixture("flak"))
        self.assertIn("Show me why", page)
        self.assertIn("Independent support groups", page)
        self.assertIn("World War Wings article", page)
        self.assertIn("Depends on:", page)

    def test_unknown_source_fails_closed(self):
        b = self.fixture("flak")
        b["propositions"][0]["source_id"] = "missing"
        with self.assertRaises(EvidenceBridgeError):
            validate_bundle(b)

    def test_duplicate_id_fails_closed(self):
        b = self.fixture("flak")
        b["propositions"].append(copy.deepcopy(b["propositions"][0]))
        with self.assertRaises(EvidenceBridgeError):
            validate_bundle(b)

    def test_invalid_state_and_relation_fail_closed(self):
        b = self.fixture("flak")
        b["propositions"][0]["state"] = "TRUE"
        with self.assertRaises(EvidenceBridgeError):
            validate_bundle(b)
        b = self.fixture("flak")
        b["propositions"][0]["relation"] = "PROVES"
        with self.assertRaises(EvidenceBridgeError):
            validate_bundle(b)

    def test_derived_source_cannot_fake_independence(self):
        b = self.fixture("flak")
        next(s for s in b["sources"] if s["id"] == "s-article")["independence_group"] = "fake"
        with self.assertRaises(EvidenceBridgeError):
            validate_bundle(b)

    def test_dangling_correction_fails_closed(self):
        b = self.fixture("flak")
        b["corrections"] = [{"id":"corr","supersedes_proposition_id":"missing","replacement_proposition_id":"p-video-asserts","source_id":"s-video"}]
        with self.assertRaises(EvidenceBridgeError):
            validate_bundle(b)

    def test_all_fixtures_validate(self):
        for name in ("flak", "hannibal", "r-vale"):
            with self.subTest(name=name):
                validate_bundle(self.fixture(name))

if __name__ == "__main__":
    unittest.main()
