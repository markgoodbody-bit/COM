# PSFH Phase 0 — ICO prospective source rule v0.1

Status: **DRAFT SOURCE-SELECTION RULE / NOT FROZEN / PRE-EXECUTION / NO SOURCE SELECTED / NO CASE READING**  
Date: 11 September 2026, Europe/London  
Basis: COM #119; Phase-0 v3.2 + v3.3; current source verdict `REPAIR_MECHANICS`.

This file reduces future operator discretion before any confirmatory ICO account is selected or read. It does **not** itself choose a monthly dataset, calendar window, case reference or Decision Notice body.

`RULE_CANDIDATE != SOURCE_FREEZE`

---

## 1. Baseline public state already exposed during development

As of the 11 September 2026 browser-mechanics pass:

- the official ICO owner page for completed FOI/EIR complaints listed monthly CSV objects;
- the newest **listed** completed-case object observed was `FOI complaints July 2026`;
- exact listed URL:
  `https://ico.org.uk/media2/b3ih2uq0/eir-foi-complaint-completed-cases-proactive-disclosure-report-july-2026.csv`;
- July 2026 is a **development-only transport fixture** if used for byte/header/repeatability testing;
- every row/reference in a development transport fixture is permanently ineligible for Phase-0 Stage A/B.

No July row/body was selected for Phase-0 evidence by this file.

`DEVELOPMENT_FIXTURE != CONFIRMATORY_UNIVERSE`

---

## 2. Prospective monthly-object selection

After this rule is frozen and the development transport mechanics are shown to work, identify the official owner page's set of links under **Completed FOI/EIR complaint cases**.

Candidate monthly objects are links that:

1. belong to the completed-case section, not active/open caseload;
2. resolve from the official ICO owner page;
3. are labelled/identified as a monthly completed FOI/EIR complaints CSV;
4. encode one unambiguous calendar report month in the displayed label **and** filename;
5. have a report month later than July 2026; and
6. are not already designated development fixtures.

Select the **chronologically earliest report month later than July 2026** among the candidate monthly objects visible at the first authorised source-preparation retrieval.

If several later monthly links appear together, choose the earliest report month. Do not choose the newest, shortest, largest, most convenient or most promising month.

If no qualifying later monthly object exists, return `SOURCE_NOT_YET_AVAILABLE`; do not fall back to July or an earlier development file.

If the report month cannot be parsed mechanically from the owner-page label and filename, return `SOURCE_RULE_UNRESOLVED`; do not inspect rows to infer which month the file probably represents.

If label and filename encode different months, return `SOURCE_MONTH_CONFLICT`.

If more than one distinct completed-case CSV object claims the same earliest qualifying report month, return `SOURCE_MONTH_AMBIGUOUS`; do not choose by file size, URL order, timestamp or content.

The first authorised owner-page retrieval may be repeated only to resolve a transport failure of that same page. A repeat may not be used to wait for a different month once a qualifying selected month/object has been observed.

`FIRST_FUTURE_MONTH_BY_RULE != OPERATOR_CHOICE`

---

## 3. Byte acquisition and repeatability gate

For the selected monthly object, perform two independent unauthenticated public GETs in one bounded source-preparation run.

For each retrieval preserve:

- initial owner-page href;
- final resolved URL;
- retrieval UTC;
- HTTP status;
- `Content-Type`;
- `Content-Disposition`, if present;
- exact byte length;
- SHA-256 of response bytes.

Do not inspect row 2+ before the repeatability comparison.

The two retrievals must agree on:

- final resolved URL;
- byte length;
- SHA-256.

If they differ, return `SOURCE_MUTABLE` and stop. Do not choose one version or retry until a preferred version appears.

Transport retries caused by a failed request may repeat the same selected URL, but they may not substitute another month. Preserve failures.

`TWO_GETS_DIFFER -> SOURCE_MUTABLE`

---

## 4. Header-only inspection before window freeze

Only after byte equality is established, run the networkless PR #200 `inspect` operation on one preserved byte-identical copy.

The permitted successful pre-contract output is limited to:

- exact byte length / SHA-256;
- BOM state;
- exact ordered header row;
- logical CSV record count.

Do not print/search row values during this step.

Parser errors are not a secrecy boundary; if a malformed source causes diagnostic text to expose a fragment, preserve the error and stop rather than continuing to inspect the malformed file.

---

