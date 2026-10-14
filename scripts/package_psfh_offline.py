#!/usr/bin/env python3
"""Source-only, deterministic, offline PSFH author-review bundle.

Rebases generated static-site links into an extracted file tree; neither
downloads nor publishes. No browser, server, or cloud runtime is invoked.
"""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
from urllib.parse import urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "out"
TARGET = ROOT / "review-artifacts" / "PSFH-complete-offline-review.zip"
DOMAIN = "https://pleasestartfromhere.com"
RELEASE_SHA = "e3267c3e41e7fdfb44c9a9279250a1a7a38d5b9c389a594fef40cfea75fdbe76"
FIGURES = (
    "figure-1-file-and-life.png",
    "figure-2-correction-window.png",
    "figure-3-two-flats-one-wall.png",
    "figure-4-machine-speed-human-correction.png",
)
ATTR = re.compile(r'(?P<name>\b(?:href|src|poster|srcset))(?P<eq>\s*=\s*)(?P<quote>["\'])(?P<value>.*?)(?P=quote)', re.I | re.S)
CSS_URL = re.compile(r'url\(\s*(?P<quote>["\']?)(?P<value>/[^)"\']+)(?P=quote)\s*\)', re.I)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def list_source(site: Path) -> dict[str, bytes]:
    if not site.is_dir():
        raise ValueError("Build the existing generated site first (npm run build)")
    found = {}
    for item in sorted(site.rglob("*")):
        if item.is_symlink():
            raise ValueError("Refusing generated symlink: " + str(item))
        if item.is_file():
            rel = item.relative_to(site).as_posix()
            found[rel] = item.read_bytes()
    essential = {
        "index.html", "style.css", "read/me-v0.8.html",
        "resources/mechanical-ethics/MECHANICAL_ETHICS.md",
        "resources/mechanical-ethics/MECHANICAL_ETHICS.pdf",
        *("resources/mechanical-ethics/figures/" + name for name in FIGURES),
    }
    absent = sorted(essential - found.keys())
    if absent:
        raise ValueError("Incomplete site output: " + ", ".join(absent))
    if digest(found["resources/mechanical-ethics/MECHANICAL_ETHICS.md"]) != RELEASE_SHA:
        raise ValueError("Original released v0.8 Markdown was changed")
    return found


def offline_url(value: str, page: str, inventory: set[str], *, required=False):
    """Return rewritten URL and optional unavailable-local-route string."""
    original = html.unescape(value)
    if original.startswith(DOMAIN):
        path_part = original[len(DOMAIN):]
        if path_part and not path_part.startswith(("/", "?", "#")):
            return value, None
        owned = True
    elif original.startswith("/") and not original.startswith("//"):
        path_part = original
        owned = True
    else:
        return value, None
    parts = urlsplit(path_part)
    raw_path = parts.path or "/"
    normalized = posixpath.normpath(raw_path.lstrip("/"))
    if normalized in (".", ""):
        normalized = "index.html"
    elif raw_path.endswith("/"):
        normalized += "/index.html"
    elif normalized not in inventory and normalized + "/index.html" in inventory:
        normalized += "/index.html"
    elif normalized not in inventory and normalized + ".html" in inventory:
        normalized += ".html"
    if normalized.startswith("../") or normalized == "..":
        raise ValueError("Path traversal in generated site URL: " + original)
    if normalized not in inventory:
        if required:
            raise ValueError("Missing local asset: " + original + " on " + page)
        # Unmirrored same-site destinations remain explicitly ONLINE, not
        # silently broken file:/// links. Record each in the package manifest.
        if owned:
            return DOMAIN + path_part, original
        return value, None
    base = posixpath.dirname(page) or "."
    relative = posixpath.relpath(normalized, base)
    if relative == ".":
        relative = "index.html"
    suffix = ("?" + parts.query if parts.query else "") + ("#" + parts.fragment if parts.fragment else "")
    return relative + suffix, None


def transform_html(content: str, page: str, inventory: set[str]):
    deferred = set()
    # Offline navigation is native HTML. Do not copy the optional hosted
    # history enhancement into the offline first-encounter variant.
    if page == "index.html":
        content = re.sub(r'<script\b[^>]*\bsrc=["\']/?journey\.js["\'][^>]*></script>', "", content, flags=re.I)
    def replace(match):
        key, old = match.group("name").lower(), match.group("value")
        if key == "srcset":
            updated = []
            for portion in old.split(","):
                bits = portion.strip().split(None, 1)
                if not bits:
                    continue
                v, missing = offline_url(bits[0], page, inventory, required=True)
                if missing:
                    deferred.add(missing)
                updated.append(v + (" " + bits[1] if len(bits) > 1 else ""))
            new = ", ".join(updated)
        else:
            new, missing = offline_url(old, page, inventory, required=(key in ("src", "poster")))
            if missing:
                deferred.add(missing)
        return match.group("name") + match.group("eq") + match.group("quote") + html.escape(new, quote=True).replace("&amp;amp;", "&amp;") + match.group("quote")
    return ATTR.sub(replace, content), deferred


