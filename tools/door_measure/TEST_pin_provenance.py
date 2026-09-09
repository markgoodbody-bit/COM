"""Offline regression cases; no GitHub or website requests.

Set PIN_PROVENANCE_REVISION to a local Git ref to run against an older tool.
The suite should fail on edd3764, not merely pass on the repaired version.
"""

import base64
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import types
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
revision = os.environ.get("PIN_PROVENANCE_REVISION")
source = (subprocess.check_output(
    ["git", "show", revision + ":tools/door_measure/pin_provenance.py"], cwd=HERE)
    if revision else (HERE / "pin_provenance.py").read_bytes())
tool = types.ModuleType("pin_provenance_under_test")
exec(compile(source, str(HERE / "pin_provenance.py"), "exec"), tool.__dict__)


def digest(data):
    return hashlib.sha256(data).hexdigest()


class PinIdentityTests(unittest.TestCase):
    def run_check(self, emitted=b"source\r\n", historical=b"source\n", overrides=None,
                  unavailable=False, incomplete=False, declared=None):
        meta = {"sha256": digest(emitted), "bytes": len(emitted)}
        meta.update(overrides or {})
        record = {"source_review": "source-ref", "files":
                  {"art/example.txt": meta} if declared is None else declared}
        encoded = {"content": base64.b64encode(json.dumps(record).encode()).decode()}
        exact = {digest(historical): ["proposals/example.txt"]}
        normalized = {digest(historical.replace(b"\r\n", b"\n")): ["proposals/example.txt"]}
        output = io.StringIO()
        with patch.object(tool, "gh", return_value=encoded), \
             patch.object(tool, "index_by_content", return_value=(exact, normalized, 1, incomplete)), \
             patch.object(tool, "emitted_bytes", return_value=None if unavailable else emitted), \
             contextlib.redirect_stdout(output):
            result = tool.check("repo", "pins-ref", "pins.json", "files", "source-ref", ("proposals/",))
        return result, output.getvalue()

    def test_fabricated_identity_cannot_use_normalized_fallback(self):
        result, report = self.run_check(overrides={"sha256": "0" * 64, "bytes": 999999})
        self.assertEqual(result, 1)
        self.assertIn("INVALID DECLARED IDENTITY: 1", report)
        self.assertNotIn("SAME CONTENT, line endings differ: 1", report)

    def test_wrong_hash_alone_is_rejected(self):
        self.assertEqual(self.run_check(overrides={"sha256": "0" * 64})[0], 1)

    def test_wrong_length_alone_is_rejected(self):
        self.assertEqual(self.run_check(overrides={"bytes": 999999})[0], 1)

    def test_exact_historical_pin_does_not_hide_wrong_emitted_copy(self):
        result, report = self.run_check(overrides={"sha256": digest(b"source\n"), "bytes": 7})
        self.assertEqual(result, 1)
        self.assertIn("BYTE-EXACT in the source tree: 0 of 1", report)

    def test_exact_match_is_accepted(self):
        result, report = self.run_check(emitted=b"source\n")
        self.assertEqual(result, 0)
        self.assertIn("BYTE-EXACT in the source tree: 1 of 1", report)

    def test_legitimate_eol_shift_is_not_called_exact(self):
        result, report = self.run_check()
        self.assertEqual(result, 0)
        self.assertIn("SAME CONTENT, line endings differ: 1", report)
        self.assertIn("BYTE-EXACT in the source tree: 0 of 1", report)

    def test_reverse_eol_shift_does_not_assume_checkout_origin(self):
        result, report = self.run_check(emitted=b"source\n", historical=b"source\r\n")
        self.assertEqual(result, 0)
        self.assertNotIn("emitted from a CRLF checkout", report)

    def test_missing_or_noninteger_declaration_is_not_resolved(self):
        for override in ({"sha256": None}, {"bytes": None}, {"bytes": True}, {"bytes": "8"}):
            with self.subTest(override=override):
                self.assertEqual(self.run_check(overrides=override)[0], 1)

    def test_unreadable_emitted_copy_is_no_verdict_even_if_hash_exists(self):
        result, report = self.run_check(emitted=b"source\n", unavailable=True)
        self.assertEqual(result, 2)
        self.assertIn("NO VERDICT", report)

    def test_valid_pin_with_no_historical_match_is_unresolved(self):
        result, report = self.run_check(emitted=b"unrelated")
        self.assertEqual(result, 1)
        self.assertIn("NO SOURCE BLOB: 1", report)

    def test_incomplete_source_scan_stops_before_verdict(self):
        result, report = self.run_check(incomplete=True)
        self.assertEqual(result, 2)
        self.assertIn("INCOMPLETE source scan", report)
        self.assertNotIn("WHAT THIS ESTABLISHES", report)

    def test_empty_file_is_valid_content(self):
        self.assertEqual(self.run_check(emitted=b"", historical=b"")[0], 0)


