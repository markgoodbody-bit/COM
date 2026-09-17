#!/usr/bin/env python3
"""100 bounded falsification probes for ATRS Answerability Audit #364.

These probes attack four layers separately:
  25 evidence/provenance binding
  25 parser/extraction robustness
  25 exploratory semantic-codebook consistency
  25 claim/drift ceilings

Passing this file is not validation. A red probe is evidence to repair/shrink.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


audit = load("atrs_falsify_audit", "audit.py")
semantic = load("atrs_falsify_semantic", "exploratory_semantic_census.py")
README = (ROOT / "README.md").read_text(encoding="utf-8")

RESULTS: list[tuple[str, bool, str]] = []


def probe(name: str, condition: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(condition), detail))


def labels(index: int) -> set[str]:
    return {label for label, indices in semantic.LABEL_INDICES.items() if index in indices}


def synthetic_report() -> dict:
    records = []
    for i in range(152):
        present = i < 151
        field = {
            "section_present": present,
            "match_count": 1 if present else 0,
            "contains_none_or_na_phrase": False,
            "syntactic_contact_token_present": False,
            "matches": ([{
                "level": "h3",
                "heading": "3.5 - Appeals and review",
                "text": f"evidence text {i}",
                "characters": len(f"evidence text {i}"),
                "contains_none_or_na_phrase": False,
                "contact_tokens": {
                    "hrefs": [], "urls_in_text": [], "emails": [], "phones": [],
                    "syntactic_contact_token_present": False,
                },
            }] if present else []),
        }
        records.append({
            "title": f"synthetic-{i:03d}",
            "url": f"https://example.test/atrs/{i:03d}",
            "source_sha256": hashlib.sha256(f"source-{i}".encode()).hexdigest(),
            "fields": {"appeals_review": field},
        })
    return {"records": records}


# ---------------------------------------------------------------------------
# A. 25 evidence/provenance binding probes
# ---------------------------------------------------------------------------
base = synthetic_report()
appeals = [r for r in base["records"] if r["fields"]["appeals_review"]["section_present"]]
semantic.EXPECTED_APPEALS_TITLE_SEQUENCE_SHA256 = hashlib.sha256(
    "\n".join(r["title"] for r in appeals).encode()
).hexdigest()

binding_available = hasattr(semantic, "appeals_evidence_digest") and hasattr(
    semantic, "EXPECTED_APPEALS_EVIDENCE_SHA256"
)
if binding_available:
    semantic.EXPECTED_APPEALS_EVIDENCE_SHA256 = semantic.appeals_evidence_digest(base)

mutation_specs: list[tuple[str, int, str]] = []
for i in range(5):
    mutation_specs.append(("text", i, f"mutated text {i}"))
for i in range(5, 10):
    mutation_specs.append(("source_sha", i, "0" * 64))
for i in range(10, 15):
    mutation_specs.append(("url", i, f"https://evil.invalid/{i}"))
for i in range(15, 20):
    mutation_specs.append(("href", i, f"https://elsewhere.invalid/{i}"))
for i in range(20, 25):
    mutation_specs.append(("extra_match", i, f"second evidence {i}"))

for n, (kind, idx, value) in enumerate(mutation_specs, start=1):
    if not binding_available:
        probe(f"A{n:02d}_evidence_binding_{kind}", False, "evidence digest binding not implemented")
        continue
    altered = copy.deepcopy(base)
    row = altered["records"][idx]
    match = row["fields"]["appeals_review"]["matches"][0]
    if kind == "text":
        match["text"] = value
    elif kind == "source_sha":
        row["source_sha256"] = value
    elif kind == "url":
        row["url"] = value
    elif kind == "href":
        match["contact_tokens"]["hrefs"].append(value)
    elif kind == "extra_match":
        second = copy.deepcopy(match)
        second["text"] = value
        row["fields"]["appeals_review"]["matches"].append(second)
        row["fields"]["appeals_review"]["match_count"] = 2
    rejected = False
    try:
        semantic.encode(altered)
    except ValueError:
        rejected = True
    probe(f"A{n:02d}_evidence_binding_{kind}", rejected, "mutated evidence must not inherit frozen witness identity")


# ---------------------------------------------------------------------------
# B. 25 parser/extraction robustness probes
# ---------------------------------------------------------------------------
def audited(body: str) -> dict:
    return audit.audit_page("https://example.test/x", body.encode("utf-8"), fetched_at_utc="2026-09-17T00:00:00+00:00")

html_footer = "<main><h3>3.5 - Appeals and review</h3><p>None.</p></main><footer><a href='https://x.test/privacy'>Privacy</a></footer>"
r = audited(html_footer)["fields"]["appeals_review"]
probe("B01_footer_link_excluded", not r["syntactic_contact_token_present"])

html_header = "<header><a href='mailto:noise@example.test'>noise</a></header><main><h3>3.5 - Appeals and review</h3><p>No route stated.</p></main>"
r = audited(html_header)["fields"]["appeals_review"]
probe("B02_header_link_excluded", not r["syntactic_contact_token_present"])

for k, text in enumerate([
    "Request review at https://example.gov.uk/appeal",
    "Email review@example.gov.uk",
    "Call +44 20 7946 0958",
    "Call 020 7946 0958",
], start=3):
    r = audited(f"<main><h3>3.5 - Appeals and review</h3><p>{text}</p></main>")["fields"]["appeals_review"]
    probe(f"B{k:02d}_plain_contact_token", r["syntactic_contact_token_present"])

r = audited("<main><h3>3.5 - Appeals and review</h3><p><a href='https://example.gov.uk/appeal'>Review</a></p></main>")["fields"]["appeals_review"]
probe("B07_href_token", r["syntactic_contact_token_present"])

r = audited("<main><h3>3.5 - Appeals and review</h3><p><a href='mailto:review@example.gov.uk'>Email</a></p></main>")["fields"]["appeals_review"]
probe("B08_mailto_token", r["syntactic_contact_token_present"])

r = audited("<main><h3>3.5 - Appeals and review</h3><p>No contact details here.</p></main>")["fields"]["appeals_review"]
probe("B09_no_false_contact_token", not r["syntactic_contact_token_present"])

r = audited("<main><h3>4.2.7 - Model performance</h3><p>None.</p><h3>4.2.7 - Model performance</h3><p>Accuracy 95%.</p></main>")["fields"]["model_performance"]
probe("B10_repeated_performance_retained", r["match_count"] == 2)

r = audited("<main><h3>3.5 - Appeals and review</h3><p>A</p><h3>3.5 - Appeals and review</h3><p>B</p></main>")["fields"]["appeals_review"]
probe("B11_repeated_appeals_retained", r["match_count"] == 2)

r = audited("<main><h2>Tier 2 - Risks, Mitigations and Impact Assessments</h2><p>category</p></main>")["fields"]["risks"]
probe("B12_tier_heading_not_risk_field", not r["section_present"])

r = audited("<main><h3>5.2 - Risks and mitigations</h3><p>Risk text.</p></main>")["fields"]["risks"]
probe("B13_risks_and_mitigations_match", r["section_present"])

r = audited("<main><h3>5.1 - Impact assessments</h3><p>DPIA.</p></main>")["fields"]["impact_assessment"]
probe("B14_plural_impact_match", r["section_present"])

r = audited("<main><h3>5.1 - Impact assessment</h3><p>DPIA.</p></main>")["fields"]["impact_assessment"]
probe("B15_singular_impact_match", r["section_present"])

r = audited("<main><h3>3.2 - Human review</h3><p>Officer review.</p></main>")["fields"]["human_review"]
probe("B16_human_review_match", r["section_present"])

r = audited("<main><h3>3.2 - Human decisions and review</h3><p>Officer review.</p></main>")["fields"]["human_review"]
probe("B17_human_decisions_review_match", r["section_present"])

r = audited("<main><h3>3.5 - Appeals and review</h3><p>A</p></main>")["fields"]["appeals_review"]
probe("B18_number_hyphen_heading", r["section_present"])

r = audited("<main><h3>3.5. Appeals and review</h3><p>A</p></main>")["fields"]["appeals_review"]
probe("B19_number_dot_heading", r["section_present"])

r = audited("<html><body><h3>3.5 - Appeals and review</h3><p>A</p></body></html>")["fields"]["appeals_review"]
probe("B20_no_main_fallback", r["section_present"])

r = audited("<h3>3.5 - Appeals and review</h3><p>outside</p><main><h3>3.2 - Human review</h3><p>inside</p></main>")["fields"]["appeals_review"]
probe("B21_main_boundary_preferred", not r["section_present"])

for k, text in enumerate(["N/A no decisions.", "There is no formal appeals process.", "None."], start=22):
    r = audited(f"<main><h3>3.5 - Appeals and review</h3><p>{text}</p></main>")["fields"]["appeals_review"]
    probe(f"B{k:02d}_none_phrase_variant", r["contains_none_or_na_phrase"])

r1 = audited("<main><h3>3.5 - Appeals and review</h3><p>A</p></main>")
r2 = audited("<main><h3>3.5 - Appeals and review</h3><p>B</p></main>")
probe("B25_source_hash_binds_bytes", r1["source_sha256"] != r2["source_sha256"])


# ---------------------------------------------------------------------------
# C. 25 semantic-codebook consistency probes from bounded hostile review
# ---------------------------------------------------------------------------
semantic_expectations = [
    (38, "NO_SEPARATE", True, "FCDO N/A plus broader rights"),
    (134, "NO_SEPARATE", False, "Splink feedback is not no-separate statement"),
    (63, "NO_SEPARATE", True, "NS&I says no formal appeal because no binding decision"),
    (60, "HELP_FEEDBACK", True, "RBA directs parents to school"),
    (60, "PROCESS_REFERENCE", False, "general school contact is not a named process"),
    (95, "PROCESS_REFERENCE", True, "BDUK says challenge mechanism exists"),
    (95, "PUBLIC_INITIATION", False, "BDUK gives no initiation/reach instruction"),
    (110, "PUBLIC_INITIATION", True, "Highways webchat gives linked reporting route"),
    (144, "NO_SEPARATE", True, "hard deletion cannot be appealed/recovered"),
    (119, "NO_SEPARATE", True, "NEET model says models do not make specific decisions"),
    (119, "REFUSAL_OR_OPT_OUT", True, "NEET data-use refusal"),
    (52, "NO_SEPARATE", True, "Xylo says tool makes no decisions"),
    (148, "PLANNED_NOT_OPERATING", True, "DARAT says process not currently designed"),
    (116, "DATA_RIGHTS", True, "Wilton Park data removal"),
    (116, "AMBIGUOUS", True, "data right relevance to output review unresolved"),
    (144, "AMBIGUOUS", True, "explanation/recovery tension"),
    (144, "EXPLANATION_ONLY", True, "justification without restoration"),
    (33, "REFUSAL_OR_OPT_OUT", True, "Magic Notes refusal"),
    (124, "REFUSAL_OR_OPT_OUT", True, "Access Assure refusal"),
]
for n, (idx, label, want, detail) in enumerate(semantic_expectations, start=1):
    present = label in labels(idx)
    probe(f"C{n:02d}_index_{idx}_{label}", present is want, detail)

probe("C20_label_unit_is_proposition", getattr(semantic, "LABEL_UNIT", None) == "proposition_within_field")
probe("C21_public_initiation_requires_instruction", "instruction" in semantic.LABELS.get("PUBLIC_INITIATION", "").lower())
probe("C22_no_separate_is_scoped", "proposition" in semantic.LABELS.get("NO_SEPARATE", "").lower())
probe("C23_explanation_only_is_scoped", "proposition" in semantic.LABELS.get("EXPLANATION_ONLY", "").lower())
probe("C24_planned_process_ceiling", "PLANNED_PROCESS != OPERATING_ROUTE" in semantic.CEILINGS)
probe("C25_actor_scope_ceiling", "ACTOR_SCOPE_MATTERS" in semantic.CEILINGS)


# ---------------------------------------------------------------------------
# D. 25 anti-drift / claim-ceiling probes
# ---------------------------------------------------------------------------
drift_needles = [
    "CURRENT COMPETITION LEAD",
    "NOT SELECTED ENTRY",
    "NOT A POLICY OR COMPLIANCE SCORE",
    "published record",
    "not hidden/internal system reality",
    "GOV.UK / Government Digital Service owns",
    "Tesseract Academy",
    "NOT_FOUND_IN_BOUNDED_SEARCH != NOVEL",
    "does not establish classification validity",
    "No scalar score is produced",
    "not called a review route",
    "sample, not a population estimate",
    "Token absence also does not mean no reader action exists",
    "Only retain that finding at the strength earned",
    "Re-read live competition Guidelines/terms",
    "FIELD_PRESENT != PRACTICAL_NAVIGABILITY",
    "SECTION_PRESENT != PRACTICALLY_EFFECTIVE_REMEDY",
    "SYNTACTIC_CONTACT_TOKEN_PRESENT != RELEVANT_APPEAL_ROUTE",
    "CONCRETE_ROUTE_OBSERVED != ROUTE_EFFECTIVE",
    "HUMAN_HANDOFF != FORMAL_APPEAL",
    "ROUTE_DESCRIBED_WITHOUT_LOCATOR != NO_ROUTE_EXISTS",
    "DISCLOSURE_ABSENT != PRACTICE_ABSENT",
    "PUBLIC_RECORD_AUDIT != COMPLIANCE_AUDIT",
    "PUBLIC_RECORD_AUDIT != POLICY_VERDICT",
    "No registration, organiser contact, model/provider spend, terms acceptance or submission",
]
for n, needle in enumerate(drift_needles, start=1):
    probe(f"D{n:02d}_drift_{n}", needle.lower() in README.lower(), needle)

assert len(RESULTS) == 100, len(RESULTS)
failed = [r for r in RESULTS if not r[1]]
print("FALSIFY_100")
print(f"total={len(RESULTS)} passed={len(RESULTS)-len(failed)} failed={len(failed)}")
for name, ok, detail in RESULTS:
    print(f"{'PASS' if ok else 'FAIL'}\t{name}\t{detail}")
if failed:
    raise SystemExit(1)
