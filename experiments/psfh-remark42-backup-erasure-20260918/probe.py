#!/usr/bin/env python3
"""Synthetic Remark42 backup/delete/restore lifecycle probe.

Runs a pinned Remark42 container on loopback, creates a synthetic mark, backs it
up, deletes it from the current store, restores the pre-delete backup, and
records whether the mark reappears.
"""
from __future__ import annotations

import argparse
import gzip
import http.cookiejar
import json
import os
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

THREAD = "https://psfh.invalid/guestbook"
SITE = "psfh"
MARKER = "PSFH_BACKUP_ERASURE_SYNTHETIC_MARK_20260918"
IMAGE = "ghcr.io/umputun/remark42:v1.16.4@sha256:980e0e76a6f241cd181f44c5b4d686f0d8cd7f552e11deb3bdcba223b2c3b866"


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(args, text=True, capture_output=True)
    if check and cp.returncode != 0:
        raise RuntimeError(
            f"command failed ({cp.returncode}): {args!r}\nstdout={cp.stdout}\nstderr={cp.stderr}"
        )
    return cp


def request(opener, url: str, *, method="GET", payload=None, xsrf=None):
    data = None if payload is None else json.dumps(payload).encode()
    headers = {}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    if xsrf:
        headers["X-XSRF-TOKEN"] = xsrf
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with opener.open(req, timeout=10) as resp:
        body = resp.read()
        return resp.status, body


def current_payload(opener, base: str):
    status, body = request(opener, f"{base}/api/v1/find?site={SITE}&url={THREAD}&format=plain")
    if status != 200:
        raise RuntimeError(f"find returned {status}")
    return json.loads(body)


def payload_contains_marker(payload) -> bool:
    return MARKER in json.dumps(payload, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--port", type=int, default=8083)
    args = parser.parse_args()

    container = "psfh-remark42-backup-erasure"
    base = f"http://127.0.0.1:{args.port}"
    result = {
        "format": "psfh-remark42-backup-erasure-probe/0.1",
        "owner_image": IMAGE,
        "marker": MARKER,
        "pre_delete_backup_contains_marker": "NOT_TESTED",
        "current_after_delete_contains_marker": "NOT_TESTED",
        "restored_from_pre_delete_backup_contains_marker": "NOT_TESTED",
        "backup_file_count_at_probe": None,
        "public_deployment": "NOT_ATTEMPTED",
        "real_person_data": False,
    }

    run(["docker", "rm", "-f", container], check=False)
    with tempfile.TemporaryDirectory(prefix="psfh-remark42-erasure-") as td:
        os.chmod(td, 0o777)
        try:
            run([
                "docker", "run", "-d", "--name", container,
                "-p", f"127.0.0.1:{args.port}:8080",
                "-v", f"{td}:/srv/var",
                "-e", f"REMARK_URL={base}",
                "-e", f"SITE={SITE}",
                "-e", "SECRET=psfh-erasure-probe-secret-0123456789abcdef",
                "-e", "AUTH_ANON=true",
                "-e", "ADMIN_PASSWD=psfh-erasure-probe-admin",
                IMAGE,
            ])

            ready = False
            for _ in range(30):
                try:
                    with urllib.request.urlopen(f"{base}/ping", timeout=2) as resp:
                        if resp.status == 200:
                            ready = True
                            break
                except Exception:
                    time.sleep(1)
            if not ready:
                raise RuntimeError("Remark42 did not become ready")

            jar = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
            status, _ = request(opener, f"{base}/auth/anonymous/login?user=erasure_probe&aud={SITE}")
            if status != 200:
                raise RuntimeError(f"anonymous login returned {status}")
            xsrf = next((c.value for c in jar if c.name == "XSRF-TOKEN"), None)

            status, body = request(
                opener,
                f"{base}/api/v1/comment?site={SITE}",
                method="POST",
                xsrf=xsrf,
                payload={"text": MARKER, "locator": {"site": SITE, "url": THREAD}},
            )
            if status != 201:
                raise RuntimeError(f"comment create returned {status}")
            comment = json.loads(body)
            comment_id = comment["id"]

            # Create a native owner backup while the synthetic mark is current.
            run([
                "docker", "exec",
                "-e", "REMARK_URL=http://127.0.0.1:8080",
                container, "backup", "-s", SITE,
            ])
            listed = run([
                "docker", "exec", container, "sh", "-lc",
                "find /srv/var/backup -maxdepth 1 -type f -name '*.gz' -print | sort"
            ]).stdout.splitlines()
            if not listed:
                raise RuntimeError("no native backup file created")
            result["backup_file_count_at_probe"] = len(listed)
            backup_in_container = listed[-1]
            local_backup = Path(td) / "pre-delete-backup.gz"
            run(["docker", "cp", f"{container}:{backup_in_container}", str(local_backup)])
            with gzip.open(local_backup, "rb") as fh:
                backup_bytes = fh.read()
            result["pre_delete_backup_contains_marker"] = MARKER.encode() in backup_bytes

            # Delete from current owner state.
            status, _ = request(
                opener,
                f"{base}/api/v1/comment/{comment_id}?site={SITE}&url={THREAD}",
                method="PUT",
                xsrf=xsrf,
                payload={"text": "", "summary": "synthetic erasure probe", "delete": True},
            )
            if status != 200:
                raise RuntimeError(f"comment delete returned {status}")
            after_delete = current_payload(opener, base)
            result["current_after_delete_contains_marker"] = payload_contains_marker(after_delete)

            # Restore the pre-delete backup and check whether old guest text returns.
            backup_name = Path(backup_in_container).name
            run([
                "docker", "exec",
                "-e", "REMARK_URL=http://127.0.0.1:8080",
                container, "restore", "-f", backup_name, "-s", SITE,
            ])
            time.sleep(0.5)
            after_restore = current_payload(opener, base)
            result["restored_from_pre_delete_backup_contains_marker"] = payload_contains_marker(after_restore)

        finally:
            run(["docker", "logs", container], check=False)
            run(["docker", "rm", "-f", container], check=False)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

    if result["pre_delete_backup_contains_marker"] is not True:
        raise SystemExit("pre-delete backup did not contain marker")
    if result["current_after_delete_contains_marker"] is not False:
        raise SystemExit("current state still contained marker after delete")
    # The restore result is observed, not preordained; either boolean is a valid
    # experiment result. Only require that it was actually measured.
    if not isinstance(result["restored_from_pre_delete_backup_contains_marker"], bool):
        raise SystemExit("restore result was not measured")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
