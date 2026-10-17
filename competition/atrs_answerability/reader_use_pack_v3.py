#!/usr/bin/env python3
"""Build reader-use pilot pack v3 from the frozen ATRS evidence.

Repairs the concrete v2 hostile-review findings without running a human study:
- position-balanced schedules (two seeded orders x three condition rotations);
- EXCERPT/LENS information parity (no generated negative-evidence cue);
- route-linked private answer bundles so action/actor/channel/object/status cannot
  be scored as an arbitrary cross-product;
- nine scored cases plus one non-scored missing-field sentinel.

This is method infrastructure only. It is not human evidence.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def _load_base():
    spec = importlib.util.spec_from_file_location("atrs_reader_use_v2", ROOT / "reader_use_pack.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load reader_use_pack.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


base = _load_base()
CONDITIONS = base.CONDITIONS
SEED = base.SEED

# Private, provisional route-linked answer bundles. These are not participant
# materials and require independent human adjudication before any study.
ROUTE_BUNDLES: dict[str, list[dict[str, Any]]] = {
    "hra-proportionate-review": [
        {"next_step":"submit a query about the tool outcome to HRA","actor":"user","channel":"queries@hra.nhs.uk","object_layer":"tool outcome","status":"operating/current"},
        {"next_step":"contact HRA for further advice","actor":"user","channel":"queries@hra.nhs.uk","object_layer":"answering / tool-use guidance","status":"operating/current"},
    ],
    "nhsbsa-residency": [
        {"next_step":"provide documentary evidence of residency","actor":"customer","channel":"documentary evidence process","object_layer":"residency/application process","status":"operating/current"},
        {"next_step":"use the complaints process","actor":"customer","channel":"published complaints-policy URL","object_layer":"residency/application process","status":"operating/current"},
    ],
    "ukho-tidal": [
        {"next_step":"send user feedback through UKHO Customer Services","actor":"user","channel":"https://www.admiralty.co.uk/contact-us","object_layer":"tidal products/services feedback","status":"no formal appeal; feedback route operating/current"},
    ],
    "nsi-polyai": [
        {"next_step":"request a human agent","actor":"customer","channel":"in-channel human-agent request","object_layer":"response/help","status":"no formal appeal for PolyAI; help route described as current"},
        {"next_step":"use other NS&I contact channels","actor":"customer","channel":"other NS&I contact channels","object_layer":"response/help","status":"no formal appeal for PolyAI; help route described as current"},
        {"next_step":"use the standard complaints process and escalation","actor":"customer","channel":"NOT STATED","object_layer":"broader complaint/escalation","status":"complaints/escalation process described as current"},
    ],
    "qcovid": [
        {"next_step":"review the result with a clinician","actor":"patient","channel":"clinician","object_layer":"QCovid result / clarification","status":"review/clarification described as current"},
        {"next_step":"refer to guidance pages for further clarification","actor":"patient","channel":"guidance pages","object_layer":"QCovid result / clarification","status":"review/clarification described as current"},
    ],
    "wilton-data-cleaning": [
        {"next_step":"request removal/deletion of personal data","actor":"individual/customer","channel":"dataprotectionofficer@wiltonpark.org.uk","object_layer":"data use/data rights","status":"operating/current data-removal route"},
    ],
    "cabinet-document-review": [
        {"next_step":"request/receive justification in an appeal or FOI context","actor":"NOT STATED/UNCLEAR","channel":"NOT STATED/UNCLEAR","object_layer":"explanation/justification for deletion; not recovery of deleted file","status":"recovery/reversal unavailable after hard deletion; justification evidence retained"},
    ],
    "darat": [
        {"next_step":"NOT STATED/UNCLEAR","actor":"NOT STATED/UNCLEAR","channel":"NOT STATED/UNCLEAR","object_layer":"review/appeal process not yet defined in the field","status":"planned/not operating; described as part of ethical review"},
    ],
    "national-highways-webchat": [
        {"next_step":"contact National Highways about an incorrect answer, concern or complaint","actor":"user","channel":"https://nationalhighways.co.uk/help-centre/","object_layer":"incorrect webchat answer / concern about operation","status":"operating/current"},
    ],
}


def lens_surface(case: dict[str, Any], row: dict[str, Any]) -> bytes:
    """Same field information as EXCERPT, with token structure only when present."""
    field = row.get("fields", {}).get("appeals_review", {})
    passage = base.appeals_text(row)
    if not field.get("section_present"):
        body = "<h2>Published Appeals and review field</h2><p class='source'>FIELD NOT OBSERVED IN FROZEN PAGE</p>"
    else:
        body = f"<h2>Published Appeals and review passage</h2><p class='source'>{base.esc(passage)}</p>"
        toks = base.field_tokens(row)
        if toks:
            body += "<h2>Published link and contact-like evidence in that passage</h2>"
            body += "<ul class='token-list'>" + "".join(
                f"<li><strong>{base.esc(kind)}</strong>: <code>{base.esc(value)}</code></li>"
                for kind, value in toks
            ) + "</ul>"
    return base.page_shell(case["title"], body)


def build_schedules(scored_cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Two fixed seeded orders, each with all three condition rotations."""
    schedules: list[dict[str, Any]] = []
    for seq in range(6):
        rotation = seq % 3
        order_seed = SEED + seq // 3
        order = [c["case_id"] for c in scored_cases]
        random.Random(order_seed).shuffle(order)
        assignments = {
            c["case_id"]: CONDITIONS[(i + rotation) % 3]
            for i, c in enumerate(scored_cases)
        }
        schedules.append({
            "sequence_id": f"S{seq + 1}",
            "seed": order_seed,
            "cases": [
                {"position": pos, "case_id": case_id, "condition": assignments[case_id]}
                for pos, case_id in enumerate(order, 1)
            ],
        })
    return schedules