def transform_css(content: str, page: str, inventory: set[str]):
    def replace(match):
        revised, _ = offline_url(match.group("value"), page, inventory, required=True)
        quote = match.group("quote")
        return "url(" + quote + revised + quote + ")"
    return CSS_URL.sub(replace, content)


def introduction():
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>PSFH · Complete offline review</title><style>
body{font:1.08rem/1.65 system-ui,sans-serif;max-width:48rem;margin:2rem auto;padding:0 1.2rem;color:#1d2425}
a{color:#164c70}li{margin:.65rem 0}small{color:#485255}
</style></head><body>
<h1>Please Start From Here — offline author review</h1>
<p>The painting-first homepage, original complete story and complete released
Mechanical Ethics v0.8.0 reading edition are together in this extracted folder.
This is an unpublished draft for Mark's editorial judgement, not a live site.</p>
<ol>
<li><a href="site/index.html">Open the proposed human entrance</a> (artwork first; full original story retained)</li>
<li><a href="site/read/me-v0.8.html">Open the complete formatted released book</a> (55 original sections, four figures)</li>
<li><a href="site/resources/mechanical-ethics/MECHANICAL_ETHICS.pdf">Open the original PDF</a>
or <a href="site/resources/mechanical-ethics/MECHANICAL_ETHICS.md">original Markdown</a></li>
</ol>
<p>Extract the ZIP before opening this file; preserve the directory structure.
These local pages and reading materials require no server or account.
Some optional links lead to live sites and need connectivity. The offline
homepage disables the optional navigation enhancement; native links remain.</p>
<p>Review: painting and orientation order; status wording; story-to-book journey;
visual readability; whether the HTML book should be published as a derived view.
Original release status and Mark's publication decision remain unchanged.</p>
<small>Source-generated preview only. Browser keyboard, screen-reader, print
inspection and real reader comprehension are not certified by this package.</small>
</body></html>
"""


def build(site: Path = SITE, output: Path = TARGET):
    source = list_source(site)
    names = set(source)
    copied = {}
    deferred = set()
    for path, raw in source.items():
        if path.endswith(".html"):
            rewritten, outstanding = transform_html(raw.decode("utf-8"), path, names)
            copied["site/" + path] = rewritten.encode("utf-8")
            deferred.update(outstanding)
        elif path.endswith(".css"):
            copied["site/" + path] = transform_css(raw.decode("utf-8"), path, names).encode("utf-8")
        else:
            copied["site/" + path] = raw
    entry = introduction().encode("utf-8")
    copied["OPEN_THIS_FIRST.html"] = entry
    copied["OPEN_THIS_FIRST.txt"] = (
        "Extract the entire ZIP; open OPEN_THIS_FIRST.html. "
        "The complete released ME v0.8 reading edition is site/read/me-v0.8.html. "
        "This is a DRAFT, not a hosted release; optional external links need internet.\n"
    ).encode()
    manifest = {
        "status": "DRAFT_OFFLINE_PREVIEW_NOT_PUBLISHED",
        "released_me_version": "0.8.0",
        "released_markdown_sha256": RELEASE_SHA,
        "original_generated_site_files": len(source),
        "same_site_online_only_optional_links": sorted(deferred),
        "files": {name: digest(raw) for name, raw in sorted(copied.items())},
    }
    copied["MANIFEST_SHA256.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(copied.items()):
            meta = zipfile.ZipInfo(name, (2026, 10, 14, 0, 0, 0))
            meta.compress_type = zipfile.ZIP_DEFLATED
            meta.external_attr = 0o100644 << 16
            archive.writestr(meta, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError("Corrupt offline review archive")
        for name, expected in manifest["files"].items():
            if digest(archive.read(name)) != expected:
                raise ValueError("Archive manifest mismatch: " + name)
    return manifest


if __name__ == "__main__":
    result = build()
    print(json.dumps({
        "artifact": str(TARGET),
        "bytes": TARGET.stat().st_size,
        "sha256": digest(TARGET.read_bytes()),
        "generated_site_files": result["original_generated_site_files"],
        "online_only_optional_links": len(result["same_site_online_only_optional_links"]),
    }, indent=2))