class SourceScanTests(unittest.TestCase):
    def scan(self, blobs, values, truncated=False):
        output = io.StringIO()
        with patch.object(tool, "tree", return_value=(blobs, truncated)), \
             patch.object(tool, "blob_bytes", side_effect=lambda repo, sha: values.get(sha)), \
             contextlib.redirect_stdout(output):
            result = tool.index_by_content("repo", "ref", ("proposals/",))
        return result, output.getvalue()

    def test_missing_blob_is_not_counted_as_hashed(self):
        result, report = self.scan({"proposals/good": "a", "proposals/missing": "b"}, {"a": b"good"})
        exact, normalized, count, incomplete = result
        self.assertEqual(count, 1)
        self.assertEqual(len(exact), 1)
        self.assertTrue(incomplete)
        self.assertIn("proposals/missing", report)

    def test_complete_scan_counts_duplicate_and_empty_blobs(self):
        result, _ = self.scan({"proposals/a": "a", "proposals/b": "a", "proposals/empty": "e",
                               "outside": "unreadable"}, {"a": b"good", "e": b""})
        exact, normalized, count, incomplete = result
        self.assertEqual(count, 3)
        self.assertEqual(len(exact), 2)
        self.assertFalse(incomplete)

    def test_truncated_tree_remains_incomplete(self):
        self.assertTrue(self.scan({}, {}, truncated=True)[0][3])

    def test_unreadable_tree_has_no_index(self):
        self.assertIsNone(self.scan(None, {})[0][0])

    def test_empty_successful_raw_response_is_not_a_read_failure(self):
        with patch.object(tool, "gh", return_value=b"") as api:
            self.assertEqual(tool.blob_bytes("repo", "empty-sha"), b"")
            self.assertEqual(api.call_count, 1)

    def test_empty_base64_emitted_copy_is_readable(self):
        with patch.object(tool, "gh", return_value={"content": "", "encoding": "base64", "sha": "empty"}), \
             patch.object(tool, "blob_bytes", return_value=None):
            self.assertEqual(tool.emitted_bytes("repo", "ref", "empty"), b"")

    def test_omitted_large_file_content_falls_back_to_blob(self):
        with patch.object(tool, "gh", return_value={"content": "", "encoding": "none", "sha": "large"}), \
             patch.object(tool, "blob_bytes", return_value=b"large file") as read_blob:
            self.assertEqual(tool.emitted_bytes("repo", "ref", "large"), b"large file")
            read_blob.assert_called_once_with("repo", "large")

    def test_api_json_mode_does_not_request_raw_bytes(self):
        response = types.SimpleNamespace(returncode=0, stdout=b'{"ok":true}')
        with patch.object(tool.subprocess, "run", return_value=response) as run:
            self.assertEqual(tool.gh("example"), {"ok": True})
            self.assertEqual(run.call_args.args[0], ["gh", "api", "example"])

    def test_api_raw_mode_requests_and_keeps_raw_bytes(self):
        response = types.SimpleNamespace(returncode=0, stdout=b'bytes')
        with patch.object(tool.subprocess, "run", return_value=response) as run:
            self.assertEqual(tool.gh("example", raw=True), b"bytes")
            self.assertIn("Accept: application/vnd.github.raw", run.call_args.args[0])


@unittest.skipUnless(os.environ.get("PIN_PROVENANCE_LOCAL_HISTORY") == "1",
                     "optional historical check needs the original local Git objects")
class HistoricalGitTests(unittest.TestCase):
    def test_original_36_pin_inventory_without_network(self):
        pins_ref = "b078c3cf4aa251c4226985c2547d03e3d88b196a"
        source_ref = "dfe4b5fcfa279ef08a1d5aac5d3c3a1c59494175"

        def git(*args):
            return subprocess.check_output(["git", *args], cwd=HERE)

        def local_contents(endpoint):
            path, ref = endpoint.split("/contents/", 1)[1].split("?ref=")
            return {"encoding": "base64", "content": base64.b64encode(
                git("show", ref + ":" + path)).decode()}

        blobs = {}
        for entry in git("ls-tree", "--full-tree", "-r", "-z", source_ref).split(b"\0"):
            if not entry:
                continue
            header, path = entry.split(b"\t", 1)
            mode, kind, sha = header.split()
            if kind == b"blob":
                blobs[path.decode()] = sha.decode()
        output = io.StringIO()
        with patch.object(tool, "gh", side_effect=local_contents), \
             patch.object(tool, "tree", return_value=(blobs, False)), \
             patch.object(tool, "blob_bytes", side_effect=lambda repo, sha: git("cat-file", "blob", sha)), \
             contextlib.redirect_stdout(output):
            result = tool.check("repo", pins_ref, "scripts/WORKS_COPIES.json", "files",
                                source_ref, ("proposals/",))
        report = output.getvalue()
        print(report)
        self.assertEqual(result, 1)  # Built HTML has no byte-identical historical source blob.
        self.assertIn("declares      36 entries", report)
        self.assertIn("hashed 67 blobs", report)
        self.assertIn("BYTE-EXACT in the source tree: 24 of 36", report)
        self.assertIn("SAME CONTENT, line endings differ: 6", report)
        self.assertIn("NO SOURCE BLOB: 6", report)
        self.assertNotIn("INVALID DECLARED IDENTITY", report)
        self.assertNotIn("NO VERDICT", report)


if __name__ == "__main__":
    unittest.main()