def _assert_balanced(schedules: list[dict[str, Any]], scored_cases: list[dict[str, Any]]) -> None:
    case_counts = {c["case_id"]: {cond: 0 for cond in CONDITIONS} for c in scored_cases}
    position_counts = {pos: {cond: 0 for cond in CONDITIONS} for pos in range(1, len(scored_cases) + 1)}
    for schedule in schedules:
        if len(schedule["cases"]) != len(scored_cases):
            raise ValueError("schedule does not contain every scored case")
        for item in schedule["cases"]:
            case_counts[item["case_id"]][item["condition"]] += 1
            position_counts[item["position"]][item["condition"]] += 1
    if any(n != 2 for counts in case_counts.values() for n in counts.values()):
        raise ValueError(f"case/condition imbalance: {case_counts}")
    if any(n != 2 for counts in position_counts.values() for n in counts.values()):
        raise ValueError(f"position/condition imbalance: {position_counts}")


def build(report: dict[str, Any], html_dir: Path, out_dir: Path):
    validated = base.validate(report, html_dir)
    participant_dir = out_dir / "participant_pack"
    private_dir = out_dir / "private_key"
    surface_manifest: dict[str, Any] = {}
    key_cases: list[dict[str, Any]] = []
    scored: list[dict[str, Any]] = []
    sentinel = None

    for case, row, raw in validated:
        payloads = {
            "FULL": base.full_surface(case, row, raw),
            "EXCERPT": base.excerpt_surface(case, row),
            "LENS": lens_surface(case, row),
        }
        targets = {}
        for condition, payload in payloads.items():
            rel = Path("surfaces") / case["case_id"] / f"{condition.lower()}.html"
            digest = base.write_surface(participant_dir / rel, payload)
            targets[condition] = {
                "path": str(rel).replace("\\", "/"),
                "sha256": digest,
                "bytes": len(payload),
            }
        surface_manifest[case["case_id"]] = {
            "title": case["title"],
            "source_sha256": case["source_sha256"],
            "appeals_text_sha256": case["appeals_text_sha256"],
            "targets": targets,
        }
        key_cases.append({
            "case_id": case["case_id"],
            "title": case["title"],
            "primary_scored": case["primary_scored"],
            "published_appeals_text": base.appeals_text(row),
            "route_bundles": ROUTE_BUNDLES.get(case["case_id"], []),
            "limits": case["key"]["limits"],
            "scoring_rule": (
                "Choose one source-supported route bundle where a route is stated; "
                "actor/channel/object/status must correspond to that route. "
                "NOT STATED or UNCLEAR may score only where the selected bundle permits it. "
                "Do not assemble a correct answer by mixing components from different routes."
            ),
            "evidence_rule": "quoted/identified Appeals-field wording must support the chosen route bundle",
        })
        if case["primary_scored"]:
            scored.append(case)
        else:
            sentinel = {
                "case_id": case["case_id"],
                "status": "NON_SCORED_FIELD_ABSENCE_SENTINEL",
                "targets": targets,
            }

    schedules = build_schedules(scored)
    _assert_balanced(schedules, scored)

    manifest = {
        "status": "V3_METHOD_PACK_NO_PARTICIPANT_RESULT",
        "study_scope": "PUBLISHED_APPEALS_AND_REVIEW_FIELD_ONLY",
        "conditions": {
            "FULL": "all frozen main-section text; participant must locate Appeals and review field",
            "EXCERPT": "same Appeals field evidence in a plain isolated excerpt",
            "LENS": "same Appeals field evidence with deterministic grouping of published contact/link tokens when present",
        },
        "information_parity": "EXCERPT and LENS contain the same published Appeals-field passage and the same extracted token values; LENS changes grouping only",
        "primary_contrasts": {
            "FULL_vs_EXCERPT": "field-location/scoping cost",
            "EXCERPT_vs_LENS": "added value of grouping/structure",
            "FULL_vs_LENS": "combined descriptive contrast",
        },
        "tasks": base.TASKS,
        "randomisation_seed_base": SEED,
        "schedules": schedules,
        "surface_manifest": surface_manifest,
        "non_scored_sentinel": sentinel,
        "timing": {
            "network": "offline/local targets only",
            "initial_scroll": 0,
            "outbound_navigation": "disabled/not part of timed task",
            "timer_start": "case target rendered and participant starts case",
            "timer_stop": "response submitted",
            "log": ["sequence", "case", "condition", "position", "completion_status", "elapsed_ms"],
        },
        "ceilings": [
            "METHOD_PACK != HUMAN_RESULT",
            "PROMPTED_FIELD_RETRIEVAL != UNSOLICITED_COMPREHENSION",
            "NINE_PURPOSIVE_CASES != WHOLE_ATRS_REGISTER",
            "ANSWER_KEY != OFFICIAL_INTERPRETATION",
            "NO_HUMAN_DATA_COLLECTED",
            "POSITION_BALANCE != NO_CARRYOVER",
            "EXCERPT ~= LENS -> ROUTE_TO_SIMPLER_OWNER",
        ],
    }
    key = {
        "status": "PRIVATE_PROVISIONAL_ROUTE_LINKED_KEY_REQUIRES_INDEPENDENT_ADJUDICATION_BEFORE_HUMAN_RUN",
        "scored_cases": 9,
        "points_per_scored_case": 6,
        "components": ["next_step", "actor", "channel", "object_layer", "status", "evidence"],
        "route_bundle_rule": "components must come from one source-supported route bundle; arbitrary cross-products are invalid",
        "unsupported_inference_errors": "count separately; do not net against retrieval score",
        "cases": key_cases,
    }

    participant_dir.mkdir(parents=True, exist_ok=True)
    private_dir.mkdir(parents=True, exist_ok=True)
    (participant_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (participant_dir / "TASKS.txt").write_text("\n\n".join(f"{i+1}. {q}" for i, q in enumerate(base.TASKS)) + "\n", encoding="utf-8")
    (private_dir / "answer_key.json").write_text(json.dumps(key, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for schedule in schedules:
        with (participant_dir / f"schedule_{schedule['sequence_id']}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["position", "case_id", "condition", "target_path", "target_sha256"])
            for item in schedule["cases"]:
                target = surface_manifest[item["case_id"]]["targets"][item["condition"]]
                writer.writerow([item["position"], item["case_id"], item["condition"], target["path"], target["sha256"]])
    return manifest, key


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("html_dir", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    manifest, _ = build(report, args.html_dir, args.out_dir)
    print(json.dumps({
        "status": manifest["status"],
        "scored_cases": 9,
        "sentinel": manifest["non_scored_sentinel"]["case_id"],
        "schedules": len(manifest["schedules"]),
        "conditions": list(manifest["conditions"]),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
