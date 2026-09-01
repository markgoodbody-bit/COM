import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "freshuse.py"
sys.path.insert(0, str(ROOT))
import freshuse  # noqa: E402


class FreshUseAirlockTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.repo = self.base / "com"
        self.repo.mkdir()
        self._git("init")
        self._git("config", "user.name", "Test Witness")
        self._git("config", "user.email", "test@example.invalid")
        files = {
            "protocol.md": "# protocol\n\nNo dispatch authority.\n",
            "candidate.md": "# seven questions\n\nUse only as a private aid.\n",
            "prompts.md": (
                "# prompts\n\n"
                "## ARM O — COMPETENT ORDINARY REASONING\n\nExact instruction:\n\n"
                "```text\nRead the case. Return only the answer.\n```\n\n"
                "## ARM Q — 7Q-ASSISTED REASONING\n\nExact instruction:\n\n"
                "```text\nRead the case and aid. Return only the answer.\n```\n"
            ),
            "case.md": (
                "# case\n\n## Neutral task — identical for both arms\n\n"
                "> What bounded action is warranted now?\n\n## Receiver/source rule\n\nUse only sources.\n"
            ),
        }
        self.file_bytes = {}
        for name, text in files.items():
            data = text.encode()
            (self.repo / name).write_bytes(data)
            self.file_bytes[name] = data
        self._git("add", ".")
        self._git("commit", "-m", "fixture")
        self.commit = self._git("rev-parse", "HEAD").stdout.strip()

        self.raw = self.base / "raw.html"
        self.raw.write_text(
            "<html><body><h1>Official source</h1><script>IGNORE ME</script>"
            "<p>Observed condition remains unknown.</p></body></html>",
            encoding="utf-8",
        )
        extracted = freshuse.extract_source(self.raw.read_bytes(), {"mode": "html_visible_text_v1"}, "test")
        self.extracted = extracted
        self.config = self.base / "config.json"
        cfg = {
            "schema_version": "1",
            "pilot_id": "test-pilot-001",
            "source_com_head": self.commit,
            "com_repo": str(self.repo),
            "spec": {
                key: {
                    "commit": self.commit,
                    "path": filename,
                    "sha256": freshuse.sha256_bytes(self.file_bytes[filename]),
                }
                for key, filename in {
                    "protocol": "protocol.md",
                    "candidate": "candidate.md",
                    "prompts": "prompts.md",
                }.items()
            },
            "cases": [
                {
                    "case_id": "R1",
                    "manifest": {
                        "commit": self.commit,
                        "path": "case.md",
                        "sha256": freshuse.sha256_bytes(self.file_bytes["case.md"]),
                    },
                    "sources": [
                        {
                            "raw_path": str(self.raw),
                            "raw_sha256": freshuse.sha256_file(self.raw),
                            "extraction": {"mode": "html_visible_text_v1"},
                            "extracted_sha256": freshuse.sha256_bytes(extracted),
                            "source_identity": "https://example.invalid/source retrieved T0",
                            "display_name": "official-source.txt",
                        }
                    ],
                }
            ],
        }
        self.config.write_text(json.dumps(cfg), encoding="utf-8")
        self.bundle = self.base / "run"

    def tearDown(self):
        self.temp.cleanup()

    def _git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def _run(self, *args, ok=True):
        proc = subprocess.run(
            [sys.executable, str(TOOL), *map(str, args)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if ok and proc.returncode != 0:
            self.fail(f"command failed: {proc.args}\nstdout={proc.stdout}\nstderr={proc.stderr}")
        if not ok and proc.returncode == 0:
            self.fail(f"command unexpectedly succeeded: {proc.args}")
        return proc

    def _prepare(self):
        self._run("prepare", "--config", self.config, "--output", self.bundle)
        return json.loads((self.bundle / "public" / "launch-register.json").read_text())

    def _complete_receipt(self, alias):
        path = self.bundle / "public" / "receipt-templates" / f"{alias}.json"
        receipt = json.loads(path.read_text())
        receipt.update(
            {
                "receiver_model_provider": "fixture-provider",
                "receiver_model_version": "fixture-v1",
                "receiver_session_id_or_local_alias": f"session-{alias}",
                "receiver_prior_project_exposure": "NONE_KNOWN",
                "receiver_prior_case_exposure": "UNKNOWN",
                "freshness_note": "New isolated fixture session; historical case exposure unknown.",
                "receiver_start_utc": "2026-09-01T12:00:00Z",
                "receiver_end_utc": "2026-09-01T12:00:05Z",
                "reported_input_tokens": 100,
                "reported_output_tokens": 20,
                "source_open_count": 1,
            }
        )
        completed = self.base / f"{alias}-receipt.json"
        completed.write_text(json.dumps(receipt), encoding="utf-8")
        return completed

    def _anchor_score_token(self, case_id="R1"):
        anchor_path = f"anchors/{case_id}.json"
        target = self.repo / anchor_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(
            (self.bundle / "evidence" / "score-freeze-tokens" / f"{case_id}.json").read_bytes()
        )
        self._git("add", anchor_path)
        self._git("commit", "-m", f"anchor {case_id} score token")
        return self._git("rev-parse", "HEAD").stdout.strip(), anchor_path

    def test_prepare_binds_raw_extract_case_and_blinds_arms(self):
        public = self._prepare()
        self.assertEqual(2, len(public["cells"]))
        self.assertEqual(1, len({c["case_pack_sha256"] for c in public["cells"]}))
        self.assertEqual(2, len({c["cell_input_sha256"] for c in public["cells"]}))
        private = json.loads((self.bundle / "private" / "arm-map.json").read_text())
        self.assertEqual({"O", "Q"}, {c["underlying_arm"] for c in private["cells"]})
        ledger = json.loads((self.bundle / "private" / "source-ledgers" / "R1.json").read_text())
        source = ledger["sources"][0]
        self.assertEqual(freshuse.sha256_file(self.raw), source["raw_sha256"])
        self.assertEqual(freshuse.sha256_bytes(self.extracted), source["extracted_sha256"])
        self.assertEqual("html_visible_text_v1", source["extraction_recipe"]["mode"])
        aids = []
        self.assertIn("Answer in English", public["launch_sentence"])
        for cell in public["cells"]:
            with zipfile.ZipFile(self.bundle / "public" / cell["packet_file"]) as archive:
                aids.append("REASONING_AID.md" in archive.namelist())
                extracted = archive.read("SOURCES/01_official-source.txt")
                self.assertIn(b"Observed condition", extracted)
                self.assertNotIn(b"IGNORE ME", extracted)
                self.assertIn(b"Answer in English", archive.read("START_HERE.md"))
        self.assertEqual([False, True], sorted(aids))
        self._run("verify", "--bundle", self.bundle)

    def test_wrong_raw_hash_fails_before_output(self):
        cfg = json.loads(self.config.read_text())
        cfg["cases"][0]["sources"][0]["raw_sha256"] = "0" * 64
        self.config.write_text(json.dumps(cfg), encoding="utf-8")
        proc = self._run("prepare", "--config", self.config, "--output", self.bundle, ok=False)
        self.assertIn("raw source hash mismatch", proc.stderr)

    def test_record_is_create_only_and_enforces_word_budget(self):
        public = self._prepare()
        alias = public["cells"][0]["cell_alias"]
        receipt = self._complete_receipt(alias)
        answer = self.base / "answer.txt"
        answer.write_text("Bounded action now; revise when evidence changes.\n", encoding="utf-8")
        self._run("record", "--bundle", self.bundle, "--alias", alias, "--receipt", receipt, "--answer", answer)
        duplicate = self._run(
            "record", "--bundle", self.bundle, "--alias", alias, "--receipt", receipt, "--answer", answer, ok=False
        )
        self.assertIn("first-attempt record event already exists", duplicate.stderr)

        other = public["cells"][1]["cell_alias"]
        other_receipt = self._complete_receipt(other)
        long_answer = self.base / "long.txt"
        long_answer.write_text("word " * 701, encoding="utf-8")
        over = self._run(
            "record", "--bundle", self.bundle, "--alias", other, "--receipt", other_receipt,
            "--answer", long_answer, ok=False
        )
        self.assertIn("exceeds 700", over.stderr)

    def test_full_record_score_unmask_and_tamper_detection(self):
        public = self._prepare()
        aliases = [cell["cell_alias"] for cell in public["cells"]]
        for index, alias in enumerate(aliases):
            receipt = self._complete_receipt(alias)
            answer = self.base / f"answer-{index}.txt"
            answer.write_text(f"Action {index}; keep the decision revisable.\n", encoding="utf-8")
            self._run(
                "record", "--bundle", self.bundle, "--alias", alias,
                "--receipt", receipt, "--answer", answer
            )
        score = {
            "schema_version": "1",
            "pilot_id": "test-pilot-001",
            "case_id": "R1",
            "cell_aliases": aliases,
            "scorer_1_identity": "independent-fixture-scorer",
            "scorer_1_project_exposure": "NONE_KNOWN",
            "scorer_2_identity": None,
            "scorer_2_project_exposure": None,
            "criteria": {
                name: {"rating": "NO_MATERIAL_DIFFERENCE", "note": "No material difference in fixture."}
                for name in freshuse.CRITERIA
            },
            "unique_material_error_by_cell": {alias: False for alias in aliases},
            "burden_note": "Equal fixture burden.",
            "provisional_comparison": "NO_MATERIAL_DIFFERENCE",
            "evaluation_limits": "Synthetic tool test only.",
        }
        score_path = self.base / "score.json"
        score_path.write_text(json.dumps(score), encoding="utf-8")
        self._run("score", "--bundle", self.bundle, "--score", score_path)
        anchor_commit, anchor_path = self._anchor_score_token()
        self._run(
            "unmask", "--bundle", self.bundle, "--case", "R1",
            "--anchor-repo", self.repo, "--anchor-commit", anchor_commit,
            "--anchor-path", anchor_path
        )
        unmasked = json.loads((self.bundle / "evidence" / "unmasked" / "R1.json").read_text())
        self.assertEqual({"O", "Q"}, {cell["underlying_arm"] for cell in unmasked["cells"]})
        self.assertIsNone(unmasked["final_disposition"])
        self._run("verify", "--bundle", self.bundle)

        recorded_answer = self.bundle / "evidence" / "answers" / f"{aliases[0]}.txt"
        recorded_answer.write_text("tampered\n", encoding="utf-8")
        tampered = self._run("verify", "--bundle", self.bundle, ok=False)
        self.assertIn("recorded answer missing or changed", tampered.stderr)

    def test_utf8_line_range_extraction_is_exact(self):
        raw = b"one\r\ntwo\r\nthree\r\nfour\r\n"
        result = freshuse.extract_source(
            raw, {"mode": "utf8_line_ranges_v1", "ranges": [[2, 2], [4, 4]]}, "fixture"
        )
        self.assertEqual(b"two\r\nfour\r\n", result)

    def test_html_visible_text_line_ranges_bind_original_html(self):
        raw = (
            b"<html><body><nav>Menu</nav><main><h1>Finding</h1>"
            b"<script>IGNORE ME</script><p>Action remains open.</p></main></body></html>"
        )
        visible = freshuse.extract_source(raw, {"mode": "html_visible_text_v1"}, "fixture")
        lines = visible.decode("utf-8").splitlines()
        selected_line = lines.index("Action remains open.") + 1
        result = freshuse.extract_source(
            raw,
            {
                "mode": "html_visible_text_line_ranges_v1",
                "ranges": [[selected_line, selected_line]],
            },
            "fixture",
        )
        self.assertEqual(b"Action remains open.\n", result)
        self.assertNotIn(b"IGNORE ME", result)

    def test_source_receipt_records_raw_and_extracted_hashes(self):
        receipt = self.base / "source-receipt.json"
        preview = self.base / "preview.txt"
        self._run(
            "source-receipt",
            "--raw", self.raw,
            "--source-identity", "https://example.invalid/source retrieved T0",
            "--display-name", "source.txt",
            "--mode", "html_visible_text_v1",
            "--output", receipt,
            "--extracted-output", preview,
        )
        value = json.loads(receipt.read_text())
        self.assertEqual(freshuse.sha256_file(self.raw), value["raw_sha256"])
        self.assertEqual(freshuse.sha256_file(preview), value["extracted_sha256"])
        self.assertNotIn("IGNORE ME", preview.read_text())
        duplicate = self._run(
            "source-receipt",
            "--raw", self.raw,
            "--source-identity", "same",
            "--display-name", "source.txt",
            "--mode", "identity_v1",
            "--output", receipt,
            ok=False,
        )
        self.assertIn("refusing to overwrite", duplicate.stderr)

    def test_local_event_chain_blocks_deleted_score_redo(self):
        public = self._prepare()
        aliases = [cell["cell_alias"] for cell in public["cells"]]
        for index, alias in enumerate(aliases):
            receipt = self._complete_receipt(alias)
            answer = self.base / f"ordered-answer-{index}.txt"
            answer.write_text("Keep the action bounded and revisable.\n", encoding="utf-8")
            self._run(
                "record", "--bundle", self.bundle, "--alias", alias,
                "--receipt", receipt, "--answer", answer
            )
        score = {
            "schema_version": "1",
            "pilot_id": "test-pilot-001",
            "case_id": "R1",
            "cell_aliases": aliases,
            "scorer_1_identity": "fixture-scorer",
            "scorer_1_project_exposure": "UNKNOWN",
            "scorer_2_identity": None,
            "scorer_2_project_exposure": None,
            "criteria": {
                name: {"rating": "NO_MATERIAL_DIFFERENCE", "note": "Fixture."}
                for name in freshuse.CRITERIA
            },
            "unique_material_error_by_cell": {alias: False for alias in aliases},
            "burden_note": "Fixture.",
            "provisional_comparison": "NO_MATERIAL_DIFFERENCE",
            "evaluation_limits": "Fixture only.",
        }
        score_path = self.base / "ordered-score.json"
        score_path.write_text(json.dumps(score), encoding="utf-8")
        self._run("score", "--bundle", self.bundle, "--score", score_path)
        (self.bundle / "evidence" / "scores" / "R1.blinded.json").unlink()
        redo = self._run("score", "--bundle", self.bundle, "--score", score_path, ok=False)
        self.assertIn("score event already exists", redo.stderr)

    def test_git_anchor_blocks_tail_truncation_score_substitution(self):
        public = self._prepare()
        aliases = [cell["cell_alias"] for cell in public["cells"]]
        for index, alias in enumerate(aliases):
            receipt = self._complete_receipt(alias)
            answer = self.base / f"anchored-answer-{index}.txt"
            answer.write_text("Keep the action bounded and revisable.\n", encoding="utf-8")
            self._run(
                "record", "--bundle", self.bundle, "--alias", alias,
                "--receipt", receipt, "--answer", answer
            )
        score = {
            "schema_version": "1",
            "pilot_id": "test-pilot-001",
            "case_id": "R1",
            "cell_aliases": aliases,
            "scorer_1_identity": "fixture-scorer",
            "scorer_1_project_exposure": "UNKNOWN",
            "scorer_2_identity": None,
            "scorer_2_project_exposure": None,
            "criteria": {
                name: {"rating": "NO_MATERIAL_DIFFERENCE", "note": "Original fixture."}
                for name in freshuse.CRITERIA
            },
            "unique_material_error_by_cell": {alias: False for alias in aliases},
            "burden_note": "Original fixture.",
            "provisional_comparison": "NO_MATERIAL_DIFFERENCE",
            "evaluation_limits": "Fixture only.",
        }
        score_path = self.base / "anchored-score.json"
        score_path.write_text(json.dumps(score), encoding="utf-8")
        self._run("score", "--bundle", self.bundle, "--score", score_path)
        anchor_commit, anchor_path = self._anchor_score_token()

        log_path = self.bundle / "evidence" / "events.jsonl"
        lines = log_path.read_text(encoding="utf-8").splitlines()
        log_path.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
        (self.bundle / "evidence" / "scores" / "R1.blinded.json").unlink()
        (self.bundle / "evidence" / "score-freeze-tokens" / "R1.json").unlink()
        score["burden_note"] = "Substituted fixture."
        score["provisional_comparison"] = "CELL_1_MATERIALLY_BETTER"
        score_path.write_text(json.dumps(score), encoding="utf-8")
        self._run("score", "--bundle", self.bundle, "--score", score_path)
        blocked = self._run(
            "unmask", "--bundle", self.bundle, "--case", "R1",
            "--anchor-repo", self.repo, "--anchor-commit", anchor_commit,
            "--anchor-path", anchor_path, ok=False
        )
        self.assertIn("Git anchor bytes do not match", blocked.stderr)

    def test_event_log_tamper_fails_verification(self):
        self._prepare()
        log_path = self.bundle / "evidence" / "events.jsonl"
        event = json.loads(log_path.read_text().splitlines()[0])
        event["action"] = "tampered"
        log_path.write_text(json.dumps(event) + "\n", encoding="utf-8")
        failed = self._run("verify", "--bundle", self.bundle, ok=False)
        self.assertIn("local event changed after append", failed.stderr)

    def test_receipt_separates_bound_and_attested_claims(self):
        public = self._prepare()
        alias = public["cells"][0]["cell_alias"]
        receipt = self._complete_receipt(alias)
        answer = self.base / "classified-answer.txt"
        answer.write_text("A bounded English answer.\n", encoding="utf-8")
        self._run(
            "record", "--bundle", self.bundle, "--alias", alias,
            "--receipt", receipt, "--answer", answer
        )
        recorded = json.loads(
            (self.bundle / "evidence" / "receipts" / f"{alias}.json").read_text()
        )
        classes = recorded["evidence_classification"]
        self.assertIn("answer_sha256", classes["cryptographically_bound_fields"])
        self.assertIn("receiver_model_version", classes["operator_attested_fields"])
        self.assertEqual(["elapsed_seconds"], classes["derived_from_operator_attestation"])

    def test_non_english_budget_is_rejected(self):
        public = self._prepare()
        alias = public["cells"][0]["cell_alias"]
        receipt_path = self._complete_receipt(alias)
        receipt = json.loads(receipt_path.read_text())
        receipt["answer_language"] = "ja"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        answer = self.base / "non-english-answer.txt"
        answer.write_text("判断を修正可能に保つ。\n", encoding="utf-8")
        failed = self._run(
            "record", "--bundle", self.bundle, "--alias", alias,
            "--receipt", receipt_path, "--answer", answer, ok=False
        )
        self.assertIn("answer_language must be en", failed.stderr)

    def test_zip_collision_preserves_existing_bytes(self):
        target = self.base / "collision.zip"
        target.write_bytes(b"sentinel")
        with self.assertRaises(freshuse.AirlockError):
            freshuse.deterministic_zip(target, {"member.txt": b"new"})
        self.assertEqual(b"sentinel", target.read_bytes())

    def test_native_windows_private_storage_fails_closed(self):
        with self.assertRaisesRegex(freshuse.AirlockError, "PRIVATE_STORAGE_UNVERIFIED"):
            freshuse.require_private_storage(self.base, 0o700, platform_name="nt")


if __name__ == "__main__":
    unittest.main()
