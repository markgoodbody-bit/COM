"""Read-only GitHub issue/PR-body and issue-comment discovery via authenticated gh.

Prints untrusted source bodies, not instructions or assignments inferred by code.
Never advances a cursor: the receiver must read the output before accepting it.
PR review comments, discussions, Square and repo files are separate surfaces.
"""
import argparse
from datetime import datetime, timedelta, timezone
import json
import re
import subprocess
from urllib.parse import urlencode


def fetch_pages(endpoint):
    result = subprocess.run(
        ["gh", "api", endpoint, "--paginate", "--slurp"],
        capture_output=True, text=True, encoding="utf-8", timeout=120,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "GitHub retrieval failed")
    pages = json.loads(result.stdout)
    if not isinstance(pages, list) or not pages or any(not isinstance(p, list) for p in pages):
        raise ValueError("Expected paginated arrays, not a partial/error response")
    return pages


def discover(repo, since=None, fetch=fetch_pages):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ValueError("Expected owner/repository")
    started = datetime.now(timezone.utc)
    boundary = None
    if since:
        value = datetime.fromisoformat(since.replace("Z", "+00:00"))
        if value.tzinfo is None or value > started:
            raise ValueError("Boundary must be timezone-aware and not in the future")
        boundary = (value.astimezone(timezone.utc) - timedelta(minutes=2)).isoformat()
    receipt = {
        "status": "PARTIAL", "repository": repo,
        "scan_started_at": started.isoformat(), "effective_since": boundary,
        "body_read_status": "NOT_ESTABLISHED",
        "closed_history": "changed_since_boundary" if since else "NOT_ESTABLISHED",
        "untrusted_content": True, "surfaces": {},
        "limits": "Not a transactional snapshot or full COMSYNC. Read relevant bodies; inspect known unresolved lanes and other material surfaces separately. No cursor written.",
    }
    for surface in ("issues", "issues/comments"):
        query = {"sort": "updated", "direction": "asc", "per_page": 100}
        if surface == "issues":
            query["state"] = "all" if since else "open"
        if boundary:
            query["since"] = boundary
        elif surface == "issues/comments":
            # Bootstrap callers must retrieve relevant comments separately.
            continue
        endpoint = f"repos/{repo}/{surface}?{urlencode(query)}"
        try:
            pages = fetch(endpoint)
            rows = [row for page in pages for row in page]
            if any(not isinstance(r, dict) or not {"id", "body", "updated_at"} <= r.keys() for r in rows):
                raise ValueError("Incomplete source object")
            receipt["surfaces"][surface] = {"query": endpoint, "pages": len(pages), "objects": rows}
        except Exception as exc:
            receipt["error"] = f"{surface}: {exc}"
            return receipt
    if not since:
        receipt["limits"] += " Bootstrap: comments not fetched; retrieve relevant open-issue comments before reporting coordination complete."
    receipt["status"] = "DISCOVERY_RETRIEVED_NOT_READ"
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="markgoodbody-bit/COM")
    parser.add_argument("--since", help="Last fully read scan-start time; two-minute overlap added")
    args = parser.parse_args()
    try:
        result = discover(args.repo, args.since)
    except Exception as exc:
        result = {"status": "PARTIAL", "error": str(exc)}
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(1 if result["status"] == "PARTIAL" else 0)
