#!/usr/bin/env python3
"""PSFH D099 read-only deployment diff and rollback preflight. Never publishes."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

EXPECTED_SOURCE_TREE = "4ecd5f564c536c76f62f53606140ac8a27240e20"
EXPECTED_PAGES_COMMIT = "6d52e35be8f7d81ff44c1bbde59c6dd15d719579"
EXPECTED_PAGES_TREE = "60081abd350cf16c04194760fe03b5fce23ca062"
RELEASED_ME_SHA256 = "e3267c3e41e7fdfb44c9a9279250a1a7a38d5b9c389a594fef40cfea75fdbe76"
REQUIRED = (
    "index.html", "read/me-v0.8.html", "explore/yac/index.html",
    "explore/yac/thr/index.html", "explore/challenge.html",
    "explore/challenge-local.html", "resources/mechanical-ethics/MECHANICAL_ETHICS.md",
    "resources/mechanical-ethics/MECHANICAL_ETHICS.pdf",
)
PUBLIC_CUSTODY = (".nojekyll", "CNAME")

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def inspect(site: Path, target: dict, *, public_ref: str, source_tree: str) -> dict:
    if target.get("commit") != EXPECTED_PAGES_COMMIT or target.get("tree") != EXPECTED_PAGES_TREE:
        raise ValueError("Pinned public target snapshot does not match known gh-pages")
    if public_ref != EXPECTED_PAGES_COMMIT:
        raise ValueError("PUBLIC_TARGET_MOVED: read latest gh-pages before proceeding")
    if source_tree != EXPECTED_SOURCE_TREE:
        raise ValueError("Candidate site source tree differs from reviewed PR829 donor")
    if not site.is_dir():
        raise ValueError("Generated out/ directory absent; run npm run build first")
    files = {}
    for path in sorted(site.rglob("*")):
        if path.is_symlink():
            raise ValueError("Site contains symlink: " + str(path))
        if path.is_file():
            name = path.relative_to(site).as_posix()
            files[name] = git_blob(path.read_bytes())
    missing = sorted(set(REQUIRED) - files.keys())
    if missing:
        raise ValueError("Missing first-visit files: " + ", ".join(missing))
    markdown = (site / "resources/mechanical-ethics/MECHANICAL_ETHICS.md").read_bytes()
    if hashlib.sha256(markdown).hexdigest() != RELEASED_ME_SHA256:
        raise ValueError("Released ME v0.8 bytes changed")
    home = (site / "index.html").read_text(encoding="utf-8")
    if not (home.index('class="art-hero"') < home.index('class="human-first-door"') < home.index('id="step-story"')):
        raise ValueError("Painting-first source order lost")
    if not ('href="/explore/challenge-local.html"' in home and "NOT SUBMITTED" in home):
        raise ValueError("Local challenge door/status absent")
    local = (site / "explore/challenge-local.html").read_text(encoding="utf-8")
    if not ("NOT SUBMITTED" in local and "connect-src 'none'; form-action 'none'" in local):
        raise ValueError("Local export could be mistaken for submission")
    yac = (site / "explore/yac/index.html").read_text(encoding="utf-8")
    if 'https://yetanotherclearing.com/' not in yac:
        raise ValueError("YAC direct reading door absent")
    book = (site / "read/me-v0.8.html").read_text(encoding="utf-8")
    if book.count("<h1") < 17 or book.count("<h2") < 38:
        raise ValueError("Complete released book heading coverage lost")
    originals = target.get("files", [])
    previous = {f["path"]: f["sha"] for f in originals}
    if len(previous) != len(originals) or any(len(v) != 40 for v in previous.values()):
        raise ValueError("Target inventory malformed")
    added = sorted(files.keys() - previous.keys())
    removed = sorted(previous.keys() - files.keys())
    modified = sorted(p for p in files.keys() & previous.keys() if files[p] != previous[p])
    unchanged = sorted(p for p in files.keys() & previous.keys() if files[p] == previous[p])
    custody = sorted(set(removed) & set(PUBLIC_CUSTODY))
    return {
        "mode": "DRY_RUN_ONLY_NO_REMOTE_MUTATION",
        "source_tree": source_tree,
        "public_target_commit": public_ref,
        "public_target_tree": target["tree"],
        "source_generated_files": len(files),
        "public_git_files": len(previous),
        "added": added, "modified": modified, "deleted_if_naive_replace": removed,
        "unchanged": unchanged,
        "must_preserve_public_files": custody,
        "operator_gate": "STOP_NO_RELEASE_APPROVAL",
        "rollback_source": {
            "prior_gh_pages_commit": public_ref,
            "prior_git_tree": target["tree"],
            "instruction": "Snapshot and independently re-verify this ref before any authorised publication; a revert/deploy is a separate human-operated act.",
        },
        "limits": [
            "Compares candidate build bytes with pinned gh-pages Git tree, not hosted CDN/current served bytes.",
            "Files missing in out/ are NOT permission to delete public target files.",
            "No browser/keyboard/print/screen-reader acceptance. No human uptake evidence.",
            "No merge, deploy, credentials, provider write or outside contact executed.",
        ],
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("out"))
    parser.add_argument("--target", type=Path, default=Path("review/psfh_release_d099/public_target_git_tree.json"))
    parser.add_argument("--public-ref", default=EXPECTED_PAGES_COMMIT)
    parser.add_argument("--source-tree", default=EXPECTED_SOURCE_TREE)
    parser.add_argument("--output", type=Path, default=Path("review-artifacts/PSFH_D099_RELEASE_REHEARSAL.json"))
    args = parser.parse_args()
    try:
        result = inspect(args.site, json.loads(args.target.read_text(encoding="utf-8")),
                         public_ref=args.public_ref, source_tree=args.source_tree)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in result.items()
                          if k in ("mode", "public_target_commit", "source_generated_files",
                                   "public_git_files", "added", "modified", "deleted_if_naive_replace",
                                   "unchanged", "must_preserve_public_files")}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as err:
        print("STOP, NOT REHEARSED: " + str(err), file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
