#!/usr/bin/env python3
"""Unblind and score the frozen EvidenceWatch Brierley retrospective run.

Offline only.

Usage:
  python research/evidencewatch_retrospective/score_brierley_unblinded.py \
    /path/to/pre_unblind_output.json \
    /path/to/evidencewatch_brierley_key.json \
    /path/to/brierley_trivial_baselines.json \
    /path/to/scored_output.json
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

EXPECTED_CASES = 44
POSITIVE = "ABSTRACT_MAJOR_CHANGE"
CONTROL = "ABSTRACT_NO_CHANGE"
PRE_SCHEMA = "evidencewatch-brierley-pre-unblind-output-v1"
KEY_SCHEMA = "evidencewatch-brierley-blinded-key-v1"
BASELINE_SCHEMA = "evidencewatch-brierley-trivial-baselines-v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_rate(numerator: int, denominator: int) -> float | None:
    return None if denominator == 0 else numerator / denominator


def confusion(rows: list[dict], prediction_field: str) -> dict:
    tp = fn = fp = tn = 0
    for row in rows:
        label = row["owner_label"]
        pred = bool(row[prediction_field])
        if label == POSITIVE:
            if pred:
                tp += 1
            else:
                fn += 1
        elif label == CONTROL:
            if pred:
                fp += 1
            else:
                tn += 1
        else:
            raise AssertionError(f"Unexpected owner label: {label}")
    return {
        "tp": tp,
        "fn": fn,
        "fp": fp,
        "tn": tn,
        "positive_n": tp + fn,
        "control_n": fp + tn,
        "sensitivity": safe_rate(tp, tp + fn),
        "false_alert_rate": safe_rate(fp, fp + tn),
        "precision": safe_rate(tp, tp + fp),
    }


def best_baseline_at_far(metric: dict, model_far: float | None) -> dict | None:
    if model_far is None:
        return None
    candidates = []
    for point in metric.get("roc_points", []):
        threshold = point.get("threshold")
        sensitivity = point.get("sensitivity")
        false_alert_rate = point.get("false_alert_rate")
        if threshold is None or sensitivity is None or false_alert_rate is None:
            continue
        if false_alert_rate <= model_far + 1e-12:
            candidates.append(point)
    if not candidates:
        return None
    candidates.sort(
        key=lambda p: (
            -float(p["sensitivity"]),
            float(p["false_alert_rate"]),
            -float(p["threshold"]),
        )
    )
    chosen = candidates[0]
    return {
        "threshold": chosen["threshold"],
        "sensitivity": chosen["sensitivity"],
        "false_alert_rate": chosen["false_alert_rate"],
        "tp": chosen["tp"],
        "fp": chosen["fp"],
        "positive_n": chosen["positive_n"],
        "control_n": chosen["control_n"],
        "comparison_ceiling": "POST_UNBLINDING_DESCRIPTIVE_OPERATING_POINT",
    }


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_pre(pre: dict) -> dict[str, dict]:
    assert pre.get("schema") == PRE_SCHEMA, pre.get("schema")
    assert pre.get("status") == "OUTPUT_FROZEN_BEFORE_OWNER_LABEL_JOIN", pre.get("status")
    assert pre.get("packet", {}).get("case_count") == EXPECTED_CASES
    assert pre.get("provider", {}).get("expected_calls") == EXPECTED_CASES * 2
    assert pre.get("provider", {}).get("observed_calls") == EXPECTED_CASES * 2
    cases = pre.get("cases")
    assert isinstance(cases, list) and len(cases) == EXPECTED_CASES
    out = {}
    for row in cases:
        case_id = row.get("case_id")
        assert case_id and case_id not in out, case_id
        expected_prediction = row.get("successor", {}).get("engine_status") == "MATERIAL_DELTA"
        assert row.get("prediction_review") is expected_prediction, case_id
        out[case_id] = row
    return out


def validate_key(key: dict) -> dict[str, dict]:
    assert key.get("schema") == KEY_SCHEMA, key.get("schema")
    assert key.get("status") == "KEEP_SEPARATE_FROM_ANALYSIS_PATH_UNTIL_UNBLINDING"
    assert key.get("case_count") == EXPECTED_CASES
    rows = key.get("cases")
    assert isinstance(rows, list) and len(rows) == EXPECTED_CASES
    out = {}
    labels = Counter()
    for row in rows:
        case_id = row.get("case_id")
        assert case_id and case_id not in out, case_id
        label = row.get("owner_label")
        assert label in {POSITIVE, CONTROL}, label
        labels[label] += 1
        out[case_id] = row
    assert labels[POSITIVE] == 22, labels
    assert labels[CONTROL] == 22, labels
    return out


def validate_baselines(baseline: dict) -> dict[str, dict]:
    assert baseline.get("schema") == BASELINE_SCHEMA, baseline.get("schema")
    assert baseline.get("status") == "PRE_MODEL_TRIVIAL_BASELINE", baseline.get("status")
    rows = baseline.get("rows")
    assert isinstance(rows, list) and len(rows) == EXPECTED_CASES
    out = {}
    for row in rows:
        doi = row.get("preprint_doi")
        assert doi and doi not in out, doi
        out[doi] = row
    return out


def case_failed(pre_row: dict, receipts: list[dict]) -> tuple[bool, list[str]]:
    reasons = []
    baseline = pre_row.get("baseline", {})
    successor = pre_row.get("successor", {})
    if baseline.get("engine_status") == "ANALYSIS_FAILED" or baseline.get("error"):
        reasons.append("baseline_analysis_failure")
    if successor.get("engine_status") == "ANALYSIS_FAILED" or successor.get("error"):
        reasons.append("successor_analysis_failure")
    for receipt in receipts:
        if receipt.get("ok") is False:
            reasons.append(f"provider_http_{receipt.get('phase') or 'unknown'}_{receipt.get('http_status')}")
    return bool(reasons), sorted(set(reasons))


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    pre_path = Path(sys.argv[1])
    key_path = Path(sys.argv[2])
    baseline_path = Path(sys.argv[3])
    output_path = Path(sys.argv[4])

    if output_path.exists():
        raise AssertionError(f"Refusing to overwrite scored output: {output_path}")

    pre = load_json(pre_path)
    key = load_json(key_path)
    baseline = load_json(baseline_path)

    pre_cases = validate_pre(pre)
    key_cases = validate_key(key)
    baseline_by_doi = validate_baselines(baseline)

    assert set(pre_cases) == set(key_cases), "Pre-unblind output and owner key case IDs differ"

    receipts_by_case: dict[str, list[dict]] = {case_id: [] for case_id in pre_cases}
    for receipt in pre.get("provider_receipts", []):
        case_id = receipt.get("case_id")
        assert case_id in receipts_by_case, case_id
        receipts_by_case[case_id].append(receipt)
    for case_id, receipts in receipts_by_case.items():
        assert len(receipts) == 2, (case_id, len(receipts))

    rows = []
    for case_id in sorted(pre_cases):
        pre_row = pre_cases[case_id]
        key_row = key_cases[case_id]
        owner_label = key_row["owner_label"]
        failed, failure_reasons = case_failed(pre_row, receipts_by_case[case_id])
        output_prediction = bool(pre_row["prediction_review"])

        # Strict failure-worst-case view:
        # - a failed positive cannot be credited as detected;
        # - a failed control is treated as review burden rather than a true quiet negative.
        if failed:
            strict_prediction = owner_label == CONTROL
        else:
            strict_prediction = output_prediction

        doi = key_row["preprint_doi"]
        baseline_row = baseline_by_doi.get(doi)
        assert baseline_row is not None, doi
        assert baseline_row.get("owner_label") == owner_label, (doi, owner_label, baseline_row.get("owner_label"))

        rows.append(
            {
                "case_id": case_id,
                "pair_id": key_row.get("pair_id"),
                "role": key_row.get("role"),
                "owner_label": owner_label,
                "preprint_doi": doi,
                "published_doi": key_row.get("published_doi"),
                "failed": failed,
                "failure_reasons": failure_reasons,
                "output_prediction_review": output_prediction,
                "strict_prediction_review": strict_prediction,
                "baseline_engine_status": pre_row.get("baseline", {}).get("engine_status"),
                "successor_engine_status": pre_row.get("successor", {}).get("engine_status"),
                "successor_relation": pre_row.get("successor", {}).get("relation"),
                "successor_material_reasons": pre_row.get("successor", {}).get("material_reasons", []),
                "successor_alert_kind": pre_row.get("successor", {}).get("alert_kind"),
                "lexical_scores": baseline_row.get("scores"),
                "published_abstract_available_for_lexical_baseline": baseline_row.get("published_abstract_available"),
            }
        )

    raw_metrics = confusion(rows, "output_prediction_review")
    strict_metrics = confusion(rows, "strict_prediction_review")
    available_rows = [row for row in rows if not row["failed"]]
    available_metrics = confusion(available_rows, "output_prediction_review")

    relation_by_label = {
        POSITIVE: Counter(),
        CONTROL: Counter(),
    }
    reason_cases_by_label = {
        POSITIVE: 0,
        CONTROL: 0,
    }
    reason_total_by_label = {
        POSITIVE: 0,
        CONTROL: 0,
    }
    failure_by_label = {
        POSITIVE: 0,
        CONTROL: 0,
    }

    for row in rows:
        label = row["owner_label"]
        relation_by_label[label][str(row.get("successor_relation"))] += 1
        reasons = row.get("successor_material_reasons") or []
        if reasons:
            reason_cases_by_label[label] += 1
            reason_total_by_label[label] += len(reasons)
        if row["failed"]:
            failure_by_label[label] += 1

    lexical_metrics = {}
    for name, metric in baseline.get("metrics", {}).items():
        lexical_metrics[name] = {
            "auc": metric.get("auc"),
            "complete_positive_n": metric.get("complete_positive_n"),
            "complete_control_n": metric.get("complete_control_n"),
            "missing_positive_n": metric.get("missing_positive_n"),
            "missing_control_n": metric.get("missing_control_n"),
            "best_at_or_below_model_strict_far": best_baseline_at_far(
                metric, strict_metrics.get("false_alert_rate")
            ),
        }

    result = {
        "schema": "evidencewatch-brierley-unblinded-score-v1",
        "status": "SCORED_AFTER_OUTPUT_FREEZE",
        "input_sha256": {
            "pre_unblind_output": sha256_file(pre_path),
            "owner_key": sha256_file(key_path),
            "trivial_baselines": sha256_file(baseline_path),
        },
        "source_identities": {
            "evidencewatch": pre.get("evidencewatch"),
            "packet": pre.get("packet"),
            "provider": pre.get("provider"),
            "common_claim": pre.get("common_claim"),
        },
        "headline_strict_failure_worst_case": strict_metrics,
        "raw_output_prediction": raw_metrics,
        "available_case_only": {
            **available_metrics,
            "case_n": len(available_rows),
            "excluded_failure_n": len(rows) - len(available_rows),
            "ceiling": "SECONDARY_VIEW_ONLY_FAILURES_EXCLUDED",
        },
        "failures": {
            "total": sum(row["failed"] for row in rows),
            "by_owner_label": failure_by_label,
        },
        "successor_relation_distribution": {
            label: dict(counter) for label, counter in relation_by_label.items()
        },
        "successor_material_reason_counts": {
            "cases_with_reasons_by_owner_label": reason_cases_by_label,
            "total_reasons_by_owner_label": reason_total_by_label,
        },
        "trivial_lexical_baselines": lexical_metrics,
        "boundaries": [
            "STRICT_FAILURE_WORST_CASE_IS_HEADLINE",
            "AVAILABLE_CASE_METRICS_ARE_SECONDARY",
            "LEXICAL_MATCHED_OPERATING_POINT_IS_POST_UNBLINDING_DESCRIPTIVE",
            "ABSTRACT_MAJOR_CHANGE != CLINICAL_MATERIALITY",
            "RETROSPECTIVE_DISCRIMINATION != REVIEWER_TIME_SAVED",
            "MODEL_ALERT != PRODUCT_VALUE",
        ],
        "cases": rows,
    }

    rendered = json.dumps(result, indent=2) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("x", encoding="utf-8") as handle:
        handle.write(rendered)

    digest = hashlib.sha256(rendered.encode("utf-8")).hexdigest()
    print("PASS")
    print(f"strict_sensitivity={strict_metrics['sensitivity']}")
    print(f"strict_false_alert_rate={strict_metrics['false_alert_rate']}")
    print(f"failures={result['failures']['total']}")
    print(f"scored_output_sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
