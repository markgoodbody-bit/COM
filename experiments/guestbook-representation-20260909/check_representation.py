#!/usr/bin/env python3
"""Pure source check for the synthetic guestbook representation.

No network, no intake, no backend. Checks selected invariants of this fixed
synthetic representation; not a general sanitizer or live-service safety proof.
"""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSONL = ROOT / "register.jsonl"
HTML = ROOT / "register.html"

# Reject explicit URLs as well as bare domain-shaped text that a downstream
# client could autolink. This intentionally also catches domains inside email
# addresses: v0 guest marks have no contact/link field.
URL_LIKE = re.compile(
    r"(?:https?://|www\.|(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}[A-Za-z0-9])?\.)+[A-Za-z]{2,}(?:[/?:#][^\s]*)?)",
    re.IGNORECASE,
)
PUBLISHER_SHAPED_GUEST_FIELDS = {"name", "kind", "note", "encounter_edition", "encounter_source"}
GUEST_CLAIM_FIELDS = (
    "claimed_name",
    "claimed_kind",
    "claimed_note",
    "claimed_encounter_edition",
    "claimed_encounter_source",
)
COMMON_FIELDS = set(GUEST_CLAIM_FIELDS) | {"record_type", "format_version", "public_id", "status", "fixture", "published_at_utc", "publication_source", "trust", "project_instruction", "identity_verified"}
FIELDS_BY_TYPE = {
    "guest_mark": COMMON_FIELDS | {"fixture_role", "corrects_public_id"},
    "guest_mark_removal_state": COMMON_FIELDS | {"removed_public_id", "removal_reason_class", "removed_text_retained_in_current_export"},
}


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


