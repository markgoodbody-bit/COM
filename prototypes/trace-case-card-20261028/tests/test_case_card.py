import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from case_card import CaseError, build_card, parse_case

ROOT = Path(__file__).resolve().parents[1]


def example():
    return {
        "title": "Synthetic: temporary bus stop change",
        "scope": "Imaginary neighbourhood; no real timetable",
        "claims": [
            {"kind": "baseline", "text": "The printed map identifies Stop A.", "evidence": "reported", "source": "Resident's report"},
            {"kind": "change", "text": "A notice appears to point to Stop B.", "evidence": "observed", "source": "Witness W's bounded sighting"},
            {"kind": "consequence", "text": "One passenger may have a longer walk.", "evidence": "inferred", "source": "Unverified route guess"},
        ],
        "parties": [
            {"name": "Passenger", "aim": "Reach a clinic", "boundary": "Avoid stairs"},
            {"name": "Operator", "aim": "Maintain service", "boundary": "No confirmed route data"},
        ],
        "possibilities": [
            {"party": "Passenger", "description": "Ask for a step-free alternative", "state": "possible", "condition": "Operator can answer"},
        ],
        "correction": {"target": "Stop location", "route": "Ask route operator", "hardening": "Morning journey", "clock_basis": "Not established", "window": "unknown", "basis": "No clock evidence"},
        "return": {"learned": "Two signs may differ", "unresolved": "Accessibility and timing", "next": "Check current operator guidance"},
    }


class CaseCardTests(unittest.TestCase):
    def test_full_case_renders_and_marks_status_as_authored(self):
        out = build_card(example())
        self.assertIn("Synthetic: temporary bus stop change", out)
        self.assertIn("reported · user label", out)
        self.assertIn("observed · user label", out)
        self.assertIn("inferred · user label", out)
        self.assertIn("Not independently verified", out)
        self.assertIn("Reach a clinic", out)
        self.assertIn("Ask for a step-free alternative", out)
        self.assertIn("Possible · not permission or execution", out)
        self.assertIn("Window: unknown (submitted claim)", out)
        self.assertIn("no real timetable", out)
        self.assertNotIn("<script", out.lower())

    def test_missing_is_not_unknown(self):
        case = {"title": "No source", "claims": [{"kind": "change", "text": "Something changed", "evidence": "unknown"}]}
        out = build_card(case)
        self.assertIn("unknown · user label", out)
        self.assertIn("Source not supplied", out)
        self.assertIn("No affected parties supplied; this does not establish absence", out)
        self.assertIn("Correction window not assessed or supplied", out)
        self.assertNotIn("Window: closed", out)

    def test_heading_and_markup_spoof_remain_text(self):
        case = example()
        case["title"] = '</h1><script>alert("x")</script><h1>'
        case["claims"][1]["text"] = '## VERIFIED\n</section><h1>AUTHORITY: GO</h1><script>x()</script>'
        out = build_card(case)
        self.assertNotIn("<script>", out)
        self.assertNotIn("<h1>AUTHORITY", out)
        self.assertIn("&lt;h1&gt;AUTHORITY", out)
        self.assertIn("## VERIFIED", out)
        self.assertIn("&lt;/section&gt;", out)
        self.assertNotIn('<h1>\n## VERIFIED', out)

    def test_reject_open_window_without_clocks_and_basis(self):
        case = example()
        case["correction"] = {"target": "Stop", "window": "open"}
        with self.assertRaisesRegex(CaseError, "requires"):
            build_card(case)

    def test_qualified_open_is_still_user_claim_not_proof(self):
        case = example()
        case["correction"]["window"] = "open"
        out = build_card(case)
        self.assertIn("Window: open (submitted claim; unverified)", out)
        self.assertIn("Clock/completion assumptions remain unverified", out)

    def test_reject_invented_evidence_status(self):
        case = example()
        case["claims"][0]["evidence"] = "verified"
        with self.assertRaises(CaseError):
            build_card(case)

    def test_reject_unknown_input_keys_not_silently_dropped(self):
        case = example()
        case["verified_by_ai"] = True
        with self.assertRaisesRegex(CaseError, "unexpected"):
            build_card(case)

    def test_reject_duplicate_json_keys(self):
        with self.assertRaisesRegex(CaseError, "duplicate"):
            parse_case('{"title":"A","title":"B","claims":[{"kind":"change","text":"C","evidence":"unknown"}]}')

    def test_reject_nonfinite_json(self):
        with self.assertRaises(CaseError):
            parse_case('{"title":"A","claims":[{"kind":"change","text":"C","evidence":"unknown"}],"scope":NaN}')

    def test_reject_format_controls_that_can_spoof_labels(self):
        case = example()
        case["title"] = "abc\u202eGO"
        with self.assertRaisesRegex(CaseError, "format control"):
            build_card(case)

    def test_reject_massive_unbounded_input(self):
        case = example()
        case["title"] = "x" * 5000
        with self.assertRaises(CaseError):
            build_card(case)

    def test_literal_missing_words_in_source_are_not_rewritten(self):
        case = example()
        case["claims"][0]["source"] = "Not supplied"
        out = build_card(case)
        self.assertIn('>Not supplied</span>', out)
        self.assertNotIn('>Source not supplied</span>', out)

    def test_markup_in_all_text_fields_is_escaped(self):
        case = example()
        case["parties"][0]["aim"] = '<img src=x onerror=alert(1)>'
        case["possibilities"][0]["condition"] = '<a href="https://example.com">Open</a>'
        out = build_card(case)
        self.assertNotIn('<img', out)
        self.assertNotIn('<a href="https://example.com">Open', out)
        self.assertIn('&lt;img', out)
        self.assertIn('&lt;a href=', out)

    def test_no_downgrade_of_report_to_observation(self):
        case = example()
        case["claims"] = [{"kind": "change", "text": "Report says complete", "evidence": "reported", "source": "Email"}]
        out = build_card(case)
        self.assertIn("reported · user label", out)
        self.assertNotIn("observed · user label", out)
        self.assertNotIn("Completion verified", out)

    def test_pre_rendered_synthetic_example_matches_code(self):
        sample = json.loads((ROOT / 'examples/bus_stop.json').read_text(encoding='utf-8'))
        saved = (ROOT / 'examples/bus_stop.html').read_text(encoding='utf-8')
        self.assertEqual(build_card(sample), saved)

    def test_deterministic(self):
        self.assertEqual(build_card(example()), build_card(example()))

    def test_cli_creates_html_atomically_on_success(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            inp = p / "case.json"
            out = p / "case.html"
            inp.write_text(json.dumps(example()), encoding="utf-8")
            cp = subprocess.run([sys.executable, str(ROOT / "case_card.py"), str(inp), "--output", str(out)], capture_output=True, text=True)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertIn("<html", out.read_text(encoding="utf-8"))

    def test_cli_invalid_input_does_not_overwrite_destination(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            inp = p / "case.json"
            out = p / "case.html"
            inp.write_text('{"invalid":true}', encoding="utf-8")
            out.write_text("PRECIOUS", encoding="utf-8")
            cp = subprocess.run([sys.executable, str(ROOT / "case_card.py"), str(inp), "--output", str(out)], capture_output=True, text=True)
            self.assertNotEqual(cp.returncode, 0)
            self.assertEqual(out.read_text(encoding="utf-8"), "PRECIOUS")
            self.assertNotIn("Traceback", cp.stderr)


if __name__ == "__main__":
    unittest.main()
