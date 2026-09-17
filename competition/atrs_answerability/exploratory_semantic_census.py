#!/usr/bin/env python3
"""Framework post-pilot exploratory coding for the frozen September ATRS witness.

This coding was produced AFTER the preregistered pilot and must not be treated
as the preregistered primary result or validated ground truth. Labels may
co-occur and attach to propositions within a field rather than replacing the
field with one state. It exists to falsify the #364 research lead before
November, not to create a transparency/compliance score.

Expected input: atrs_full.json from run 35257984573 / source head
4a7b43df95a2b776b885f8ee903d929100414af7.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

EXPECTED_RECORDS = 152
EXPECTED_APPEALS = 151
EXPECTED_APPEALS_TITLE_SEQUENCE_SHA256 = "dde867019a5c2f5dcac7212c8d3e96fd414a0395cedc0e6f99701c332d1bf517"
EXPECTED_APPEALS_EVIDENCE_SHA256 = "b971a4fe5679b2b2f50a03605c519573f688444266f01f28b8902290f6ef8c9f"
LABEL_UNIT = "proposition_within_field"

LABELS = {
    "PUBLIC_INITIATION": "one proposition gives an eligible non-internal actor a concrete initiation instruction/channel or in-channel action for review, appeal, complaint, challenge or reconsideration; actor scope must be preserved",
    "PROCESS_REFERENCE": "one proposition references an existing review/appeal/complaints process, mechanism or right without necessarily giving a concrete initiation instruction/channel",
    "HELP_FEEDBACK": "one proposition gives general help, feedback, bug-reporting, ordinary contact or customer-service rather than clear reconsideration",
    "IN_CHANNEL_HANDOFF": "one proposition says the interaction itself offers or routes to a human",
    "INTERNAL_REVIEW": "one proposition describes human/internal QA, checking or professional review without a public-initiation claim",
    "NO_SEPARATE": "one proposition says no separate/tool-specific process or relevant decision exists, or marks review/appeal not applicable; proposition-scoped and does not negate broader rights/review elsewhere in the field",
    "SELF_CORRECTION": "one proposition says the user can edit, retry, rephrase or use an alternate path rather than appeal",
    "DATA_RIGHTS": "one proposition describes a data access/removal/privacy action",
    "REFUSAL_OR_OPT_OUT": "one proposition says a person can refuse or opt out of the tool/service/data use, preserving the stated scope",
    "EXPLANATION_ONLY": "one proposition describes audit/explanation/justification without recovery/reversal in that proposition; it does not negate recovery or review elsewhere in the field",
    "PLANNED_NOT_OPERATING": "one proposition says a review/appeal process is planned, under design, or not operating yet",
    "AMBIGUOUS": "scope/relevance cannot be resolved from the published wording without material inference",
}

# Coding is stored by frozen appeals-record index after evidence-identity
# validation. This remains exploratory. Hostile-review corrections below are
# record-specific bounded repairs, not a claim that the remaining census has
# been independently validated.
LABEL_INDICES = {
    "AMBIGUOUS": [38,116,144,148],
    "DATA_RIGHTS": [116,119],
    "EXPLANATION_ONLY": [52,144],
    "HELP_FEEDBACK": [20,29,30,31,35,36,37,42,44,46,49,55,60,65,69,79,81,82,85,86,90,91,96,103,104,105,106,107,108,110,112,113,118,129,130,131,133,134,139,140,145],
    "INTERNAL_REVIEW": [2,12,28,35,38,45,50,52,54,59,62,68,69,72,74,92,98,99,100,104,111,113,132,134,137,139,142,150],
    "IN_CHANNEL_HANDOFF": [0,25,31,39,47,63,96,129,131],
    "NO_SEPARATE": [0,1,2,3,4,5,6,7,9,10,11,13,14,15,20,21,22,23,24,25,26,27,28,29,30,32,38,39,41,43,44,47,51,52,53,55,56,57,58,60,61,63,66,67,68,69,73,76,80,88,89,91,94,98,99,100,119,120,122,125,126,127,132,135,136,138,141,143,144,147,149],
    "PLANNED_NOT_OPERATING": [148],
    "PROCESS_REFERENCE": [4,8,12,16,17,18,19,29,30,34,38,41,45,48,52,54,63,68,70,74,75,76,77,78,83,87,88,91,93,95,97,101,102,104,111,114,115,117,123,124,128,146],
    "PUBLIC_INITIATION": [12,13,16,17,18,19,34,48,50,59,70,71,72,74,75,83,84,87,92,93,97,101,102,109,110,114,115,121,123,128,133,137,142],
    "REFUSAL_OR_OPT_OUT": [33,119,124],
    "SELF_CORRECTION": [40,44,46,64,78,82,88],
}

CEILINGS = [
    "EXPLORATORY_CODING != PREREGISTERED_PRIMARY_RESULT",
    "FRAMEWORK_LABEL != VALIDATED_CLASSIFICATION",
    "LABEL_COUNT != QUALITY_SCORE",
    "LABELS_MAY_CO_OCCUR",
    "LABEL_ON_ONE_PROPOSITION != WHOLE_FIELD_STATE",
    "NO_SEPARATE != NO_INTERNAL_REVIEW_OR_RIGHTS",
    "PROCESS_REFERENCE != EFFECTIVE_REMEDY",
    "PLANNED_PROCESS != OPERATING_ROUTE",
    "ACTOR_SCOPE_MATTERS",
    "BOUNDED_REVIEW_REPAIR != FULL_CENSUS_VALIDATION",
]


def appeals_rows(report: dict) -> list[dict]:
    return [
        row for row in report.get("records", [])
        if row["fields"]["appeals_review"]["section_present"]
    ]


def appeals_evidence_digest(report: dict) -> str:
    """Bind the evidence actually used by this exploratory coding.

    The digest covers ordered title, URL, source hash and the complete extracted
    Appeals and review field. It intentionally does not claim to bind unrelated
    fields that this coding does not use.
    """
    payload = [
        {
            "title": row["title"],
            "url": row["url"],
            "source_sha256": row.get("source_sha256"),
            "appeals_review": row["fields"]["appeals_review"],
        }
        for row in appeals_rows(report)
    ]
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def encode(report: dict) -> dict:
    if len(report.get("records", [])) != EXPECTED_RECORDS:
        raise ValueError("not the frozen 152-record witness")
    appeals = appeals_rows(report)
    if len(appeals) != EXPECTED_APPEALS:
        raise ValueError("unexpected appeals-field membership")
    title_hash = hashlib.sha256("\n".join(r["title"] for r in appeals).encode()).hexdigest()
    if title_hash != EXPECTED_APPEALS_TITLE_SEQUENCE_SHA256:
        raise ValueError("frozen appeals title/order identity mismatch")
    evidence_hash = appeals_evidence_digest(report)
    if evidence_hash != EXPECTED_APPEALS_EVIDENCE_SHA256:
        raise ValueError("frozen appeals evidence identity mismatch")

    by_index = {i: [] for i in range(EXPECTED_APPEALS)}
    for label, indices in LABEL_INDICES.items():
        if label not in LABELS:
            raise ValueError(f"unknown label {label}")
        for i in indices:
            if not 0 <= i < EXPECTED_APPEALS:
                raise ValueError(f"bad index {i}")
            by_index[i].append(label)
    if any(not labels for labels in by_index.values()):
        raise ValueError("every appeals record must have at least one exploratory label")

    records = []
    for i, row in enumerate(appeals):
        field = row["fields"]["appeals_review"]
        records.append({
            "index": i,
            "title": row["title"],
            "url": row["url"],
            "labels": sorted(by_index[i]),
            "evidence_text": " || ".join(m["text"] for m in field["matches"]),
            "source_sha256": row.get("source_sha256"),
        })
    counts = Counter(label for row in records for label in row["labels"])
    return {
        "status": "FRAMEWORK_EXPLORATORY_POST_PILOT_CODING_NOT_VALIDATED_GROUND_TRUTH",
        "source_run": 35257984573,
        "source_head": "4a7b43df95a2b776b885f8ee903d929100414af7",
        "evidence_sha256": evidence_hash,
        "label_unit": LABEL_UNIT,
        "records_with_appeals_field": len(records),
        "labels": LABELS,
        "label_counts": dict(sorted(counts.items())),
        "records": records,
        "ceilings": CEILINGS,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("report", type=Path)
    p.add_argument("--json-out", type=Path)
    p.add_argument("--csv-out", type=Path)
    a = p.parse_args()
    result = encode(json.loads(a.report.read_text(encoding="utf-8")))
    if a.json_out:
        a.json_out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        print(json.dumps({"records": result["records_with_appeals_field"], "label_counts": result["label_counts"]}, indent=2))
    if a.csv_out:
        with a.csv_out.open("w", newline="", encoding="utf-8") as h:
            w = csv.writer(h)
            w.writerow(["index", "title", "url", "labels", "source_sha256"])
            for row in result["records"]:
                w.writerow([row["index"], row["title"], row["url"], ";".join(row["labels"]), row["source_sha256"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