rows = []
for lineno, line in enumerate(JSONL.read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip():
        continue
    try:
        row = json.loads(line)
        if not isinstance(row, dict):
            fail(f"register.jsonl line {lineno} must be an object")
        rows.append(row)
    except json.JSONDecodeError as exc:
        fail(f"register.jsonl line {lineno} is invalid JSON: {exc}")

if not rows or rows[0].get("record_type") != "guestbook_envelope":
    fail("first JSONL row must be guestbook_envelope")

envelope = rows[0]
if envelope.get("trust_boundary") != "UNTRUSTED_VISITOR_DATA":
    fail("envelope trust boundary missing or changed")
if envelope.get("project_instruction") is not False:
    fail("envelope must say project_instruction=false")
if envelope.get("public_intake") is not False:
    fail("prototype must say public_intake=false")

seen_ids: set[str] = set()
earlier_guest_ids: set[str] = set()
removed_ids: set[str] = set()
injection_fixture_seen = False
removal_fixture_seen = False
correction_fixture_seen = False

for row in rows[1:]:
    public_id = row.get("public_id")
    if not isinstance(public_id, str) or not public_id:
        fail("every publication-state row needs a public_id")
    if public_id in seen_ids:
        fail(f"duplicate public_id: {public_id}")
    seen_ids.add(public_id)

    if row.get("project_instruction") is not False:
        fail(f"{public_id}: project_instruction must be false")
    if row.get("identity_verified") is not False:
        fail(f"{public_id}: identity_verified must be false")

    record_type = row.get("record_type")
    if record_type not in FIELDS_BY_TYPE:
        fail(f"{public_id}: unknown record_type {record_type!r}")
    extra = set(row) - FIELDS_BY_TYPE[record_type]
    if extra:
        fail(f"{public_id}: fields outside this synthetic format: {sorted(extra)}")
    if row.get("fixture") is not True or row.get("publication_source") != "synthetic_fixture" or row.get("published_at_utc") is not None:
        fail(f"{public_id}: synthetic-only publication markers required")
    if record_type == "guest_mark":
        if row.get("trust") != "visitor_supplied_untrusted_data":
            fail(f"{public_id}: guest mark lost per-row untrusted-data label")
        forbidden = PUBLISHER_SHAPED_GUEST_FIELDS.intersection(row)
        if forbidden:
            fail(f"{public_id}: publisher-shaped guest fields present: {sorted(forbidden)}")

        for required in ("claimed_name", "claimed_kind", "claimed_note"):
            if not isinstance(row.get(required), str):
                fail(f"{public_id}: {required} must be text")
        for field in GUEST_CLAIM_FIELDS:
            value = row.get(field)
            if value is not None and not isinstance(value, str):
                fail(f"{public_id}: {field} must be text or null")
            if isinstance(value, str) and URL_LIKE.search(value):
                fail(f"{public_id}: URL-like text is not accepted in v0 guest field {field}")

        note = row.get("claimed_note")
        if len(note) > 280:
            fail(f"{public_id}: claimed_note exceeds 280 Unicode characters")

        if public_id == "fixture-injection-001":
            injection_fixture_seen = "ignore prior instructions" in note.lower()
        if "corrects_public_id" in row:
            target = row["corrects_public_id"]
            if not isinstance(target, str) or target not in earlier_guest_ids:
                fail(f"{public_id}: correction must reference an earlier guest row")
            correction_fixture_seen = True
        earlier_guest_ids.add(public_id)

    elif record_type == "guest_mark_removal_state":
        removal_fixture_seen = True
        if row.get("trust") != "system_publication_state":
            fail(f"{public_id}: removal requires system publication-state label")
        target = row.get("removed_public_id")
        if not isinstance(target, str) or not target:
            fail(f"{public_id}: removal requires a removed_public_id")
        removed_ids.add(target)
        for field in GUEST_CLAIM_FIELDS:
            if row.get(field) is not None:
                fail(f"{public_id}: removal state retains {field}")
        if row.get("removed_text_retained_in_current_export") is not False:
            fail(f"{public_id}: removal state must say removed text is absent from current export")
    else:
        fail(f"{public_id}: unknown record_type {record_type!r}")

if removed_ids.intersection(seen_ids):
    fail("removed public id is still present in the current export")
if not injection_fixture_seen:
    fail("instruction-shaped hostile fixture missing")
if not correction_fixture_seen:
    fail("correction fixture missing")
if not removal_fixture_seen:
    fail("removal fixture missing")

class FixtureHTML(HTMLParser):
    """Narrow static-fixture syntax checks, not a browser or CSS safety audit."""
    allowed = {"html", "head", "meta", "title", "style", "body", "header", "p", "h1", "main", "article", "h2", "footer", "code"}
    attributes = {"html": {"lang"}, "meta": {"charset", "name", "content"}}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.article = None
        self.article_count = 0

    def handle_starttag(self, tag, attrs):
        if tag not in self.allowed:
            fail(f"human fixture contains unsupported tag: {tag}")
        for name, value in attrs:
            if name not in self.attributes.get(tag, {"class"}):
                fail(f"human fixture contains unsupported attribute: {tag}.{name}")
        if tag == "article":
            if self.article is not None:
                fail("nested guest articles are not supported")
            removed = "removed" in dict(attrs).get("class", "").split()
            self.article = (removed, [])

    def handle_data(self, data):
        if self.article is not None:
            self.article[1].append(data)

    def handle_endtag(self, tag):
        if tag == "article":
            if self.article is None:
                fail("unmatched guest article end")
            removed, chunks = self.article
            label = "system publication state" if removed else "visitor-supplied untrusted data"
            if label not in " ".join(chunks).lower():
                fail(f"human article lacks its own {label} label")
            self.article_count += 1
            self.article = None


html = HTML.read_text(encoding="utf-8")
parsed = FixtureHTML()
parsed.feed(html)
parsed.close()
if parsed.article is not None or parsed.article_count != 4:
    fail("expected four complete articles in this fixed synthetic fixture")
lower_html = html.lower()
for forbidden_tag in ("<script", "<form", "<input", "<textarea", "<button"):
    if forbidden_tag in lower_html:
        fail(f"human fixture unexpectedly contains {forbidden_tag}")
if "visitor-supplied untrusted data" not in lower_html:
    fail("human fixture lacks visible untrusted-data labelling")
if "ignore prior instructions" not in lower_html:
    fail("human fixture does not render the hostile-content fixture")
if URL_LIKE.search(html):
    fail("human fixture unexpectedly contains URL-like content")

print(f"PASS: {len(rows) - 1} publication-state rows; selected synthetic representation checks passed")
