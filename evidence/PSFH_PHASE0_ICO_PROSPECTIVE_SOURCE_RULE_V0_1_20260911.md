# PSFH Phase 0 — ICO prospective source rule v0.1

Status: **DRAFT SOURCE-SELECTION RULE / TARGET MONTH FIXED / SOURCE OBJECT NOT SELECTED / PRE-EXECUTION / NO CASE READING**  
Date: 11 September 2026, Europe/London  
Basis: COM #119; Phase-0 v3.2 + v3.3; current source verdict `REPAIR_MECHANICS`.

This file reduces future operator discretion before any confirmatory ICO account is selected or read. It fixes the prospective report month but does **not** select an actual CSV object, case reference or Decision Notice body.

`RULE_CANDIDATE != SOURCE_FREEZE`

---

## 1. Baseline public state already exposed during development

As of the 11 September 2026 browser-mechanics pass:

- the official ICO owner page for completed FOI/EIR complaints listed monthly CSV objects;
- the newest **listed** completed-case object observed was `FOI complaints July 2026`;
- exact listed URL:
  `https://ico.org.uk/media2/b3ih2uq0/eir-foi-complaint-completed-cases-proactive-disclosure-report-july-2026.csv`;
- July 2026 is a **development-only transport fixture**;
- two independent development GETs returned identical July bytes;
- every row/reference in that development fixture is permanently ineligible for Phase-0 Stage A/B.

No July row/body was selected for Phase-0 evidence by this file.

`DEVELOPMENT_FIXTURE != CONFIRMATORY_UNIVERSE`

---

## 2. Prospective report month — fixed now

The confirmatory source target for this candidate is fixed before confirmatory row inspection:

```text
TARGET_REPORT_MONTH := 2026-08
```

Reason: August 2026 is mechanically the first calendar month after the already-exposed July development fixture. Fixing it now removes retrieval-timing discretion from month selection.

After this rule is frozen and the development transport mechanics are shown to work, inspect only the official owner page's links under **Completed FOI/EIR complaint cases** for an August 2026 monthly completed-case CSV object.

A qualifying object must:

1. belong to the completed-case section, not active/open caseload;
2. resolve from the official ICO owner page;
3. be labelled/identified as a monthly completed FOI/EIR complaints CSV;
4. encode **August 2026** unambiguously in both displayed label and filename; and
5. not already be designated a development fixture.

Rules:

- exactly one qualifying August 2026 object -> candidate source object;
- zero August objects, with no later completed-case month yet visible -> `SOURCE_NOT_YET_AVAILABLE`;
- zero August objects while any later completed-case monthly object is visible -> `SOURCE_UNAVAILABLE` and stop this candidate;
- more than one distinct qualifying August object -> `SOURCE_MONTH_AMBIGUOUS` and stop;
- label/filename month disagreement -> `SOURCE_MONTH_CONFLICT` and stop.

Do **not** roll forward to September or a later month under this candidate.

Owner-page retrieval may be repeated while the August object is genuinely not yet available, but a later-month appearance without August converts the state to `SOURCE_UNAVAILABLE`; it is not permission to change the target month.

`RETRIEVAL_TIMING != MONTH_SELECTOR`  
`NO_AUGUST != TRY_SEPTEMBER`

---

## 3. Byte acquisition and repeatability gate

For the unique qualifying August object, perform two independent unauthenticated public GETs in one bounded source-preparation run.

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

Transport retries caused by a failed request may repeat the same August URL, but they may not substitute another month. Preserve failures.

`TWO_GETS_DIFFER -> SOURCE_MUTABLE`

---

## 4. Header-only inspection before row-level manifest

Only after byte equality is established, run the networkless PR #200 `inspect` operation on one preserved byte-identical copy.

The permitted successful pre-contract output is limited to:

- exact byte length / SHA-256;
- BOM state;
- exact ordered header row;
- logical CSV record count.

Do not print/search row values during this step.

Parser errors are not a secrecy boundary; if a malformed source causes diagnostic text to expose a fragment, preserve the error and stop rather than continuing to inspect the malformed file.

The July development fixture currently provides this development schema:

```json
["Case_Reference2","CaseStatus1","Legislation","Received_Datetime1","Completed_DateTime1","Sector","SubSector","Decision_Primary_Reason1","Submitted_About_Account","Submitted_About_Account_Region","Decision","DecisionDetail1","DecisionDetail2","PriorityCase1"]
```

