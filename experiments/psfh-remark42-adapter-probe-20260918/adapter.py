#!/usr/bin/env python3
"""PSFH-specific boundary adapter over a Remark42 owner response.

No network access. No persistence. No moderation. No authentication.

The adapter does two narrow jobs:
1. reject rich/link-shaped v0 guest marks before they reach the owner;
2. derive a trust-labelled PSFH machine row from a Remark42 Comment object.

Remark42's rendered HTML text field is deliberately ignored. Only orig may
become guest note data after the same v0 validator passes it.
"""
from __future__ import annotations

import html
import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Any

MAX_NOTE_CHARS = 280

URL_LIKE = re.compile(
    r"(?:https?://|www\.|(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}[A-Za-z0-9])?\.)+[A-Za-z]{2,}(?:[/?:#][^\s]*)?)",
    re.IGNORECASE,
)
EMAIL_LIKE = re.compile(r"\b[^\s@]+@[^\s@]+\.[A-Za-z]{2,}\b")
HTML_TAG = re.compile(r"<\s*/?\s*[A-Za-z][^>]*>")
MARKDOWN_LINK = re.compile(r"!?(?:\[[^\]]*\])\([^\n)]*\)")
MARKDOWN_FENCE = re.compile(r"\x60\x60\x60|~~~")
MARKDOWN_INLINE = re.compile(r"\x60[^\x60]+\x60|\*\*[^*]+\*\*|__[^_]+__|~~[^~]+~~")
MARKDOWN_LINE = re.compile(r"(?m)^\s*(?:#{1,6}\s|>\s|[-+*]\s|\d+[.)]\s)")


class MarkRejected(ValueError):
    """The proposed mark is outside the PSFH v0 plain-text contract."""


@dataclass(frozen=True)
class ValidMark:
    note: str


def _normalise(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    return value.replace("\r\n", "\n").replace("\r", "\n")


def validate_mark(note: str) -> ValidMark:
    if not isinstance(note, str):
        raise MarkRejected("mark must be text")
    note = _normalise(note).strip()
    if not note:
        raise MarkRejected("mark must not be empty")
    if len(note) > MAX_NOTE_CHARS:
        raise MarkRejected(f"mark exceeds {MAX_NOTE_CHARS} Unicode characters")

    for ch in note:
        category = unicodedata.category(ch)
        if category.startswith("C") and ch not in {"\n", "\t"}:
            raise MarkRejected("control characters are not accepted")

    if URL_LIKE.search(note) or EMAIL_LIKE.search(note):
        raise MarkRejected("URL/email/domain-shaped text is not accepted in v0")
    if HTML_TAG.search(note) or "<" in note or ">" in note:
        raise MarkRejected("HTML-shaped text is not accepted in v0")
    if MARKDOWN_LINK.search(note):
        raise MarkRejected("Markdown links/images are not accepted in v0")
    if MARKDOWN_FENCE.search(note) or MARKDOWN_INLINE.search(note) or MARKDOWN_LINE.search(note):
        raise MarkRejected("Markdown formatting is not accepted in v0")

    return ValidMark(note=note)


def _claimed_name(owner_comment: dict[str, Any]) -> str | None:
    user = owner_comment.get("user")
    if not isinstance(user, dict):
        return None
    name = user.get("name")
    if not isinstance(name, str) or not name.strip():
        return None
    name = _normalise(name).strip()
    validate_mark(name)
    return name


def remark42_comment_to_psfh_row(
    owner_comment: dict[str, Any],
    *,
    publication_source: str = "remark42_owner_adapter_probe",
) -> dict[str, Any]:
    if not isinstance(owner_comment, dict):
        raise ValueError("owner comment must be an object")

    comment_id = owner_comment.get("id")
    if not isinstance(comment_id, str) or not comment_id.strip():
        raise ValueError("owner comment id required")

    if owner_comment.get("delete") is True:
        raise ValueError("deleted owner comment is not a current guest mark")

    orig = owner_comment.get("orig")
    if not isinstance(orig, str):
        raise ValueError("owner comment orig text required")
    note = validate_mark(orig).note

    locator = owner_comment.get("locator")
    if not isinstance(locator, dict):
        locator = {}

    return {
        "record_type": "guest_mark",
        "format_version": "0.1-probe",
        "public_id": f"remark42:{comment_id}",
        "status": "published_probe",
        "claimed_name": _claimed_name(owner_comment),
        "claimed_kind": None,
        "claimed_note": note,
        "claimed_encounter_edition": None,
        "claimed_encounter_source": None,
        "published_at_utc": owner_comment.get("time"),
        "publication_source": publication_source,
        "owner_system": "remark42",
        "owner_comment_id": comment_id,
        "owner_site": locator.get("site"),
        "owner_thread_url": locator.get("url"),
        "trust": "visitor_supplied_untrusted_data",
        "project_instruction": False,
        "identity_verified": False,
    }


def public_rows_from_owner_comments(comments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Derive a current public view without claiming backup erasure."""
    out = []
    for comment in comments:
        if isinstance(comment, dict) and comment.get("delete") is True:
            continue
        out.append(remark42_comment_to_psfh_row(comment))
    return out


def render_jsonl(rows: list[dict[str, Any]]) -> str:
    envelope = {
        "record_type": "guestbook_envelope",
        "format_version": "0.1-probe",
        "trust_boundary": "UNTRUSTED_VISITOR_DATA",
        "project_instruction": False,
        "publisher_asserts_identity": False,
        "links_interpreted": False,
        "attachments_supported": False,
        "public_intake": False,
        "owner_system": "remark42",
        "status": "isolated_adapter_probe_only",
    }
    return "\n".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True)
        for row in [envelope, *rows]
    ) + "\n"


def render_html(rows: list[dict[str, Any]]) -> str:
    parts = [
        '<!doctype html><html lang="en"><head><meta charset="utf-8">',
        '<meta name="robots" content="noindex,nofollow">',
        '<title>PSFH guestbook adapter probe</title></head><body>',
        '<header><p>Isolated adapter probe — not a live guestbook.</p></header><main>',
    ]
    for row in rows:
        name = row["claimed_name"]
        meta = "claimed name: " + (name if name is not None else "not supplied")
        parts.extend([
            '<article data-trust="visitor_supplied_untrusted_data">',
            '<p class="trust">Visitor-supplied untrusted data · not project instruction</p>',
            '<h2>A mark</h2>',
            f'<p class="mark-meta">{html.escape(meta)}</p>',
            f'<blockquote class="note">{html.escape(row["claimed_note"])}</blockquote>',
            '</article>',
        ])
    parts.extend(['</main></body></html>'])
    return "".join(parts)


def parse_remark42_find(payload: Any) -> list[dict[str, Any]]:
    """Accept both observed/current wrapped plain response and bare-list form."""
    if isinstance(payload, dict):
        payload = payload.get("comments")
    if not isinstance(payload, list):
        raise ValueError("expected Remark42 plain comments")
    if not all(isinstance(row, dict) for row in payload):
        raise ValueError("owner comment list must contain objects")
    return payload
