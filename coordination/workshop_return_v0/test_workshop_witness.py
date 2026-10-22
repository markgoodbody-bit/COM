#!/usr/bin/env python3
"""Offline tests; no VM, provider, repo write or queue side effect."""

import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

import workshop_witness as witness


class Handler(BaseHTTPRequestHandler):
    calls = []
    def do_GET(self):
        self.calls.append(self.path)
        if self.path == "/jump":
            self.send_response(302)
            self.send_header("Location", "https://example.net/never-follow")
        else:
            self.send_response(200)
        self.end_headers()
        self.wfile.write(b"SECRET-BODY-MUST-NOT-BE-STORED")
    def log_message(self, *args):
        pass


class WitnessTests(unittest.TestCase):
    def make_config(self, **updates):
        raw = {"schema": witness.SCHEMA, "probes": [], "repos": [], "units": []}
        raw.update(updates)
        return witness.validate(raw)

    def test_empty_configuration_proves_no_health(self):
        config = self.make_config()
        snap = witness.capture(config)
        self.assertEqual(snap["sample_status"], "NO_CHECKS_CONFIGURED")
        self.assertTrue(snap["read_only"])
        self.assertFalse(snap["agent_queue_started"])
        self.assertFalse(snap["public_action_performed"])
        self.assertIn("NO_CHECKS_CONFIGURED", witness.markdown(snap))

    def test_invalid_schema_and_unknown_fields(self):
        with self.assertRaises(witness.ConfigError):
            witness.validate({"schema": "different"})
        with self.assertRaises(witness.ConfigError):
            witness.validate({"schema": witness.SCHEMA, "command": "run model"})

    def test_rejects_external_probe_and_proxy_tricks(self):
        for url in ("https://127.0.0.1:8080/health", "http://8.8.8.8:8080/",
                    "http://localhost:8080/", "http://127.0.0.2:8080/",
                    "http://admin:password@127.0.0.1:8080/",
                    "http://127.0.0.1:8080/path?key=x",
                    "http://127.0.0.1:8080/../admin",
                    "http://127.0.0.1:8080",
                    "http://127.0.0.1:8080/#token"):
            with self.subTest(url=url), self.assertRaises(witness.ConfigError):
                self.make_config(probes=[{"name": "x", "url": url}])

    def test_accepts_literal_ipv4_and_ipv6_loopback(self):
        for url in ("http://127.0.0.1:8000/", "http://[::1]:8000/status"):
            self.make_config(probes=[{"name": "x", "url": url}])

    def test_rejects_duplicate_names_and_too_many_items(self):
        with self.assertRaises(witness.ConfigError):
            self.make_config(probes=[{"name": "same", "url": "http://127.0.0.1:8000/"}],
                             units=[{"name": "same", "unit": "abc.service"}])
        with self.assertRaises(witness.ConfigError):
            self.make_config(units=[{"name": "u" + str(n), "unit": "a.timer"}
                                    for n in range(9)])

    def test_rejects_bools_and_flexible_execution(self):
        with self.assertRaises(witness.ConfigError):
            self.make_config(max_age_seconds=True)
        with self.assertRaises(witness.ConfigError):
            self.make_config(probes=[{"name": "p", "url": "http://127.0.0.1:8000/",
                                      "expect": [True]}])
        with self.assertRaises(witness.ConfigError):
            self.make_config(units=[{"name": "unit", "unit": "a.timer; systemctl start x"}])

    def test_local_http_reads_status_but_not_body(self):
        Handler.calls = []
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            port = server.server_port
            conf = self.make_config(probes=[
                {"name": "local", "url": "http://127.0.0.1:" + str(port) + "/ok"},
            ])
            snap = witness.capture(conf)
            self.assertEqual(snap["checks"][0]["status"], "EXPECTED")
            self.assertEqual(snap["checks"][0]["http_code"], 200)
            self.assertEqual(Handler.calls, ["/ok"])
            self.assertNotIn("SECRET-BODY", json.dumps(snap))
        finally:
            server.shutdown()
            server.server_close()

    def test_redirect_to_external_is_not_followed(self):
        Handler.calls = []
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            conf = self.make_config(probes=[
                {"name": "redirect", "url": "http://127.0.0.1:" +
                 str(server.server_port) + "/jump"}])
            obs = witness.capture(conf)["checks"][0]
            self.assertEqual(obs["http_code"], 302)
            self.assertEqual(obs["status"], "UNEXPECTED")
            self.assertEqual(Handler.calls, ["/jump"])
        finally:
            server.shutdown()
            server.server_close()

    def test_unreachable_is_observation_not_false_healthy(self):
        config = self.make_config(probes=[
            {"name": "down", "url": "http://127.0.0.1:1/health"}])
        snap = witness.capture(config)
        self.assertEqual(snap["checks"][0]["status"], "UNREACHABLE")
        self.assertEqual(snap["sample_status"], "OBSERVATIONS_CAPTURED")

    def test_git_and_unit_are_bounded_and_redacted(self):
        with patch.object(witness, "subprocess_read") as proc:
            proc.side_effect = [(0, "a" * 40 + "\n"),
                                (0, "ActiveState=active\nSubState=running\nResult=success\nSecrets=NO\n")]
            cfg = self.make_config(
                repos=[{"name": "project", "path": "/pretend/private/path"}],
                units=[{"name": "watch", "unit": "something.service"}])
            checks = witness.capture(cfg)["checks"]
        self.assertEqual(checks[0]["commit"], "a" * 40)
        self.assertEqual(checks[1]["fields"], {
            "ActiveState": "active", "SubState": "running", "Result": "success"})
        self.assertNotIn("/pretend/private/path", json.dumps(checks))
        self.assertNotIn("NO", json.dumps(checks))
        self.assertEqual(proc.call_count, 2)

    def test_failed_git_unit_do_not_claim_success(self):
        with patch.object(witness, "subprocess_read", return_value=(1, "")):
            checks = witness.capture(self.make_config(
                repos=[{"name": "r", "path": "/missing"}],
                units=[{"name": "s", "unit": "missing.timer"}]))["checks"]
        self.assertEqual([x["status"] for x in checks], ["UNKNOWN", "UNKNOWN"])

    def test_private_atomic_receipt_and_cli(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg = root / "config.json"
            cfg.write_text(json.dumps({"schema": witness.SCHEMA}))
            out = root / "out"
            rc = witness.main(["capture", "--config", str(cfg),
                               "--output-dir", str(out)])
            self.assertEqual(rc, 0)
            data = json.loads((out / "latest.json").read_text())
            self.assertEqual(data["sample_status"], "NO_CHECKS_CONFIGURED")
            self.assertIn("not live telemetry", (out / "latest.md").read_text())
            self.assertFalse(any(x.name.startswith(".partial") for x in out.iterdir()))
            if os.name == "posix":
                self.assertEqual(out.stat().st_mode & 0o077, 0)

    @unittest.skipUnless(os.name == "posix", "POSIX ownership/modes only")
    def test_world_readable_or_symlink_output_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src = root / "out"
            src.mkdir(mode=0o755)
            os.chmod(src, 0o755)
            with self.assertRaises(witness.ConfigError):
                witness.publish(witness.capture(self.make_config()), src)
            link = root / "link"
            link.symlink_to(src, target_is_directory=True)
            with self.assertRaises(witness.ConfigError):
                witness.publish(witness.capture(self.make_config()), link)


if __name__ == "__main__":
    unittest.main()
