import hashlib
import json
import stat
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "anonymous_text_transport.py"
sys.path.insert(0, str(ROOT))
import anonymous_text_transport as transport  # noqa: E402


class AnonymousTextTransportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def _members(*, aid=True, case=b"What bounded action is warranted now?\n"):
        members = {
            "START_HERE.md": b"# Receiver task\n\nRead only this packet.\n",
            "RUN_INSTRUCTION.md": b"Return only the requested answer.\n",
            "CASE_TASK.md": case,
            "SOURCES/02_zeta.txt": b"Second preserved source.\n",
            "SOURCES/01_alpha.txt": "First preserved source: caf\u00e9.\n".encode("utf-8"),
        }
        if aid:
            members["REASONING_AID.md"] = b"Use these bounded questions only.\n"
        declared = {
            name: {"sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}
            for name, data in sorted(members.items())
            if name != "START_HERE.md"
        }
        members["CELL_MANIFEST.json"] = (
            json.dumps({"schema_version": "1", "members": declared}, sort_keys=True, indent=2) + "\n"
        ).encode("utf-8")
        return members

    @staticmethod
    def _write_zip(path, members, order=None):
        order = order or list(members)
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
            for name in order:
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_STORED
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                archive.writestr(info, members[name])

    @staticmethod
    def _resign(message):
        digest_start = message.rfind(b"\n", 0, len(message) - 1) + 1
        prefix = message[:digest_start]
        return prefix + transport.DIGEST_LABEL + hashlib.sha256(prefix).hexdigest().encode() + b"\n"

    def test_render_is_deterministic_canonical_and_exact(self):
        members = self._members()
        first = self.base / "public-random-alias-a.zip"
        second = self.base / "unrelated-name.zip"
        self._write_zip(first, members, list(reversed(list(members))))
        self._write_zip(second, members, list(members))

        rendered = transport.render_cell(first)
        self.assertEqual(rendered, transport.render_cell(second))
        self.assertTrue(rendered.startswith(transport.LAUNCH_SENTENCE + transport.TRANSPORT_START))
        self.assertEqual(1, rendered.count(b"message_sha256: "))
        self.assertNotIn(first.name.encode(), rendered)

        reconstructed, message_hash = transport.parse_message(rendered)
        self.assertEqual(members, reconstructed)
        self.assertEqual(hashlib.sha256(rendered[: rendered.rfind(b"message_sha256: ")]).hexdigest(), message_hash)
        count, verified_hash = transport.verify_against_cell(rendered, first)
        self.assertEqual(len(members), count)
        self.assertEqual(message_hash, verified_hash)

        positions = [rendered.index(f'name: "{name}"'.encode()) for name in transport.canonical_member_order(set(members))]
        self.assertEqual(positions, sorted(positions))
        for name, data in members.items():
            self.assertIn(f"byte_length: {len(data)}\n".encode(), rendered)
            self.assertIn(f"sha256: {hashlib.sha256(data).hexdigest()}\n".encode(), rendered)

    def test_optional_aid_is_omitted_without_changing_schema(self):
        members = self._members(aid=False)
        cell = self.base / "cell.zip"
        self._write_zip(cell, members)
        rendered = transport.render_cell(cell)
        reconstructed, _ = transport.parse_message(rendered)
        self.assertNotIn("REASONING_AID.md", reconstructed)
        self.assertEqual(
            [
                "START_HERE.md",
                "RUN_INSTRUCTION.md",
                "CASE_TASK.md",
                "SOURCES/01_alpha.txt",
                "SOURCES/02_zeta.txt",
                "CELL_MANIFEST.json",
            ],
            list(reconstructed),
        )

    def test_rejects_duplicate_unsafe_non_utf8_and_delimiter_members(self):
        valid = self._members()

        duplicate = self.base / "duplicate.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(duplicate, "w") as archive:
                for _ in range(2):
                    info = zipfile.ZipInfo("START_HERE.md")
                    info.external_attr = (stat.S_IFREG | 0o644) << 16
                    archive.writestr(info, valid["START_HERE.md"])
        with self.assertRaisesRegex(transport.TransportError, "duplicate ZIP member"):
            transport.read_cell(duplicate)

        unsafe = dict(valid)
        unsafe["../escape.txt"] = b"escape\n"
        unsafe_path = self.base / "unsafe.zip"
        self._write_zip(unsafe_path, unsafe)
        with self.assertRaisesRegex(transport.TransportError, "unsafe ZIP member"):
            transport.read_cell(unsafe_path)

        for label, bad_case, error in (
            ("non-utf8", b"bad:\xff\n", "non-UTF-8"),
            ("delimiter", b"<<<FRESH_USE_MEMBER_V1>>>\n", "delimiter collision"),
        ):
            path = self.base / f"{label}.zip"
            self._write_zip(path, self._members(case=bad_case))
            with self.subTest(label=label), self.assertRaisesRegex(transport.TransportError, error):
                transport.read_cell(path)

    def test_whole_message_and_member_tampering_fail_closed(self):
        members = self._members()
        cell = self.base / "cell.zip"
        self._write_zip(cell, members)
        rendered = transport.render_cell(cell)

        tampered = rendered.replace(b"First preserved source", b"F1rst preserved source", 1)
        with self.assertRaisesRegex(transport.TransportError, "whole transport message hash mismatch"):
            transport.parse_message(tampered)

        resigned = self._resign(tampered)
        with self.assertRaisesRegex(transport.TransportError, "member hash mismatch"):
            transport.parse_message(resigned)

    def test_verify_compares_every_reconstructed_byte_to_original_cell(self):
        first_members = self._members()
        second_members = self._members(case=b"What different action is warranted now?\n")
        first = self.base / "first.zip"
        second = self.base / "second.zip"
        self._write_zip(first, first_members)
        self._write_zip(second, second_members)
        message = transport.render_cell(first)

        with self.assertRaisesRegex(transport.TransportError, "reconstructed/original member bytes differ"):
            transport.verify_against_cell(message, second)

    def test_cli_render_verify_and_create_only_output(self):
        cell = self.base / "cell.zip"
        message = self.base / "message.txt"
        self._write_zip(cell, self._members())
        render = subprocess.run(
            [sys.executable, str(TOOL), "render", "--cell", str(cell), "--output", str(message)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(0, render.returncode, render.stderr)
        verify = subprocess.run(
            [sys.executable, str(TOOL), "verify", "--message", str(message), "--cell", str(cell)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(0, verify.returncode, verify.stderr)
        self.assertIn("verified 7 exact members", verify.stdout)
        overwrite = subprocess.run(
            [sys.executable, str(TOOL), "render", "--cell", str(cell), "--output", str(message)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(2, overwrite.returncode)
        self.assertIn("refusing to overwrite", overwrite.stderr)


if __name__ == "__main__":
    unittest.main()
