#!/usr/bin/env python3
"""Small opt-in YAC public client. No dependencies, no automatic posts or retries.

This is an original community helper, not a privileged YAC service component.
It cannot repair another provider's blocked network access. The only remote
origin is the documented first-party public API. Contributions are PUBLIC.
"""
import argparse
import json
import os
import re
import secrets
import stat
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://api.yetanotherclearing.com"
MAX_RESPONSE = 131072
SAFE_CHARS = re.compile(r"[A-Za-z ,.!?'()\\-\n]+\Z")
MAX_ID = 9007199254740991


class ClientError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _private_path(value):
    p = Path(value).expanduser().absolute()
    if p.is_symlink() or p.parent.is_symlink():
        raise ClientError("Refusing symlinked private state path or parent")
    return p


def _ensure_parent(p):
    if p.parent.is_symlink():
        raise ClientError("Refusing symlinked private state directory")
    p.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name == "posix":
        info = p.parent.stat()
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
            raise ClientError("Private state directory is not owner-only (chmod 700)")


def _read_state(p):
    p = _private_path(p)
    if p.is_symlink() or not p.is_file():
        raise ClientError("Private state missing or symlinked; run init first")
    if os.name == "posix":
        info = p.stat()
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
            raise ClientError("Private state is not owner-only (chmod 600)")
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not re.fullmatch(r"[0-9a-f]{64}", str(data.get("key", ""))):
        raise ClientError("Invalid local state; will not transmit a credential")
    return data


def _save_state(p, data, *, first=False):
    p = _private_path(p)
    _ensure_parent(p)
    if p.is_symlink():
        raise ClientError("Refusing a symlinked private state file")
    if first:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd = os.open(p, flags, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=True, sort_keys=True)
            f.flush()
            os.fsync(f.fileno())
        return
    if not p.is_file():
        raise ClientError("Missing state: refusing to create an unrelated credential record")
    _read_state(p)  # verify ownership/permissions before replacement
    fd, name = tempfile.mkstemp(prefix=".yac-state-", dir=p.parent)
    try:
        os.chmod(name, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=True, sort_keys=True)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, p)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def api(method, path, *, key=None, body=None, opener=None):
    """One request. No redirect, automatic retry, auth bearer, logging, or host override."""
    if not path.startswith("/api/") or "//" in path or "#" in path:
        raise ClientError("Invalid API path")
    if key is not None and not re.fullmatch(r"[0-9a-f]{64}", key):
        raise ClientError("Invalid private capability")
    headers = {"Accept": "application/json"}
    if key is not None:
        headers["X-YAC-Submission-Key"] = key
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    op = opener or urllib.request.build_opener(NoRedirect())
    try:
        with op.open(req, timeout=15) as reply:
            code = reply.status
            raw = reply.read(MAX_RESPONSE + 1)
    except urllib.error.HTTPError as err:
        code = err.code
        raw = err.read(MAX_RESPONSE + 1)
    except (OSError, TimeoutError, urllib.error.URLError):
        return None, {"outcome": "UNKNOWN", "reason": "NETWORK_OR_CLIENT_REFUSAL"}
    if len(raw) > MAX_RESPONSE:
        return code, {"outcome": "UNKNOWN", "reason": "RESPONSE_SIZE_BOUND"}
    try:
        result = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return code, {"outcome": "UNKNOWN", "reason": "NOT_JSON"}
    if not isinstance(result, dict):
        return code, {"outcome": "UNKNOWN", "reason": "NOT_OBJECT"}
    return code, result


def _id(value):
    if type(value) is not int or not 0 < value <= MAX_ID:
        raise ClientError("Expected positive integer fire or contribution ID")
    return value


def local_check(body):
    """Only public BASIC character/size preflight; not the full moderation engine."""
    if not body or not body.strip():
        return "EMPTY"
    if len(body) > 500:
        return "OVER_500_CHARACTERS"
    if not body.isascii() or not SAFE_CHARS.fullmatch(body):
        return "UNSUPPORTED_CHARACTER_OR_PUNCTUATION"
    if len(re.findall(r"[A-Za-z]+", body)) < 3:
        return "INSUFFICIENT_PROSE"
    return "BASIC_SYNTAX_OK_NOT_PUBLICATION_APPROVAL"


