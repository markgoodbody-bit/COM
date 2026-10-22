#!/usr/bin/env python3
"""Finite, read-only, non-model observations for Framework-Lab.

Local guest evidence only. No GitHub/Cloudflare/provider API, command queue,
credentials, agent wake, continuous model identity, or public publishing.
Requires Python >=3.10, stdlib only.
"""

import argparse
from datetime import datetime, timezone
import ipaddress
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from urllib import error, parse, request

SCHEMA = "workshop-witness.v1"
NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,47}$")
UNIT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.@-]{0,95}\.(service|timer)$")
HEX_SHA = re.compile(r"^[a-f0-9]{40}$")
ALLOWED_UNIT_FIELDS = ("ActiveState", "SubState", "Result")
MAX_ITEMS = 8


class ConfigError(ValueError):
    pass


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = request.build_opener(request.ProxyHandler({}), NoRedirect())


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def safe_name(value):
    if not isinstance(value, str) or not NAME.fullmatch(value):
        raise ConfigError("item name must be a simple identifier")
    return value


def check_url(value):
    if not isinstance(value, str):
        raise ConfigError("probe URL must be a string")
    parts = parse.urlsplit(value)
    if (parts.scheme != "http" or parts.username is not None or
            parts.password is not None or parts.query or parts.fragment):
        raise ConfigError("probe must be unauthenticated HTTP without query or fragment")
    try:
        host = parts.hostname
        port = parts.port
    except ValueError as exc:
        raise ConfigError("invalid local port") from exc
    # Literal loopback only, not localhost, hostnames, proxy or network ranges.
    if host is None or port is None:
        raise ConfigError("probe requires explicit loopback IP and port")
    try:
        ip = ipaddress.ip_address(host)
    except ValueError as exc:
        raise ConfigError("probe must use a numeric loopback IP") from exc
    if host not in ("127.0.0.1", "::1") or not ip.is_loopback:
        raise ConfigError("probe is outside the local loopback allowlist")
    if not parts.path.startswith("/") or ".." in parts.path:
        raise ConfigError("probe path must be absolute and non-traversing")
    return value


def validate(raw):
    if not isinstance(raw, dict) or raw.get("schema") != SCHEMA:
        raise ConfigError("expected schema workshop-witness.v1")
    if set(raw) - {"schema", "probes", "repos", "units", "max_age_seconds"}:
        raise ConfigError("unexpected configuration fields")
    prepared = {"schema": SCHEMA}
    all_names = set()
    for section in ("probes", "repos", "units"):
        things = raw.get(section, [])
        if not isinstance(things, list) or len(things) > MAX_ITEMS:
            raise ConfigError("each section must be a list with no more than 8 items")
        good = []
        for item in things:
            if not isinstance(item, dict):
                raise ConfigError("each configured item must be an object")
            name = safe_name(item.get("name"))
            if name in all_names:
                raise ConfigError("item names must be unique across the snapshot")
            all_names.add(name)
            if section == "probes":
                if set(item) - {"name", "url", "expect"}:
                    raise ConfigError("unexpected probe fields")
                url = check_url(item.get("url"))
                expect = item.get("expect", [200])
                if (not isinstance(expect, list) or not (1 <= len(expect) <= 6)
                        or not all(type(x) is int and 100 <= x <= 599 for x in expect)):
                    raise ConfigError("expect must be a short list of HTTP status integers")
                good.append({"name": name, "url": url, "expect": expect})
            elif section == "repos":
                if set(item) != {"name", "path"}:
                    raise ConfigError("repo requires only name and path")
                path = item.get("path")
                if not isinstance(path, str) or not Path(path).is_absolute():
                    raise ConfigError("repo path must be absolute")
                good.append({"name": name, "path": path})
            else:
                if set(item) != {"name", "unit"} or not isinstance(item.get("unit"), str):
                    raise ConfigError("unit requires only name and unit")
                if not UNIT.fullmatch(item["unit"]):
                    raise ConfigError("unit must be an explicit .timer or .service name")
                good.append({"name": name, "unit": item["unit"]})
        prepared[section] = good
    max_age = raw.get("max_age_seconds", 3600)
    if type(max_age) is not int or not (60 <= max_age <= 86400):
        raise ConfigError("max_age_seconds must be between 60 and 86400")
    prepared["max_age_seconds"] = max_age
    return prepared


def subprocess_read(argv):
    # Wholly fixed executables and argument structure; never a shell.
    try:
        result = subprocess.run(
            argv, shell=False, capture_output=True, text=True,
            timeout=3, check=False,
            env={"PATH": "/usr/bin:/bin", "HOME": "/nonexistent",
                 "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1",
                 "GIT_CONFIG_GLOBAL": "/dev/null"},
        )
        return result.returncode, result.stdout[:2048]
    except (OSError, subprocess.TimeoutExpired):
        return None, ""