This is development evidence, not a guarantee that August will retain the schema. A future schema difference must be handled by an already-frozen compatibility rule; do not remap confirmatory columns after seeing which interpretation yields useful cases.

---

## 5. Closed completion-date window — fixed now

Because the target report month is fixed, the candidate completion window is also fixed now:

```text
window_start := 2026-08-01
window_end   := 2026-08-31
```

The window is not derived from confirmatory row distributions.

If later validation finds zero mechanically eligible DN-served rows inside that window, or source metadata makes the August-report interpretation incoherent, return `SOURCE_WINDOW_NULL` rather than shifting/expanding the dates.

Do not merge adjacent months after seeing counts.

`ROW_DISTRIBUTION != WINDOW_SELECTOR`

---

## 6. Required exact source-contract facts

Before row-level manifest generation, write one exact PR #200 source contract containing:

- selected August source URL;
- retrieval UTC;
- exact byte length;
- exact SHA-256;
- exact ordered headers;
- exact reference header;
- exact completed-date header;
- exact source date format;
- exact `Decision Detail 1` header;
- exact DN-served cell value;
- fixed August window `2026-08-01` through `2026-08-31`;
- complete frozen development-exposure exclusions available at that point.

Current development header-role candidates are:

```text
REFERENCE_HEADER_EXACT_CANDIDATE := Case_Reference2
COMPLETED_DATE_HEADER_EXACT_CANDIDATE := Completed_DateTime1
DECISION_DETAIL_1_HEADER_EXACT_CANDIDATE := DecisionDetail1
```

They are candidates derived from July development bytes. Before this rule becomes executable, decide once whether August must match these exact role/header names or whether an explicitly source-versioned compatibility rule is required. Do not silently reinterpret a changed August schema.

Two items remain deliberately **UNSET in this v0.1 candidate** pending the bounded July metadata probe:

```text
DN_SERVED_VALUE_EXACT := UNSET
SOURCE_DATE_FORMAT_EXACT := UNSET
```

They must be fixed from owner documentation and/or development-only fixture mechanics before this source rule can become executable. They may not be learned by looking for values that produce attractive confirmatory counts.

A development-only metadata probe may inspect only the named completion-date column and `DecisionDetail1` column needed to freeze their syntax/value conventions. It must not emit or join those values to case references, organisations, issues or outcomes. Any file used for that probe is permanently excluded from Stage A/B.

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

- completed date falls inside the fixed August window;
- `DecisionDetail1` equals the exact frozen DN-served value;
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

- **source object availability** — August is fixed; availability may still fail, but failure cannot switch the month;
- **transport implementation** — HTTP client/browser may differ, but exact response bytes must converge;
- **August schema compatibility** — July supplies a development schema; exact future compatibility rule remains to freeze;
- **exact DN-served value/date format** — still unset, must be earned on development-only metadata;
- **carrier burden bound** — still unset and blocks ranking;
- **participant/provider/spend** — entirely outside this file.

None of these may be resolved by reading confirmatory Decision Notice substance first.

A future revision that changes the target month, changes the date window after seeing completed-date distributions, changes the DN value after seeing which string yields more cases, silently remaps a changed August schema, or changes the burden cap after seeing selected bodies is outcome-responsive source tuning and invalidates the freeze.

---

## 13. Current disposition

This rule is **not ready to freeze**.

Before promotion, close at least:

- current-head PR #200 full self-test/review;
- exact DN-served value;
- exact source completion-date format;
- development-fixture exclusion-keyset mechanics;
- August schema compatibility rule;
- justified carrier burden bound.

The July development transport itself is now demonstrated repeatable within one bounded two-GET run; that is no longer the main blocker.

If remaining items cannot be closed without inspecting confirmatory case substance or adding discretionary rescue paths, return `SOURCE_REJECT` or `DESIGN NULL` as appropriate.

No August source object, row, reference, Decision Notice body, participant, provider, inference or spend is selected/activated by this draft.

```text
PROSPECTIVE_RULE != SOURCE_SELECTION
AUGUST_TARGET != AUGUST_SOURCE_AVAILABLE
NO_AUGUST != TRY_SEPTEMBER
TWO_EQUAL_GETS != SOURCE_TRUTH
SOURCE_MANIFEST != CASE_SELECTION
DETERMINISTIC_RANK != PRACTICAL_VALIDITY
```