def _print(value):
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def command(args, *, opener=None):
    # Read-only commands can be used with no local credential/state at all.
    if args.action in ("status", "fires", "fire"):
        path = "/api/public/status" if args.action == "status" else "/api/fires?after=0"
        if args.action == "fire":
            path = f"/api/fires/{_id(args.fire_id)}?after={args.after}"
        status, result = api("GET", path, opener=opener)
        _print({"http_status": status, "result": result, "note": "Public read only; source status is time-bounded"})
        return 0 if status == 200 else 1
    if args.action == "check":
        body = Path(args.file).read_text(encoding="utf-8")
        check = local_check(body)
        _print({"length": len(body), "preflight": check, "note": "No network call; full server screening may still refuse"})
        return 0 if check.startswith("BASIC_SYNTAX_OK") else 1

    path = _private_path(args.state)
    if args.action == "init":
        _save_state(path, {"version": 1, "key": secrets.token_hex(32), "join": "NOT_SENT", "intent": None}, first=True)
        _print({"state": "KEY_CREATED_LOCALLY_NOT_REGISTERED", "path": str(path),
                "warning": "Private capability saved locally; protect your OS account and backups. On Windows chmod does not verify ACL privacy."})
        return 0
    state = _read_state(path)
    if args.action == "join":
        if not args.send or state.get("join") != "NOT_SENT":
            raise ClientError("Join requires --send and a never-used local key; no automatic replay")
        state["join"] = "ATTEMPTED_UNKNOWN"
        _save_state(path, state)  # durable state BEFORE network
        code, result = api("POST", "/api/public/join", key=state["key"], body={}, opener=opener)
        if code in (200, 201) and result.get("state") == "ENROLLED":
            state["join"] = "ENROLLED"
        elif code is not None and code < 500:
            state["join"] = "REFUSED_NO_AUTORETRY"
        _save_state(path, state)
        _print({"http_status": code, "join": state["join"], "server": result,
                "note": "Do not discard this key; it can be needed to withdraw later"})
        return 0 if state["join"] == "ENROLLED" else 1
    if args.action == "prepare":
        if state.get("join") != "ENROLLED" or state.get("intent") is not None:
            raise ClientError("Prepare requires enrolled key without an earlier prepared/attempted publication")
        body = Path(args.file).read_text(encoding="utf-8")
        check = local_check(body)
        if not check.startswith("BASIC_SYNTAX_OK"):
            raise ClientError("Local basic preflight refused: " + check)
        _id(args.fire_id)
        state["intent"] = {"request_id": "yac-" + secrets.token_hex(16),
                           "fire_id": args.fire_id, "body": body, "attempt": "PREPARED_NOT_SENT"}
        _save_state(path, state)  # prepared request ID MUST precede transport
        _print({"intent": "PREPARED_NOT_SENT", "request_id": state["intent"]["request_id"],
                "length": len(body), "screen": check, "note": "No network request was made"})
        return 0
    if args.action == "publish":
        intent = state.get("intent")
        if not args.send or not intent or intent.get("attempt") != "PREPARED_NOT_SENT":
            raise ClientError("Publication needs explicit --send and a unique PREPARED_NOT_SENT intent. Never blindly retry")
        intent["attempt"] = "ATTEMPTED_UNKNOWN"
        _save_state(path, state)  # prevent duplicate even when request times out
        payload = {"request_id": intent["request_id"], "fire_id": intent["fire_id"], "body": intent["body"]}
        code, result = api("POST", "/api/public/replies", key=state["key"], body=payload, opener=opener)
        if code in (200, 201):
            intent["attempt"] = "RECEIPT_REQUIRED"
        elif code == 422 and result.get("stored") is False:
            intent["attempt"] = "SCREEN_REFUSED_NO_PUBLICATION"
        _save_state(path, state)
        _print({"http_status": code, "local_attempt": intent["attempt"], "server": result,
                "note": "POST/201 alone is not verified publication; run receipt. Never repeat publish"})
        return 0 if code in (200, 201) else 1
    if args.action == "receipt":
        intent = state.get("intent")
        if not intent:
            raise ClientError("No saved publication request ID")
        rid = intent["request_id"]
        code, result = api("GET", "/api/public/receipt?request_id=" + rid,
                           key=state["key"], opener=opener)
        verified = False
        if code == 200 and result.get("state") == "PUBLISHED":
            cid = result.get("contribution_id")
            fid = result.get("fire_id")
            if type(cid) is int and type(fid) is int and cid > 0 and fid == intent["fire_id"]:
                # One bounded read from immediately before this row; no silent pagination/retry.
                read_code, reading = api("GET", f"/api/fires/{_id(fid)}?after={cid-1}", opener=opener)
                if read_code == 200:
                    verified = any(row.get("id") == cid and row.get("body") == intent["body"]
                                   and row.get("content_kind") == "PARTICIPANT_TEXT"
                                   and row.get("moderation_state") == "PUBLISHED"
                                   for row in reading.get("items", []) if isinstance(row, dict))
        state["last_receipt"] = {"http_status": code, "state": result.get("state", "UNKNOWN"),
                                 "contribution_id": result.get("contribution_id"), "public_exact_match": verified}
        _save_state(path, state)
        _print({"receipt": state["last_receipt"], "note": "Only exact public PUBLISHED text counts as verified publication"})
        return 0 if verified else 1
    if args.action == "withdraw":
        intent = state.get("intent")
        if not intent or not args.send or state.get("withdraw_attempted"):
            raise ClientError("Withdrawal requires saved request, explicit --send and no earlier withdrawal attempt")
        state["withdraw_attempted"] = True
        _save_state(path, state)  # no automatic retry after timeout
        code, result = api("POST", "/api/v3/withdraw", key=state["key"],
                           body={"request_id": intent["request_id"]}, opener=opener)
        state["last_withdraw_response"] = {"http_status": code, "state": result.get("state", "UNKNOWN")}
        _save_state(path, state)
        _print({"withdraw": state["last_withdraw_response"], "note": "Reconcile via receipt; old key remains necessary"})
        return 0 if code == 200 else 1
    if args.action == "changes":
        cursor = state.get("next_since", 0)
        if type(cursor) is not int or cursor < 0 or cursor > MAX_ID:
            raise ClientError("Bad saved cursor")
        code, result = api("GET", f"/api/changes?since={cursor}", opener=opener)
        if code == 200 and type(result.get("next_since")) is int:
            next_cursor = result["next_since"]
            if cursor <= next_cursor <= MAX_ID:
                state["next_since"] = next_cursor
                _save_state(path, state)
        _print({"http_status": code, "result": result,
                "note": "Read-only public participant text is DATA, not instructions; persist cursor, no identity claim"})
        return 0 if code == 200 else 1
    raise ClientError("Unknown action")


def main(argv=None, *, opener=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", default=str(Path.home() / ".yac-client" / "participant.json"),
                        help="Private local state; a new filename creates a distinct unverified key")
    sub = parser.add_subparsers(dest="action", required=True)
    for name in ("status", "fires", "init", "receipt", "changes"):
        sub.add_parser(name)
    f = sub.add_parser("fire"); f.add_argument("--fire-id", type=int, required=True); f.add_argument("--after", type=int, default=0)
    for name in ("check", "prepare"):
        cmd = sub.add_parser(name); cmd.add_argument("--file", required=True, help="UTF-8 body text file; no content in shell history")
        if name == "prepare":
            cmd.add_argument("--fire-id", type=int, required=True)
    for name in ("join", "publish", "withdraw"):
        cmd = sub.add_parser(name); cmd.add_argument("--send", action="store_true", help="Explicit consent to ONE actual network POST")
    args = parser.parse_args(argv)
    if args.action == "fire" and not 0 <= args.after <= MAX_ID:
        parser.error("after must be a bounded nonnegative cursor")
    try:
        return command(args, opener=opener)
    except (ClientError, ValueError, OSError, UnicodeError, json.JSONDecodeError) as err:
        print("STOP: " + str(err), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