def observe_probe(item):
    t0 = time.monotonic()
    result = {"kind": "loopback_http", "name": item["name"],
              "status": "UNKNOWN", "http_code": None, "elapsed_ms": None}
    try:
        req = request.Request(item["url"], method="GET",
                              headers={"User-Agent": "FrameworkWorkshopWitness/0.1"})
        with OPENER.open(req, timeout=2) as resp:
            code = resp.status
            # Do not retain, inspect or reproduce private response content.
            result["http_code"] = code
            result["status"] = "EXPECTED" if code in item["expect"] else "UNEXPECTED"
    except error.HTTPError as exc:
        # Redirects are intentionally not followed. A 302 is not a success.
        result["http_code"] = exc.code
        result["status"] = "UNEXPECTED"
        exc.close()
    except (error.URLError, OSError, ValueError, TimeoutError):
        result["status"] = "UNREACHABLE"
    finally:
        result["elapsed_ms"] = round((time.monotonic() - t0) * 1000)
    return result


def observe_repo(item):
    code, stdout = subprocess_read(
        ["git", "-C", item["path"], "rev-parse", "--verify", "HEAD"])
    sha = stdout.strip()
    ok = code == 0 and HEX_SHA.fullmatch(sha) is not None
    return {"kind": "git_head", "name": item["name"],
            "status": "OBSERVED" if ok else "UNKNOWN",
            "commit": sha if ok else None}


def observe_unit(item):
    code, stdout = subprocess_read(
        ["systemctl", "show", "--no-pager",
         "--property=" + ",".join(ALLOWED_UNIT_FIELDS), item["unit"]])
    data = {}
    if code == 0:
        for line in stdout.splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key in ALLOWED_UNIT_FIELDS and re.fullmatch(r"[A-Za-z0-9_-]{1,48}", value):
                data[key] = value
    return {"kind": "systemd_unit", "name": item["name"],
            "status": "OBSERVED" if code == 0 and "ActiveState" in data else "UNKNOWN",
            "fields": data}


def capture(config):
    start = utc_now()
    checks = []
    for item in config["probes"]:
        checks.append(observe_probe(item))
    for item in config["repos"]:
        checks.append(observe_repo(item))
    for item in config["units"]:
        checks.append(observe_unit(item))
    return {
        "schema": SCHEMA,
        "observed_at_utc": start,
        "finished_at_utc": utc_now(),
        "clock_note": "Guest system UTC clock; not independently attested.",
        "expires_after_seconds": config["max_age_seconds"],
        "evidence_scope": "Read-only local guest sample, NOT a live stream or model presence.",
        "checks": checks,
        "sample_status": "NO_CHECKS_CONFIGURED" if not checks else "OBSERVATIONS_CAPTURED",
        "read_only": True, "agent_queue_started": False,
        "public_action_performed": False,
    }


def markdown(snapshot):
    lines = [
        "# Framework-Lab: latest bounded witness",
        "",
        "This is a dated **local observation**, not live telemetry or an AI conversation.",
        "",
        "Observed UTC: " + snapshot["observed_at_utc"],
        "Expires after: " + str(snapshot["expires_after_seconds"]) + " seconds.",
        "Clock: " + snapshot["clock_note"],
        "",
        "No model, queue, scheduled timer, provider write or public post is started by this script.",
        "",
    ]
    if not snapshot["checks"]:
        lines.append("NO_CHECKS_CONFIGURED — a timestamp alone proves no service health.")
    else:
        for item in snapshot["checks"]:
            label = item["name"]
            if item["kind"] == "loopback_http":
                lines.append("* " + label + ": HTTP " + str(item["http_code"]) +
                             " / " + item["status"] + " (" +
                             str(item["elapsed_ms"]) + " ms)")
            elif item["kind"] == "git_head":
                lines.append("* " + label + ": " + item["status"] + " / " +
                             str(item["commit"] or "no supported HEAD"))
            else:
                lines.append("* " + label + ": " + item["status"] + " / " +
                             json.dumps(item["fields"], sort_keys=True))
    lines += ["", "Before acting: verify source clock, scope, authority and the actual task receipt.",
              "A later reader must recompute age from its own clock; no stale sample is CURRENT merely because a file exists.", ""]
    return "\n".join(lines)


def atomic_write(directory, name, data):
    tmp_name = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=directory, prefix=".partial-", delete=False) as f:
            tmp_name = f.name
            os.chmod(tmp_name, 0o600)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, directory / name)
    finally:
        if tmp_name is not None and os.path.exists(tmp_name):
            os.unlink(tmp_name)


def publish(snapshot, output_dir):
    dest = Path(output_dir)
    if dest.is_symlink():
        raise ConfigError("output directory cannot be a symlink")
    dest.mkdir(parents=True, mode=0o700, exist_ok=True)
    if os.name == "posix":
        if dest.stat().st_uid != os.geteuid() or dest.stat().st_mode & 0o077:
            raise ConfigError("output directory must be owned by caller and private (0700)")
    # latest.json is the authoritative data; markdown is a convenience view.
    atomic_write(dest, "latest.json", json.dumps(snapshot, sort_keys=True, indent=2) + "\n")
    atomic_write(dest, "latest.md", markdown(snapshot))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("operation", choices=["capture"])
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args(argv)
    try:
        config = validate(json.loads(args.config.read_text(encoding="utf-8")))
        snapshot = capture(config)
        publish(snapshot, args.output_dir)
    except (ConfigError, OSError, ValueError, json.JSONDecodeError) as exc:
        print("WITNESS_NOT_WRITTEN: " + str(exc), file=sys.stderr)
        return 2
    print("WITNESS_CAPTURED " + snapshot["observed_at_utc"] +
          " checks=" + str(len(snapshot["checks"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
