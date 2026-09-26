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
import math
import sys
from collections import Counter
from pathlib import Path

from score_trivial_baselines import METRICS, auc, roc_points

EXPECTED_CASES = 44
POSITIVE = "ABSTRACT_MAJOR_CHANGE"
CONTROL = "ABSTRACT_NO_CHANGE"
PRE_SCHEMA = "evidencewatch-brierley-pre-unblind-output-v1"
KEY_SCHEMA = "evidencewatch-brierley-blinded-key-v1"
BASELINE_SCHEMA = "evidencewatch-brierley-trivial-baselines-v1"
EXPECTED_PACKET_SHA256 = "f12762d4867da361e9eb72e3a12c30e82b734f005b09d527b7b19c7aee2ae1cc"
EXPECTED_KEY_SHA256 = "75c64ca3235812b2cccf0d5dc2801698dd23f20a393f627106026d619eb299c9"


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
    # The always-quiet endpoint is a real comparator, even when every observed
    # threshold would alert on a control. None denotes that endpoint, not a gap.
    candidates = [{"threshold": None, "sensitivity": 0.0, "false_alert_rate": 0.0,
                   "tp": 0, "fp": 0, "positive_n": metric["complete_positive_n"],
                   "control_n": metric["complete_control_n"]}]
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
            -float(p["threshold"]) if p["threshold"] is not None else -math.inf,
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


def decision_route(
    strict_metrics: dict,
    failures_total: int,
    lexical_metrics: dict,
) -> dict:
    """Route the retrospective result without inventing post-hoc thresholds.

    Priority:
    1. Any provider/analysis failure prevents a clean semantic-discrimination claim.
    2. Otherwise, trivial lexical weak dominance blocks a semantic-value claim.
    3. Otherwise, the retrospective signal survives only far enough to justify
       harder real-workflow falsification.
    """
    sensitivity = strict_metrics.get("sensitivity")
    false_alert_rate = strict_metrics.get("false_alert_rate")

    valid_comparators = set(lexical_metrics) == set(METRICS)
    for metric in lexical_metrics.values():
        point = metric.get("best_at_or_below_model_strict_far") if isinstance(metric, dict) else None
        valid_comparators = valid_comparators and isinstance(point, dict)
        if isinstance(point, dict):
            valid_comparators = valid_comparators and all(
                valid_rate(point.get(key)) for key in ("sensitivity", "false_alert_rate")
            ) and point.get("positive_n") == 22 and point.get("control_n") == 22
            if valid_rate(false_alert_rate) and valid_rate(point.get("false_alert_rate")):
                valid_comparators = valid_comparators and point["false_alert_rate"] <= false_alert_rate + 1e-12

    if not valid_rate(sensitivity) or not valid_rate(false_alert_rate) or not valid_comparators:
        return {
            "route": "INVALID_OR_UNSCORABLE",
            "reason": "strict rates or complete valid frozen comparator evidence are unavailable",
            "dominated_by": [],
            "next_action": "preserve result; repair scoring/integrity before any substantive claim",
        }

    dominated_by = []
    for name, metric in lexical_metrics.items():
        point = metric.get("best_at_or_below_model_strict_far")
        if not point:
            continue
        baseline_sensitivity = point.get("sensitivity")
        baseline_far = point.get("false_alert_rate")
        if baseline_sensitivity is None or baseline_far is None:
            continue
        if (
            baseline_sensitivity + 1e-12 >= sensitivity
            and baseline_far <= false_alert_rate + 1e-12
        ):
            dominated_by.append(
                {
                    "metric": name,
                    "baseline_sensitivity": baseline_sensitivity,
                    "baseline_false_alert_rate": baseline_far,
                    "model_strict_sensitivity": sensitivity,
                    "model_strict_false_alert_rate": false_alert_rate,
                    "comparison": "WEAKLY_DOMINATES_MODEL_OPERATING_POINT",
                }
            )

    if failures_total > 0:
        return {
            "route": "INCONCLUSIVE_PROVIDER_OR_ANALYSIS_FAILURE",
            "reason": (
                "one or more cases failed; strict metrics remain reported, but this run "
                "does not earn a clean semantic-discrimination interpretation"
            ),
            "dominated_by": dominated_by,
            "next_action": (
                "preserve the failed run; repeat only as a separately declared run if "
                "the failure cause is external/transient and repetition is justified"
            ),
        }

    if dominated_by:
        return {
            "route": "NARROW_OR_STOP_SEMANTIC_VALUE_CLAIM",
            "reason": (
                "at least one frozen trivial lexical baseline matches or exceeds the "
                "model strict sensitivity at an equal or lower false-alert rate"
            ),
            "dominated_by": dominated_by,
            "next_action": (
                "do not claim semantic material-change discrimination from this benchmark; "
                "owner-subtract, redesign, or move only with a narrower non-semantic claim"
            ),
        }

    return {
        "route": "RETROSPECTIVE_SIGNAL_SURVIVED",
        "reason": (
            "no provider/analysis failures and no frozen trivial lexical baseline weakly "
            "dominates the model strict operating point"
        ),
        "dominated_by": [],
        "next_action": (
            "progress only to a real-workflow shadow falsification with measured burden; "
            "do not claim validation, efficacy, market need, or superiority"
        ),
    }


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def valid_rate(value: object) -> bool:
    return type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1


