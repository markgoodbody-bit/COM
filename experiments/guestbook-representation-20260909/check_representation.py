#!/usr/bin/env python3
"""Pure source check for the synthetic guestbook representation.

No network, no intake, no backend. Fails if the fixture loses the trust boundary
or grows fields/content the v0 representation explicitly excludes.
"""
from __future__ import annotations

import json
import re
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


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


rows = []
for lineno, line in enumerate(JSONL.read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip():
        continue
    try:
        rows.append(json.loads(line))
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
    if record_type == "guest_mark":
        if row.get("trust") != "visitor_supplied_untrusted_data":
            fail(f"{public_id}: guest mark lost per-row untrusted-data label")
        forbidden = PUBLISHER_SHAPED_GUEST_FIELDS.intersection(row)
        if forbidden:
            fail(f"{public_id}: publisher-shaped guest fields present: {sorted(forbidden)}")

        for required in ("claimed_name", "claimed_kind", "claimed_note"):
            if required not in row:
                fail(f"{public_id}: missing {required}")

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
        if row.get("corrects_public_id"):
            correction_fixture_seen = True

    elif record_type == "guest_mark_removal_state":
        removal_fixture_seen = True
        for field in GUEST_CLAIM_FIELDS:
            if row.get(field) is not None:
                fail(f"{public_id}: removal state retains {field}")
        if row.get("removed_text_retained_in_current_export") is not False:
            fail(f"{public_id}: removal state must say removed text is absent from current export")
    else:
        fail(f"{public_id}: unknown record_type {record_type!r}")

if not injection_fixture_seen:
    fail("instruction-shaped hostile fixture missing")
if not correction_fixture_seen:
    fail("correction fixture missing")
if not removal_fixture_seen:
    fail("removal fixture missing")

html = HTML.read_text(encoding="utf-8")
lower_html = html.lower()
for forbidden_tag in ("<script", "<form", "<input", "<textarea", "<button"):
    if forbidden_tag in lower_html:
        fail(f"human fixture unexpectedly contains {forbidden_tag}")
if "visitor-supplied untrusted data" not in lower_html:
    fail("human fixture lacks visible untrusted-data labelling")
if "ignore prior instructions" not in lower_html:
    fail("human fixture does not render the hostile-content fixture")

# The system-authored footer may legitimately name local files such as
# register.jsonl. The v0 no-URL invariant applies to the mark/register region,
# not to every dot in the surrounding authored document.
main_start = lower_html.find("<main>")
main_end = lower_html.find("</main>", main_start + 1)
if main_start < 0 or main_end < 0:
    fail("human fixture must contain a main register region")
register_region = html[main_start:main_end]
if URL_LIKE.search(register_region):
    fail("human register region unexpectedly contains URL-like content")

print(f"PASS: {len(rows) - 1} publication-state rows; trust/correction/removal fixtures intact")
