"""Synthetic-only contract tests; no external or calibrated sensor tested."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from air_sensor_preflight import audit_bytes

BASE = b"timestamp,pm25_ug_m3\n2026-10-25T00:00:00Z,12.5\n2026-10-25T01:00:00Z,13\n2026-10-25T02:00:00Z,14\n"


class PreflightTests(unittest.TestCase):
    def test_clean_three_sample_hourly(self):
        r = audit_bytes(BASE, 60)
        self.assertEqual((r["structure_status"], r["potential_unobserved_slots"]), ("PASS", 0))
        self.assertEqual(r["calibration_and_reference_comparison"], "NOT_ASSESSED")

    def test_no_assumed_cadence(self):
        r = audit_bytes(BASE)
        self.assertEqual(r["cadence_status"], "NOT_ASSESSED")
        self.assertIsNone(r["potential_unobserved_slots"])

    def test_gap_one_slot(self):
        b = BASE.replace(b"2026-10-25T01:00:00Z,13\n", b"")
        r = audit_bytes(b, 60)
        self.assertEqual((r["structure_status"], r["potential_unobserved_slots"]), ("REVIEW", 1))

    def test_duplicate_same_instant_different_offset(self):
        b = BASE + b"2026-10-25T02:00:00+00:00,15\n"
        r = audit_bytes(b, 60)
        self.assertIn("DUPLICATE_INSTANT", [e["code"] for e in r["issues"]])
        self.assertEqual(r["cadence_status"], "UNDETERMINED")

    def test_timezone_naive_rejected(self):
        r = audit_bytes(BASE.replace(b"2026-10-25T01:00:00Z", b"2026-10-25T01:00:00"), 60)
        self.assertEqual(r["structure_status"], "FAIL")
        self.assertEqual(r["cadence_status"], "UNDETERMINED")

    def test_negative_nonfinite_and_text_rejected(self):
        for bad in (b"-3", b"NaN", b"Infinity", b"ten"):
            with self.subTest(bad=bad):
                self.assertEqual(audit_bytes(BASE.replace(b",13\n", b"," + bad + b"\n"))["structure_status"], "FAIL")

    def test_missing_reading_triggers_review(self):
        r = audit_bytes(BASE.replace(b",13\n", b",\n"), 60)
        self.assertEqual((r["blank_readings"], r["structure_status"]), (1, "REVIEW"))

    def test_irregular_interval_do_not_infer_slots(self):
        b = BASE.replace(b"2026-10-25T01:00:00Z", b"2026-10-25T01:30:00Z")
        r = audit_bytes(b, 60)
        self.assertEqual((r["cadence_status"], r["potential_unobserved_slots"]), ("INCONSISTENT", None))

    def test_reordered_do_not_infer_slots(self):
        b = b"timestamp,pm25_ug_m3\n2026-10-25T01:00:00Z,13\n2026-10-25T00:00:00Z,12\n"
        r = audit_bytes(b, 60)
        self.assertEqual(r["cadence_status"], "UNDETERMINED")
        self.assertEqual(r["structure_status"], "REVIEW")

    def test_extra_columns_rejected_for_minimal_data_contract(self):
        r = audit_bytes(b"timestamp,pm25_ug_m3,home_address\n2026-10-25T00:00:00Z,7,none\n")
        self.assertEqual(r["issues"][0]["code"], "HEADER_MISMATCH_OR_EXTRA_COLUMNS")

    def test_bad_row_shape(self):
        r = audit_bytes(BASE + b"2026-10-25T03:00:00Z,12,extra\n")
        self.assertEqual(r["structure_status"], "FAIL")

    def test_distinct_clock_change_offsets(self):
        # UK fallback on 25 October: same wall clock hour but different actual UTC instant.
        raw = (b"timestamp,pm25_ug_m3\n2026-10-25T01:30:00+01:00,9\n"
               b"2026-10-25T01:30:00+00:00,10\n")
        r = audit_bytes(raw, 60)
        self.assertEqual(r["structure_status"], "PASS")
        self.assertEqual(r["potential_unobserved_slots"], 0)

    def test_csv_bom_and_hash(self):
        b = b"\xef\xbb\xbf" + BASE
        r = audit_bytes(b)
        self.assertEqual(r["structure_status"], "PASS")
        self.assertEqual(r["input_sha256"], hashlib.sha256(b).hexdigest())

    def test_empty_no_data(self):
        self.assertEqual(audit_bytes(b"timestamp,pm25_ug_m3\n")["structure_status"], "FAIL")

    def test_oversized_file(self):
        r = audit_bytes(b"x" * (2 * 1024 * 1024 + 1))
        self.assertEqual(r["issues"][0]["code"], "FILE_TOO_LARGE")
        self.assertIsNone(r["input_sha256"])

    def test_cli_json_exit_codes_no_raw_readings(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "s.csv"
            p.write_bytes(BASE)
            cp = subprocess.run([sys.executable, str(Path(__file__).with_name("air_sensor_preflight.py")), str(p), "--interval-minutes", "60"], capture_output=True, text=True)
            r = json.loads(cp.stdout)
            self.assertEqual((cp.returncode, r["structure_status"]), (0, "PASS"))
            self.assertNotIn("12.5", cp.stdout)
            p.write_bytes(BASE.replace(b",13\n", b",\n"))
            cp = subprocess.run([sys.executable, str(Path(__file__).with_name("air_sensor_preflight.py")), str(p)], capture_output=True, text=True)
            self.assertEqual(cp.returncode, 1)
            p.write_bytes(BASE.replace(b",13\n", b",bad\n"))
            cp = subprocess.run([sys.executable, str(Path(__file__).with_name("air_sensor_preflight.py")), str(p)], capture_output=True, text=True)
            self.assertEqual(cp.returncode, 2)


if __name__ == "__main__":
    unittest.main()