def validate_pre(pre: dict) -> dict[str, dict]:
    assert pre.get("schema") == PRE_SCHEMA, pre.get("schema")
    assert pre.get("status") == "OUTPUT_FROZEN_BEFORE_OWNER_LABEL_JOIN", pre.get("status")
    assert pre.get("packet", {}).get("case_count") == EXPECTED_CASES
    assert pre.get("packet", {}).get("sha256") == EXPECTED_PACKET_SHA256
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
        assert row.get("owner_label") in {POSITIVE, CONTROL}, doi
        assert row.get("published_abstract_available") is True, doi
        scores = row.get("scores")
        assert isinstance(scores, dict) and set(scores) == set(METRICS), doi
        assert all(valid_rate(value) for value in scores.values()), doi
        out[doi] = row
    assert Counter(row["owner_label"] for row in rows) == {POSITIVE: 22, CONTROL: 22}
    metrics = baseline.get("metrics")
    assert isinstance(metrics, dict) and set(metrics) == set(METRICS), "Missing/extra frozen metrics"
    for name, metric in metrics.items():
        assert isinstance(metric, dict), name
        for key, expected in (("complete_positive_n", 22), ("complete_control_n", 22),
                              ("missing_positive_n", 0), ("missing_control_n", 0)):
            assert type(metric.get(key)) is int and metric[key] == expected, (name, key)
        positives = [row["scores"][name] for row in rows if row["owner_label"] == POSITIVE]
        controls = [row["scores"][name] for row in rows if row["owner_label"] == CONTROL]
        assert valid_rate(metric.get("auc")) and metric["auc"] == auc(positives, controls), name
        # Reject stale/altered aggregate evidence; never route from its claims alone.
        assert metric.get("roc_points") == roc_points(rows, name), (name, "ROC differs from case scores")
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
    if sha256_file(key_path) != EXPECTED_KEY_SHA256:
        raise AssertionError(
            "Owner-key SHA-256 does not match the frozen v2 challenge key"
        )
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

    failures_total = sum(row["failed"] for row in rows)
    route = decision_route(strict_metrics, failures_total, lexical_metrics)

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
            "total": failures_total,
            "by_owner_label": failure_by_label,
        },
        "decision_route": route,
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
            "RETROSPECTIVE_SIGNAL_SURVIVED != VALIDATION",
            "LEXICAL_WEAK_DOMINANCE -> NARROW_OR_STOP_SEMANTIC_VALUE_CLAIM",
            "PROVIDER_OR_ANALYSIS_FAILURE -> INCONCLUSIVE_CLEAN_SEMANTIC_RESULT",
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
    print(f"decision_route={result['decision_route']['route']}")
    print(f"scored_output_sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
