# PSFH #119 — Phase 0 irreversibility-construct candidate

Status: DESIGN CANDIDATE / PRE-REGISTRATION INPUT ONLY / NO STUDY EXECUTION / NOT A PUBLIC CLAIM
Prepared: 9 September 2026
Purpose: test whether `irreversibility point` is scoreable enough to support any later usefulness comparison.

## Why Phase 0 exists

Before asking whether PSFH helps a reader notice irreversibility points, establish whether independent readers can identify sufficiently overlapping points in the same written account without PSFH vocabulary, project coaching or Mark acting as hidden gold standard.

If the reference construct is unstable, later recall scores are not meaningful.

`OUTCOME_MEASURE_UNSTABLE -> STUDY_STOPS`
`AGREEMENT != TRUTH`

Agreement here establishes only that the construct can be scored reproducibly enough for a bounded comparison. It does not establish moral truth, domain correctness or usefulness.

## Neutral working definition

For Phase 0 only, an **irreversibility point** is a source-supported event, threshold or time relation after which restoring the materially relevant earlier state, option or opportunity becomes impossible, substantially harder, or requires a qualitatively different repair.

A proposed point must identify:
1. what state/option/opportunity is at stake;
2. the event, threshold or clock relation after which restoration changes materially;
3. the source evidence supporting that relation.

Exclude:
- generic risks with no event/time/order relation;
- invented consequences not supported by the account;
- moral verdicts standing in for a structural point;
- merely costly actions where the source gives no basis that later restoration is materially different.

Builders may return **zero** points. `NONE FOUND` is not a failed annotation.

## Case selection — prevent showcase selection

Do not choose accounts after reading them for suitability.

Candidate mechanical procedure to attack before freeze:
- predeclare 3 public source families with sufficiently self-contained chronology, e.g. an ombudsman/final decision account, an incident investigation/report, and a regulatory/final decision notice;
- from each family, construct an eligible metadata-only list using date/publication/status/length/access rules, without reading substantive content;
- select one account per family by deterministic seeded ordering/hash recorded before content inspection;
- freeze exact source bytes/URLs and cutoff date;
- project-authored cases, AISI material already used in PSFH development, and prior TRACE/ME fixtures are ineligible for the independent set.

An account selected mechanically may contain few or no usable irreversibility points. Do not replace it after reading merely to rescue the construct.

## Independent reference builders

Use 3 builders who:
- do not see the PSFH condition, hypothesis wording, TRACE/ME vocabulary or one another's outputs;
- receive only the frozen account plus the neutral working definition/template;
- may state that the account lacks enough evidence or requires external domain facts;
- produce at most 8 candidate points per account to prevent exhaustive risk-list inflation.

Each point record:

```text
point_id: builder-local opaque id
state_or_option_at_stake:
threshold_or_event:
what_becomes_materially_harder_to_restore:
source_anchor: section/page/line or short source span
confidence: low | medium | high
needs_external_domain_fact: yes | no
```

If `needs_external_domain_fact=yes`, the point is excluded from the Phase-0 consensus core unless the frozen account itself supplies that fact elsewhere.

## Blind matching — do not force agreement

Two matchers receive anonymised/shuffled point records without builder identity.

Two points match only when they concern the same materially affected state/option **and** substantially the same threshold/event relation. Similar wording or sharing a broad topic is insufficient.

Matching rules:
- one-to-one only; no many-to-one merge that inflates apparent agreement;
- matchers independently mark MATCH / NOT MATCH / UNCERTAIN;
- only MATCH/MATCH counts automatically;
- matcher disagreement remains visible rather than being silently harmonised;
- a third adjudicator may resolve matcher disagreement only under a predeclared rule, blind to builder identity and later experimental condition.

## Metrics — reference set mainly measures recall

For every pair of builders, calculate set precision/recall/F1 from one-to-one matched points, then report the symmetric pairwise F1 distribution. Do not choose whichever builder makes the comparison look best.

Also construct a **consensus core**: a point family independently surfaced by at least 2 of 3 builders after blind matching.

Important correction:

`NOT_IN_REFERENCE_SET != FALSE_POSITIVE`

A later experimental reader may surface a valid source-supported irreversibility point all three reference builders missed. Therefore:
- reference consensus is primarily the denominator for **recall**;
- later output **precision/inflation** is adjudicated directly against frozen source evidence by blind raters, not merely by membership in the consensus set;
- novel source-supported points may be accepted as valid without retroactively pretending the original reference set was complete.

This prevents reference-builder omission from being scored as participant error.

## Candidate predeclared stop/pass rule — attack before freeze

Numeric thresholds are provisional design inputs, not results.

A deliberately demanding candidate:

**Construct survives Phase 0 only if:**
- at least 2 of the 3 mechanically selected accounts yield either (a) at least 2 consensus-core points or (b) unanimous zero-point returns;
- pooled median pairwise builder F1 is >= 0.60;
- no non-zero account has median pairwise builder F1 < 0.40;
- blind matchers agree on >= 80% of proposed pair decisions before adjudication;
- fewer than 20% of consensus-core candidates depend on external facts absent from the frozen account.

Otherwise STOP with one of the explicit NULLs:
- `REFERENCE_EXTRACTION_UNSTABLE`;
- `MATCHING_TOO_AMBIGUOUS`;
- `ACCOUNT_NOT_SELF_CONTAINED_ENOUGH`;
- `CONSTRUCT_TOO_SPARSE_FOR_RECALL_SCORING`.

Do not weaken thresholds or substitute accounts after outputs are seen.

CC/Codex should attack whether the exact 0.60/0.40/80%/20% floors are defensible before pre-registration. If no defensible numeric floor can be stated without pretending conventional F1 cutoffs have universal meaning, replace them with a simpler predeclared practical rule **before** outputs exist. Do not import a reliability label by authority.

## Phase 1 boundary if Phase 0 survives

Only then compare:
- matched generic structured-risk prompt;
- fixed PSFH/correction-window route;
- relevant established/domain method where applicable.

Primary outcome: recall of consensus-core irreversibility points.
Secondary: direct blind source-validity judgement of named points / inflation.
Separate: `AVAILABLE -> USED -> HELPFUL` uptake evidence.

No participant recruitment, paid inference, public study or homepage claim follows from Phase 0 design work.

## Main falsifiers preserved

- builders agree only because the extraction prompt smuggles PSFH wording into the task;
- source selection quietly prefers cases where correction-window structure is obvious;
- matcher flexibility creates agreement post hoc;
- a sparse/incomplete consensus set falsely turns novel valid points into false positives;
- domain knowledge unavailable in the text determines the supposed point;
- project AIs agree with one another and that is mislabelled independent validation.

`REFERENCE_SET != WORLD`
`SCORABLE != USEFUL`
`PHASE0_PASS != PRACTICAL_ADVANTAGE`
