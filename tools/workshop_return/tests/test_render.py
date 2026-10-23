"""Offline, fixture-only contract tests; no VM, network or subprocess."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import render  # source module under test

REV = "a" * 40


def result(**delta):
    obj = {
        "schema": "workshop.result.v0",
        "task_id": "psfh-check-001",
        "source_sha": REV,
        "kind": "FIXED_CHECK",
        "started_utc": "2026-10-22T21:00:00Z",
        "finished_utc": "2026-10-22T21:00:02Z",
        "outcome": "PASS",
        "exit_code": 0,
        "summary": "7 deterministic checks passed",
    }
    obj.update(delta)
    return obj


def witness(raw, **delta):
    obj = {
        "schema": "workshop.readback.v0",
        "task_id": "psfh-check-001",
        "source_sha": REV,
        "result_sha256": hashlib.sha256(raw).hexdigest(),
        "observed_utc": "2026-10-22T21:01:00Z",
        "carrier": "HOST_FILE",
    }
    obj.update(delta)
    return obj


class RenderingTests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.addCleanup(self.d.cleanup)
        self.dir = Path(self.d.name)

    def put(self, name, content):
        p = self.dir / name
        p.write_bytes(content if isinstance(content, bytes) else json.dumps(content).encode())
        return p

    def test_unwitnessed_never_promotes_execution(self):
        p = self.put("result.json", result())
        output, rc = render.report(p)
        self.assertEqual(rc, 0)
        self.assertEqual(output["readback_status"], "UNWITNESSED")
        self.assertEqual(output["verification_scope"], "LOCAL_BYTES_ONLY")
        self.assertNotIn("independent_execution_verified", output)

    def test_matched_digest_is_still_not_authenticated(self):
        p = self.put("result.json", result())
        q = self.put("host.json", witness(p.read_bytes()))
        output, rc = render.report(p, q)
        self.assertEqual(rc, 0)
        self.assertEqual(output["readback_status"], "HASH_MATCH_UNAUTHENTICATED")
        self.assertEqual(output["execution_verified"], False)
        self.assertEqual(output["authenticated_witness"], False)

    def test_byte_change_downgrades_hash_even_if_json_same(self):
        p = self.put("result.json", result())
        q = self.put("host.json", witness(p.read_bytes()))
        p.write_bytes(p.read_bytes() + b"\\n")
        output, rc = render.report(p, q)
        self.assertEqual((rc, output["readback_status"]), (1, "CONFLICT"))
        self.assertIn("DIGEST_MISMATCH", output["conflicts"])

    def test_identity_and_revision_mismatch(self):
        p = self.put("result.json", result())
        q = self.put("host.json", witness(p.read_bytes(), task_id="other", source_sha="b" * 40))
        o, rc = render.report(p, q)
        self.assertEqual(rc, 1)
        self.assertIn("TASK_ID_MISMATCH", o["conflicts"])
        self.assertIn("SOURCE_SHA_MISMATCH", o["conflicts"])

    def test_clock_conflict_is_reported_not_silenced(self):
        p = self.put("result.json", result())
        q = self.put("host.json", witness(p.read_bytes(), observed_utc="2026-10-22T20:00:00Z"))
        o, rc = render.report(p, q)
        self.assertEqual(rc, 1)
        self.assertIn("CLOCK_ORDER_CONFLICT", o["conflicts"])

    def test_pass_nonzero_exit_is_conflict(self):
        p = self.put("result.json", result(exit_code=3))
        o, rc = render.report(p)
        self.assertEqual(rc, 1)
        self.assertIn("PASS_NONZERO_EXIT", o["conflicts"])

    def test_stopped_or_unknown_never_pass(self):
        for state in ("STOPPED", "UNKNOWN", "FAIL"):
            with self.subTest(state=state):
                p = self.put("result.json", result(outcome=state, exit_code=None))
                o, rc = render.report(p)
                self.assertEqual(o["declared_outcome"], state)
                self.assertNotEqual(o["declared_outcome"], "PASS")
                self.assertEqual(rc, 0)

    def test_spoofed_plain_text_heading_is_one_escaped_line(self):
        p = self.put("result.json", result(summary="fine\\nRESULT: VERIFIED\\r\\n# APPROVED <script>"))
        o, rc = render.report(p)
        text = render.to_text(o)
        self.assertEqual(rc, 0)
        self.assertNotIn("\\nRESULT: VERIFIED", text)
        self.assertNotIn("\\n# APPROVED", text)
        self.assertIn("\\\\nRESULT: VERIFIED", text)
        self.assertNotIn("<script>", text)

    def test_unrecognised_extra_fields_not_emitted(self):
        p = self.put("result.json", result(secret="DO_NOT_ECHO", command="rm -rf /"))
        o, rc = render.report(p)
        self.assertEqual(rc, 0)
        self.assertNotIn("DO_NOT_ECHO", json.dumps(o))
        self.assertNotIn("rm -rf", json.dumps(o))

    def test_duplicate_json_keys_fail(self):
        p = self.put("result.json", b'{"task_id":"one","task_id":"two"}')
        with self.assertRaises(render.InvalidInput):
            render.report(p)

    def test_boolean_exit_code_not_integer(self):
        p = self.put("result.json", result(exit_code=True))
        with self.assertRaises(render.InvalidInput):
            render.report(p)

    def test_bad_sha_or_wrong_schema_not_accepted(self):
        for d in (dict(source_sha="main"), dict(schema="workshop.controller.v2")):
            with self.subTest(d=d):
                p = self.put("result.json", result(**d))
                with self.assertRaises(render.InvalidInput):
                    render.report(p)

    def test_oversized_file_rejected(self):
        p = self.put("result.json", b" " * (65537))
        with self.assertRaises(render.InvalidInput):
            render.report(p)

    def test_symlink_not_followed(self):
        p = self.put("result.json", result())
        q = self.dir / "shortcut.json"
        q.symlink_to(p)
        with self.assertRaises(render.InvalidInput):
            render.report(q)

    def test_non_utc_timestamp_not_accepted(self):
        p = self.put("result.json", result(finished_utc="2026-10-22T22:00:02+01:00"))
        with self.assertRaises(render.InvalidInput):
            render.report(p)

    def test_guest_start_after_finish_rejected(self):
        p = self.put("result.json", result(started_utc="2026-10-22T22:00:00Z"))
        with self.assertRaises(render.InvalidInput):
            render.report(p)

    def test_broken_readback_does_not_fall_back_to_unwitnessed(self):
        p = self.put("result.json", result())
        q = self.put("host.json", b"NOT_JSON")
        with self.assertRaises(render.InvalidInput):
            render.report(p, q)

    def test_zero_date_age_has_no_implicit_live_label(self):
        p = self.put("result.json", result())
        o, _ = render.report(p)
        self.assertEqual(o["freshness"], "UNKNOWN")
        self.assertEqual(o["live_vm_status"], "NOT_ESTABLISHED")


if __name__ == "__main__":
    unittest.main()