## 5. Closed completion-date window

The selected monthly object's **report month** determines the candidate closed completion window:

```text
window_start = first calendar day of report month
window_end   = final calendar day of report month
```

The window is therefore fixed by the prospectively selected monthly object, not by inspecting the distribution of completed dates.

If later validation finds zero mechanically eligible DN-served rows inside that window, or source metadata makes the report-month interpretation incoherent, return `SOURCE_WINDOW_NULL` rather than shifting/expanding the dates.

Do not merge adjacent months after seeing counts.

`ROW_DISTRIBUTION != WINDOW_SELECTOR`

---

## 6. Required exact source-contract facts

Before row-level manifest generation, write one exact PR #200 source contract containing:

- selected source URL;
- retrieval UTC;
- exact byte length;
- exact SHA-256;
- exact ordered headers;
- exact reference header;
- exact completed-date header;
- exact source date format;
- exact `Decision Detail 1` header;
- exact DN-served cell value;
- mechanically derived report-month window;
- complete frozen development-exposure exclusions available at that point.

Two items remain deliberately **UNSET in this v0.1 candidate** pending development-fixture evidence:

```text
DN_SERVED_VALUE_EXACT := UNSET
SOURCE_DATE_FORMAT_EXACT := UNSET
```

They must be fixed from owner documentation and/or development-only fixture mechanics before this source rule can become executable. They may not be learned by looking for values that produce attractive confirmatory counts.

A development-only metadata probe may inspect only the named completion-date column and `Decision Detail 1` column needed to freeze their syntax/value conventions. It must not emit or join those values to case references, organisations, issues or outcomes. Any file used for that probe is permanently excluded from Stage A/B.

`UNSET != WILDCARD`

---

## 7. Development-fixture exclusion keyset

Every reference contained in any source file used as a development transport/parser/metadata fixture is ineligible for Stage A/B, even if no substantive body was read.

Before confirmatory manifest generation, construct a development exclusion keyset mechanically from the **reference column only** of every development fixture whose bytes were used.

Permitted operation:

```text
fixture exact bytes
-> frozen reference-header identity
-> reference-column extraction only
-> trim outer whitespace only
-> reject blank reference
-> exact case-sensitive reference set
-> sort unique references by UTF-8 byte order
-> serialize each exact reference as UTF-8 + LF
-> SHA256(serialized exclusion keyset)
-> preserve set count + SHA256 + contributing fixture byte hashes
```

No case-folding, punctuation normalization, suffix stripping or fuzzy reference matching is allowed.

Do not inspect accompanying issue/outcome/organisation/body fields for this exclusion operation.

The confirmatory contract must include the union of:

1. the existing named project exposure ledger; and
2. the mechanically extracted development-fixture reference set.

The inline contract list remains the operative exclusion list for PR #200 v0.1. The exclusion-keyset count/hash are replay/provenance controls, not substitutes for the actual list.

If the development reference header cannot be identified without semantic row inspection, stop with `EXCLUSION_KEYSET_UNRESOLVED`.

If two contributing fixtures contain the same reference, union it once and preserve the duplicate-across-fixtures count separately; do not treat the duplicate as evidence that either source is invalid by itself.

`FIXTURE_USED -> FIXTURE_REFERENCES_EXCLUDED`

---

## 8. DN-row eligibility and internal join

After the exact contract is frozen, PR #200 may emit the source manifest.

A manifest row is mechanically eligible for the next join only if:

- completed date falls inside the frozen report-month window;
- `Decision Detail 1` equals the exact frozen DN-served value;
- reference is not in the frozen development/project exclusion set;
- validator source-integrity checks pass.

For each eligible reference, use the ICO **Decision Notices** collection's internal exact-reference search.

Observed development evidence on 11 September 2026 showed `1 of 1` for four already-excluded references. That demonstrates the mechanism, not total coverage.

Frozen future rule:

```text
0 Decision Notice results  -> SOURCE_UNAVAILABLE_FOR_REFERENCE
1 result whose route encodes the exact searched reference -> JOIN_OK
>1 results -> SOURCE_AMBIGUOUS_FOR_REFERENCE
```

Matching is exact after the same outer-whitespace trim used for the source reference. No case folding, approximate string match or external-search rescue.

The joined Decision Notice body is still not opened at this stage.

---

## 9. Mechanical carrier availability / length parameter

