#!/usr/bin/env python3
"""Build an evidence-bound ATRS Reader Lens A/B study pack.

This creates method materials only. It does not recruit participants, collect
responses, score people, or establish reader benefit.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

TASKS = [
    "What does the record say someone can do next if they want review, challenge, correction, complaint, clarification, or help?",
    "Who does the record say can take that step? Preserve the role/scope where stated.",
    "How can the step be initiated or reached? If no route/channel is stated, say NOT STATED rather than guessing.",
    "What is being acted on: tool output, broader decision/process, data use, general service/help, explanation/justification, or something else?",
    "Does the record describe the route/process as operating now, unavailable/no separate process, planned/not operating, or unclear?",
    "Identify the exact sentence(s) in the presented record that support your answer.",
]

# The identities below are frozen against the version-aware derived report from
# the preserved September source bytes. Answer-key language remains a bounded
# study adjudication, not an official/legal interpretation of the ATRS record.
CASES: list[dict[str, Any]] = [
    {
        "case_id": "hra-proportionate-review",
        "title": "Health Research Authority: Proportionate Review Toolkit",
        "source_sha256": "5444c3a33252d980ce241070b82c688cc1ab8a556e43620e89dbd1a47655ac1b",
        "appeals_text_sha256": "314c681768aad37f714328b7dd7fe5ed8b698f88f79c13b1a4c0f7d647f51581",
        "answer_key": {
            "next_step": ["submit a query about the tool outcome to HRA", "contact HRA for further advice"],
            "actor": ["user"],
            "channel": ["queries@hra.nhs.uk"],
            "object_layer": ["tool outcome", "answering / tool-use guidance"],
            "status": ["operating/current"],
            "limits": ["source supports review by a senior advisor; it does not by itself establish a statutory appeal right"],
        },
    },
    {
        "case_id": "nhsbsa-residency",
        "title": "NHS BSA: Residency Checker for UK EHIC/GHIC/PRC/S2",
        "source_sha256": "09bf1f39a852befdd89e5a89eed4ce46154b53b54d5ef112599f13dd3bdd9371",
        "appeals_text_sha256": "a2fbc6269da87f18b80b72b2676416b48961dd372df791a25a23a78039b923ba",
        "answer_key": {
            "next_step": ["provide documentary evidence of residency", "use the complaints process"],
            "actor": ["customer"],
            "channel": ["documentary evidence process", "published complaints-policy URL"],
            "object_layer": ["residency/application process"],
            "status": ["operating/current"],
            "limits": ["record does not promise that complaint or evidence will establish entitlement"],
        },
    },
    {
        "case_id": "ukho-tidal",
        "title": "UKHO: Tidal Harmonic Analysis and Prediction",
        "source_sha256": "26c162dc448de2e1025185b8352ed434af57f7a515f318de8b8f7a8c46899c0e",
        "appeals_text_sha256": "62c42010a360985e43657dd512339b75d78f5698015a4d01cf5865d19f62485d",
        "answer_key": {
            "next_step": ["send user feedback through UKHO Customer Services"],
            "actor": ["user"],
            "channel": ["https://www.admiralty.co.uk/contact-us", "UKHO Customer Services"],
            "object_layer": ["tidal products/services feedback"],
            "status": ["no formal appeal; feedback route operating/current"],
            "limits": ["general feedback is not a formal appeal"],
        },
    },
    {
        "case_id": "nsi-polyai",
        "title": "NS&I: PolyAI",
        "source_sha256": "f677262e8da43fcee4360eef421eb72346199bdb37a02e5be7a60ad0ce855e8f",
        "appeals_text_sha256": "22277dc7b924bfd78b011464debd1cca31d4980af25ebcee451567af87c18af9",
        "answer_key": {
            "next_step": ["request a human agent", "use other NS&I contact channels", "use the standard complaints process and escalation"],
            "actor": ["customer"],
            "channel": ["in-channel human-agent request", "other NS&I contact channels", "complaints/escalation process referenced but locator not stated in this field"],
            "object_layer": ["response/help", "broader complaint/escalation"],
            "status": ["no formal appeal for PolyAI; human/help and complaints routes described as current"],
            "limits": ["PolyAI is described as non-binding; no locator for the complaints process appears in this field"],
        },
    },
    {
        "case_id": "qcovid",
        "title": "Department for Health and Social Care and NHS Digital: QCovid algorithm",
        "source_sha256": "b735c1e05831a9f9c2bb37822b312d6041a5e96ee6b3386c96f2a7b57de08783",
        "appeals_text_sha256": "529319f6dff7610f07c83dd89e7f8ff0891a2e1827081e9ed9adec6301b98532",
        "answer_key": {
            "next_step": ["review the result with a clinician", "refer to guidance pages for further clarification"],
            "actor": ["patient"],
            "channel": ["clinician", "guidance pages"],
            "object_layer": ["QCovid result / clarification"],
            "status": ["review/clarification described as current"],
            "limits": ["field does not state a formal appeal process"],
        },
    },
    {
        "case_id": "wilton-data-cleaning",
        "title": "Wilton Park: Data Cleaning Tool",
        "source_sha256": "6b43dcfe84152efb1da3bca5f61492cadc2eace5226234b549a365c19cb6a273",
        "appeals_text_sha256": "fda19b2bb26f709c3b0b7d084c1c57d9c9c9465c992ddbc8ef634f60f37e28d4",
        "answer_key": {
            "next_step": ["request removal/deletion of personal data"],
            "actor": ["individual", "customer"],
            "channel": ["dataprotectionofficer@wiltonpark.org.uk", "privacy policy"],
            "object_layer": ["data use/data rights"],
            "status": ["operating/current data-removal route"],
            "limits": ["relevance to reconsideration of a tool output is not established"],
        },
    },
    {
        "case_id": "cabinet-document-review",
        "title": "Cabinet Office: Automated Digital Document Review",
        "source_sha256": "f6cdd458d9e0e09701540b40f428a5423b636622948b48a90c1743d7f1ee0bf7",
        "appeals_text_sha256": "ea13ffc50581153db63b80a931d07f2b04c97cf95f70a3c04f9368c5f458f330",
        "answer_key": {
            "next_step": ["request/receive justification in an appeal or FOI context"],
            "actor": ["NOT STATED / UNCLEAR"],
            "channel": ["NOT STATED / UNCLEAR"],
            "object_layer": ["explanation/justification for deletion; not recovery of deleted file"],
            "status": ["recovery/reversal unavailable after hard deletion; justification evidence retained"],
            "limits": ["later explanation does not restore the deleted file"],
        },
    },
    {
        "case_id": "darat",
        "title": "Hampshire and Thames Valley Police: DARAT",
        "source_sha256": "9b8c999ef1ab061673350ff191fa48230267698ee4661e8006af9a375c41dc09",
        "appeals_text_sha256": "ad56e92b8738e2440d1cc61aaa3f26e997a82cf86130b1081b86ad54a60056fd",
        "answer_key": {
            "next_step": ["NOT STATED / UNCLEAR"],
            "actor": ["NOT STATED / UNCLEAR"],
            "channel": ["NOT STATED / UNCLEAR"],
            "object_layer": ["review/appeal process not yet defined in the field"],
            "status": ["planned/not operating; described as part of ethical review"],
            "limits": ["future intention must not be scored as an operating route"],
        },
    },
    {
        "case_id": "dbt-find-exporters",
        "title": "DBT: Find Exporters",
        "source_sha256": "4d3df859dd4dac508cf052c3da2e10ba6185f5d9c7e7ba4e2287a3f47103b0d2",
        "appeals_text_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "answer_key": {
            "next_step": ["NOT STATED"],
            "actor": ["NOT STATED"],
            "channel": ["NOT STATED"],
            "object_layer": ["NOT STATED"],
            "status": ["Appeals and review field not observed in frozen record"],
            "limits": ["missing field is not evidence that no review route or practice exists elsewhere"],
        },
    },
    {
        "case_id": "national-highways-webchat",
        "title": "National Highways: Highways Webchat",
        "source_sha256": "cd2918b10c314ca4714822ef6351e76938d09acd40ba3c4bc12766e1b4f86d5f",
        "appeals_text_sha256": "ca00f53b958810aad720c7aba9ccfb74023fada0eb7b2765381ffa498986c161",
        "answer_key": {
            "next_step": ["contact National Highways about an incorrect answer, concern or complaint"],
            "actor": ["user"],
            "channel": ["https://nationalhighways.co.uk/help-centre/", "contact details in explainability statement"],
            "object_layer": ["incorrect webchat answer / concern about operation"],
            "status": ["operating/current"],
            "limits": ["contact route does not by itself establish a formal appeal right"],
        },
    },
]


def appeals_text(row: dict[str, Any]) -> str:
    field = row.get("fields", {}).get("appeals_review", {})
    return " || ".join(str(m.get("text", "")) for m in field.get("matches", []))


def validate(report: dict[str, Any]) -> list[dict[str, Any]]:
    by_title = {str(r.get("title")): r for r in report.get("records", [])}
    selected = []
    for case in CASES:
        row = by_title.get(case["title"])
        if row is None:
            raise ValueError(f"missing frozen case: {case['title']}")
        if row.get("source_sha256") != case["source_sha256"]:
            raise ValueError(f"source identity mismatch: {case['case_id']}")
        actual_appeals_hash = hashlib.sha256(appeals_text(row).encode("utf-8")).hexdigest()
        if actual_appeals_hash != case["appeals_text_sha256"]:
            raise ValueError(f"appeals evidence mismatch: {case['case_id']}")
        selected.append(row)
    return selected


def build(report: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = validate(report)
    manifest_cases = []
    key_cases = []
    for i, (case, row) in enumerate(zip(CASES, rows), start=1):
        manifest_cases.append({
            "order": i,
            "case_id": case["case_id"],
            "title": case["title"],
            "url": row["url"],
            "source_sha256": case["source_sha256"],
            "appeals_text_sha256": case["appeals_text_sha256"],
            "sequence_A_condition": "RAW" if i <= 5 else "LENS",
            "sequence_B_condition": "LENS" if i <= 5 else "RAW",
        })
        key_cases.append({
            "case_id": case["case_id"],
            "title": case["title"],
            "source_sha256": case["source_sha256"],
            "appeals_text_sha256": case["appeals_text_sha256"],
            "published_appeals_text": appeals_text(row),
            "answer_key": case["answer_key"],
        })
    manifest = {
        "status": "METHOD_PACK_NO_PARTICIPANT_RESULT",
        "cases": manifest_cases,
        "tasks": TASKS,
        "ceilings": [
            "TEN_PURPOSIVE_CASES != WHOLE_ATRS_REGISTER",
            "ANSWER_KEY != OFFICIAL_INTERPRETATION",
            "READER_TASK != LEGAL_ADVICE",
            "NO_HUMAN_DATA_COLLECTED",
        ],
    }
    answer_key = {
        "status": "BOUNDED_STUDY_ADJUDICATION_REQUIRES_INDEPENDENT_REVIEW_BEFORE_HUMAN_RUN",
        "cases": key_cases,
        "scoring": {
            "points_per_case": 6,
            "components": ["next_step", "actor", "channel", "object_layer", "status", "evidence"],
            "unsupported_inference_errors": "count separately; do not net against retrieval score",
        },
    }
    return manifest, answer_key


def write_sequences(out_dir: Path, manifest: dict[str, Any]) -> None:
    for seq in ("A", "B"):
        path = out_dir / f"sequence_{seq}.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["order", "case_id", "title", "condition", "source_url"])
            for case in manifest["cases"]:
                writer.writerow([
                    case["order"], case["case_id"], case["title"],
                    case[f"sequence_{seq}_condition"], case["url"],
                ])


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("report", type=Path)
    p.add_argument("--out-dir", type=Path, required=True)
    args = p.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    manifest, key = build(report)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (args.out_dir / "answer_key.json").write_text(json.dumps(key, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_sequences(args.out_dir, manifest)
    print(json.dumps({"cases": len(manifest["cases"]), "tasks": len(manifest["tasks"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
