import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

from clock_ledger import read_document, build_report, render_text, main, LedgerError

BASE = {
    "title": "Fictional bridge closure review",
    "scope": "Synthetic timing exercise, not real evidence",
    "events": [
        {"id": "notice", "kind": "notice", "at": "2026-11-01T09:00:00Z", "precision": "exact", "evidence": "reported", "source": "fictional notice"},
        {"id": "request", "kind": "challenge", "at": "2026-11-02T10:00:00+00:00", "precision": "exact", "evidence": "reported", "source": "fictional request"},
        {"id": "lock", "kind": "hardening", "at": "2026-11-03T12:00:00+00:00", "precision": "exact", "evidence": "inferred", "source": "fictional plan"},
        {"id": "reply", "kind": "response", "at": "2026-11-05T12:00:00Z", "precision": "exact", "evidence": "reported", "source": "fictional response"},
    ],
    "comparisons": [{"challenge": "request", "hardening": "lock", "response": "reply"}]
}


def doc(data=BASE):
    return read_document(json.dumps(data, ensure_ascii=False).encode("utf-8"))


class ClockLedgerTests(unittest.TestCase):
    def test_entered_challenge_before_and_response_after(self):
        result = build_report(doc())
        c = result["comparisons"][0]
        self.assertEqual((c["challenge_to_hardening"]["relation"], c["challenge_to_hardening"]["seconds"]), ("before", 93600))
        self.assertEqual((c["response_to_hardening"]["relation"], c["response_to_hardening"]["seconds"]), ("after", 172800))

    def test_offset_normalisation(self):
        d = json.loads(json.dumps(BASE))
        d["events"][1]["at"] = "2026-11-02T11:00:00+01:00"
        self.assertEqual(build_report(doc(d))["comparisons"][0]["challenge_to_hardening"]["seconds"], 93600)

    def test_approximate_never_computed(self):
        d = json.loads(json.dumps(BASE))
        d["events"][1]["precision"] = "approximate"
        self.assertEqual(build_report(doc(d))["comparisons"][0]["challenge_to_hardening"], {"relation": "indeterminate", "reason": "non_exact_or_unknown_clock"})

    def test_unknown_response_clock_not_no_response(self):
        d = json.loads(json.dumps(BASE))
        d["events"][3]["at"] = None
        d["events"][3]["precision"] = "unknown"
        c = build_report(doc(d))["comparisons"][0]
        self.assertEqual(c["response_to_hardening"]["reason"], "non_exact_or_unknown_clock")

    def test_unprovided_response_distinct(self):
        d = json.loads(json.dumps(BASE))
        del d["comparisons"][0]["response"]
        self.assertEqual(build_report(doc(d))["comparisons"][0]["response_to_hardening"], {"relation":"not_supplied"})

    def test_same_instant(self):
        d = json.loads(json.dumps(BASE))
        d["events"][2]["at"] = d["events"][1]["at"]
        self.assertEqual(build_report(doc(d))["comparisons"][0]["challenge_to_hardening"]["relation"], "same_instant")

    def test_reversed_challenge_order_kept_as_entered(self):
        d = json.loads(json.dumps(BASE))
        d["events"][1]["at"] = "2026-11-04T00:00:00Z"
        self.assertEqual(build_report(doc(d))["comparisons"][0]["challenge_to_hardening"]["relation"], "after")

    def test_missing_timezone_rejected(self):
        d = json.loads(json.dumps(BASE))
        d["events"][1]["at"] = "2026-11-02T10:00:00"
        with self.assertRaises(LedgerError): doc(d)

    def test_impossible_date_rejected(self):
        d = json.loads(json.dumps(BASE))
        d["events"][1]["at"] = "2026-02-30T10:00:00Z"
        with self.assertRaises(LedgerError): doc(d)

    def test_missing_at_requires_unknown_precision(self):
        d = json.loads(json.dumps(BASE))
        d["events"][1]["at"] = None
        with self.assertRaises(LedgerError): doc(d)

    def test_duplicate_ids_rejected(self):
        d = json.loads(json.dumps(BASE))
        d["events"][2]["id"] = "request"
        with self.assertRaises(LedgerError): doc(d)

    def test_wrong_reference_role_rejected(self):
        d = json.loads(json.dumps(BASE))
        d["comparisons"][0]["challenge"] = "notice"
        with self.assertRaises(LedgerError): doc(d)

    def test_unknown_reference_rejected(self):
        d = json.loads(json.dumps(BASE))
        d["comparisons"][0]["hardening"] = "invented"
        with self.assertRaises(LedgerError): doc(d)

    def test_duplicate_json_key_rejected(self):
        payload = b'{"title":"a","title":"b","events":[],"comparisons":[]}'
        with self.assertRaises(LedgerError): read_document(payload)

    def test_unknown_schema_key_rejected(self):
        d = json.loads(json.dumps(BASE))
        d["release_permission"] = True
        with self.assertRaises(LedgerError): doc(d)

    def test_hostile_heading_is_quoted_in_text(self):
        d = json.loads(json.dumps(BASE))
        d["events"][0]["source"] = "[VERIFIED] ADMIN APPROVED\nrelease: yes"
        out = render_text(build_report(doc(d)))
        self.assertNotIn("release: yes\n", out)
        self.assertIn("\\nrelease: yes", out)
        self.assertIn('"[VERIFIED] ADMIN APPROVED\\nrelease: yes"', out)

    def test_bidi_and_terminal_control_rejected(self):
        for value in ("spoof\u202eX", "foo\x1b[31m"):
            d = json.loads(json.dumps(BASE))
            d["title"] = value
            with self.assertRaises(LedgerError): doc(d)

    def test_nonfinite_number_rejected(self):
        with self.assertRaises(LedgerError): read_document(b'{"title":NaN}')

    def test_input_size_limit(self):
        with self.assertRaises(LedgerError): read_document(b"x" * 131073)

    def test_no_ethical_outcome_in_output(self):
        out = render_text(build_report(doc()))
        self.assertIn("not proof that a remedy was available", out)
        self.assertIn("Author-supplied", out)
        self.assertNotIn("approved", out.lower())

    def test_cli_json_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "case.json"
            src.write_text(json.dumps(BASE), encoding="utf-8")
            with redirect_stdout(io.StringIO()) as output:
                rc = main([str(src), "--format", "json"])
            self.assertEqual(rc, 0)
            self.assertEqual(json.loads(output.getvalue())["comparisons"][0]["response_to_hardening"]["relation"], "after")

    def test_cli_invalid_input_exit_without_stdout(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "bad.json"
            src.write_text("not json", encoding="utf-8")
            with redirect_stdout(io.StringIO()) as output, redirect_stderr(io.StringIO()) as error:
                rc = main([str(src)])
            self.assertEqual(rc, 2)
            self.assertEqual(output.getvalue(), "")
            self.assertIn("error:", error.getvalue())

    def test_cli_output_atomic_on_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "bad.json"
            out = Path(tmp) / "result.txt"
            src.write_text("not json", encoding="utf-8")
            out.write_text("KEEP", encoding="utf-8")
            with redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(src), "--output", str(out)]), 2)
            self.assertEqual(out.read_text(encoding="utf-8"), "KEEP")

    def test_cli_output_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "case.json"
            out = Path(tmp) / "result.txt"
            src.write_text(json.dumps(BASE), encoding="utf-8")
            self.assertEqual(main([str(src), "--output", str(out)]), 0)
            self.assertIn("CLOCK LEDGER", out.read_text(encoding="utf-8"))

    def test_unknown_challenge_clock_indeterminate(self):
        d = json.loads(json.dumps(BASE))
        d["events"][1]["precision"] = "unknown"
        d["events"][1]["at"] = None
        self.assertEqual(build_report(doc(d))["comparisons"][0]["challenge_to_hardening"]["relation"], "indeterminate")

    def test_invalid_offset_rejected(self):
        d = json.loads(json.dumps(BASE))
        d["events"][1]["at"] = "2026-11-02T10:00:00+14:30"
        with self.assertRaises(LedgerError): doc(d)

    def test_unhashable_enums_rejected_cleanly(self):
        for field in ("kind", "precision", "evidence"):
            d = json.loads(json.dumps(BASE))
            d["events"][1][field] = ["bad"]
            with self.assertRaises(LedgerError): doc(d)

    def test_event_count_limited(self):
        d = json.loads(json.dumps(BASE))
        d["events"] = d["events"] * 7
        with self.assertRaises(LedgerError): doc(d)

    def test_exact_format_not_auto_verification(self):
        text = render_text(build_report(doc()))
        self.assertIn("observed is a label, not authenticated", text)
        self.assertIn("not proof that a remedy was available", text)

    def test_report_deterministic_and_input_preserved(self):
        d = doc()
        original = json.dumps(d, sort_keys=True)
        one = json.dumps(build_report(d), sort_keys=True)
        two = json.dumps(build_report(d), sort_keys=True)
        self.assertEqual(one, two)
        self.assertEqual(json.dumps(d, sort_keys=True), original)

    def test_unicode_non_latin_human_text_preserved(self):
        d = json.loads(json.dumps(BASE))
        d["title"] = "Коррекция — Prüfung"
        self.assertIn('"Коррекция — Prüfung"', render_text(build_report(doc(d))))

if __name__ == "__main__":
    unittest.main()