A selected joined Decision Notice must later be convertible into the frozen text-only carrier described in the ICO reuse note.

The maximum participant-carrier burden is intentionally **UNSET** here:

```text
MAX_CARRIER_WORDS := UNSET
```

Do not invent a length threshold merely to finish this file. It must be fixed before confirmatory ranking using participant/task burden evidence or a separately justified dry-timing rule.

If no defensible burden bound is frozen, this source rule remains non-executable.

`BURDEN_BOUND_UNSET -> NO_RANKING`

---

## 10. Deterministic ranking seed — frozen candidate

If all prior mechanics are frozen and satisfied, eligible/joined/available references may be ordered without reading their substantive bodies by:

```text
seed_material := "PSFH_PHASE0_STAGE_A_ICO_V1|e5ce9e955dfbf187992604e47109e218e7341bc1"
seed_sha256   := 861eec5f632dbc3f2541256343dad89f0270ffdf6d44da3878b9c1bc2c063d04
rank_input    := lowercase ASCII seed_sha256 + "|" + exact trimmed reference
rank_key(ref) := SHA256(UTF8(rank_input))
order         := ascending lowercase hexadecimal rank_key
```

The seed is derived from an already-public Phase-0 source identity, not chosen after the universe is visible.

If two distinct references somehow produce the same rank key, order those references by exact UTF-8 byte order as a deterministic tie-break and record the collision. Do not regenerate a seed.

This v0.1 file does **not** yet authorise ranking because the exact DN value, source date format and carrier burden bound remain unset.

`SEED_FROZEN != RANKING_AUTHORISED`

---

## 11. Stage-A selection once and only if rule becomes executable

Only after every required parameter above is frozen:

1. build exact source manifest;
2. apply internal DN join;
3. apply frozen carrier-availability/burden rule;
4. compute deterministic rank keys without opening substantive bodies;
5. choose the first three eligible ranked references as `A1`, `A2`, `A3` in rank order;
6. freeze those three exact reference identities and their source/join provenance;
7. only then may the separately authorised Stage-A process open A1 substantive content.

No replacement for substantive unsuitability is permitted.

If A1/A2/A3 later prove awkward, uninteresting, negative controls, or hostile to the construct, that is part of the test.

Only pre-frozen source-unavailability/malformed/join/carrier-failure rules may advance to the next ranked reference.

If fewer than three references survive the entire pre-frozen mechanical pipeline, return `SOURCE_UNIVERSE_INSUFFICIENT`; do not widen the month, relax exclusions or raise the burden cap.

`AWKWARD_CASE != REPLACEMENT_REASON`

---

## 12. Self-attack / remaining discretion map

This v0.1 deliberately exposes rather than hides the remaining operator freedoms:

- **when the first authorised owner-page retrieval occurs** — execution scheduling remains external, but month choice does not: earliest qualifying month after July wins;
- **transport implementation** — HTTP client/browser may differ, but exact response bytes must converge;
- **exact DN-served value/date format** — still unset, must be earned on development-only metadata;
- **carrier burden bound** — still unset and blocks ranking;
- **participant/provider/spend** — entirely outside this file.

None of these may be resolved by reading confirmatory Decision Notice substance first.

A future revision that changes the source month after seeing row counts, changes the date window after seeing the completed-date distribution, changes the DN value after seeing which string yields more cases, or changes the burden cap after seeing selected bodies is outcome-responsive source tuning and invalidates the freeze.

---

## 13. Current disposition

This rule is **not ready to freeze**.

Before promotion, close at least:

- development monthly CSV byte/repeatability transport;
- current-head PR #200 review/test;
- exact DN-served value;
- exact source completion-date format;
- development-fixture exclusion-keyset mechanics;
- justified carrier burden bound.

If those cannot be closed without inspecting confirmatory case substance or adding discretionary rescue paths, return `SOURCE_REJECT` or `DESIGN NULL` as appropriate.

No source file, month, row, reference, Decision Notice body, participant, provider, inference or spend is selected/activated by this draft.

```text
PROSPECTIVE_RULE != SOURCE_SELECTION
FIRST_FUTURE_MONTH != BEST_LOOKING_MONTH
TWO_EQUAL_GETS != SOURCE_TRUTH
SOURCE_MANIFEST != CASE_SELECTION
DETERMINISTIC_RANK != PRACTICAL_VALIDITY
```
