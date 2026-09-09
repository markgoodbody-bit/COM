# PSFH Phase 0 — irreversibility construct candidate v2

Status: DESIGN INPUT / NOT FROZEN / NO STUDY EXECUTION / NO USEFULNESS CLAIM  
Prepared: 9 September 2026  
Supersedes for current design discussion: `PSFH_PHASE0_IRREVERSIBILITY_CONSTRUCT_CANDIDATE_20260909.md` only where this note is more specific.  
Inputs: Framework candidate `ff54721d...`; Codex pre-freeze critique `35f4ab0...` / `PSFH_PHASE0_PREFREEZE_CRITIQUE_20260909.md`.

## Question

Before asking whether PSFH improves reasoning, establish whether this proposed outcome is stable enough to score:

> **Irreversibility point:** a source-supported state, option or condition that becomes materially harder or impossible to restore after a named threshold/event or after time passes beyond a source-supported window.

A point must be supportable from the frozen account itself. Outside facts may be needed to understand a domain, but they cannot silently supply the point being scored.

`SCORABLE != USEFUL`  
`REFERENCE_SET != WORLD`

## Why v1 is not ready to freeze

The first candidate left five material holes:

1. empty-empty F1 was undefined;
2. a convenient empty-set convention could dominate pooled medians;
3. source-sufficiency was measured after excluding the very points that would reveal insufficiency;
4. matcher agreement had no defined candidate-pair universe;
5. pairwise matches did not define a consistent three-builder family.

Do not patch these with arbitrary constants and proceed.

## Smaller architecture

Use **two separated stages**.

### Stage A — calibration / rule debugging

Purpose: learn whether the extraction and matching instructions are operable, and fix mechanical ambiguities before a confirmatory construct check.

- Mechanically select a small disposable development set of heterogeneous public written accounts using a rule fixed before substantive reading.
- These development accounts are permanently excluded from the later confirmatory Phase 0 and any efficacy comparison.
- Three independent builders receive the same frozen account and the same plain-language definition. They may return `ZERO` or at most six source-anchored points.
- Each nonzero point must contain:
  1. the state/option/condition;
  2. the threshold/event/window after which restoration becomes materially harder or impossible;
  3. a source anchor;
  4. `SOURCE_SUFFICIENT` or `NEEDS_OUTSIDE_FACT`, with a short reason.
- Two matchers independently construct a **one-to-one matching** between each pair of builders' point sets. They do not label every Cartesian pair. They may return `UNCERTAIN` rather than force a match.
- Matching instructions are debugged only on Stage A. Any rule change is recorded.

Stage A is not evidence that the construct survived. It exists so the confirmatory rules are not invented after seeing the holdout.

### Freeze boundary

After Stage A and before selecting/reading any holdout account, freeze:

- source-selection rule for holdout accounts;
- builder instructions and point cap;
- matching instructions;
- treatment of `NEEDS_OUTSIDE_FACT`;
- family-formation rule below;
- exact descriptive statistics;
- explicit survival / NULL rule.

If the team cannot write those rules without hand-waving after Stage A, stop. Do not create a confirmatory Phase 0.

### Stage B — confirmatory Phase 0 holdout

Use fresh accounts selected mechanically after the protocol is frozen. No account used in Stage A, TRACE/ME development, or prior project examples may enter the holdout.

Three fresh independent builders extract points. Two blind matchers apply the frozen matching rule.

## Zero accounts are a separate outcome

Do **not** put zero-zero cases into F1 or another extraction-agreement average.

For each account report one of:

- `ALL_ZERO` — all three builders return zero;
- `MIXED_ZERO` — at least one zero and at least one nonzero;
- `ALL_NONZERO` — all three return at least one point.

`ALL_ZERO` can show agreement that the frozen account does not support an irreversibility point under the definition. It supplies **no recall denominator** and must not inflate nonempty extraction reliability.

`MIXED_ZERO` is direct evidence of construct instability for that account and must stay visible.

## Source sufficiency stays visible before filtering

Every proposed point is retained in the audit record even if marked `NEEDS_OUTSIDE_FACT`.

Report, before any exclusion:

- total points proposed;
- number/percentage marked `NEEDS_OUTSIDE_FACT` by builders;
- number whose source-sufficiency label is disputed during blind review.

Only source-supported points may enter a later reference set, but the excluded points remain part of the Phase-0 result. This prevents the source-sufficiency denominator disappearing during filtering.

## Matching and three-builder families

Avoid an all-pairs YES/NO matrix whose easy negatives dominate agreement.

For each builder pair (A-B, A-C, B-C), each matcher independently creates a one-to-one set of proposed matches plus any `UNCERTAIN` items.

A pair edge is **accepted** only when both matchers independently choose the same one-to-one match. Disagreement or uncertainty leaves the edge unaccepted; no adjudicator silently repairs it during Phase 0.

A **three-builder family** exists only when all three accepted pair edges exist:

- A1 ↔ B1
- A1 ↔ C1
- B1 ↔ C1

Do not infer the third edge by transitive closure. Broad/narrow inconsistent triangles therefore remain disagreement rather than manufactured consensus.

## Descriptive outputs for nonempty accounts

For every `ALL_NONZERO` account report, without pooling zero accounts into it:

- points proposed by each builder;
- accepted A-B / A-C / B-C matches;
- number of complete three-builder families;
- per-builder **family coverage** = that builder's points participating in a complete three-builder family / that builder's source-supported points;
- unmatched source-supported points;
- disputed/uncertain matches;
- pre-exclusion outside-fact rate.

For `MIXED_ZERO` accounts report the same information where defined, but mark the account unstable rather than rescuing it through averages.

Do not use one pooled median across accounts as the primary gate.

## Survival rule — to be frozen after calibration, not invented from convention

This v2 deliberately does **not** invent replacement numeric thresholds before Stage A. The thresholds in the first candidate were not justified, and moving them around would only create prettier arbitrary numbers.

Stage A may be used to determine whether a simple, auditable survival rule can be written. The rule must then be frozen before holdout selection. At minimum it must separately constrain:

1. prevalence of `MIXED_ZERO` holdout accounts;
2. amount of source-supported nonempty material available for a later recall denominator;
3. family coverage on `ALL_NONZERO` accounts;
4. matcher uncertainty/disagreement;
5. outside-fact dependence before exclusion.

If Stage A cannot support a defensible rule simple enough to explain in a paragraph, the construct returns **DESIGN NULL** and #119 should choose another outcome rather than add more adjudication machinery.

## Novel points in a later efficacy study

If Phase 0 eventually survives, the consensus families may provide a conservative recall denominator. They are not a complete ontology of the account.

Therefore:

`NOT_IN_REFERENCE_SET != FALSE_POSITIVE`

A candidate output that names a point outside the consensus families must not automatically be punished. Any later precision/inflation analysis needs a separately frozen, blind source-support adjudication rule. That later rule is **not part of Phase 0** and must not be smuggled in as a second hidden gold standard here.

## Independence / contamination

- Mark is not an adjudicator or hidden gold standard.
- Project AIs that helped write this protocol are contaminated for builder roles.
- Development accounts and project-authored examples are excluded from confirmatory holdout.
- Builder/matcher identities and prior exposure are recorded.
- No private chain-of-thought is required; only submitted points/matches and source anchors are retained.

## Current disposition

**INCOMPLETE DESIGN, IMPROVED.**

Next legitimate work is hostile review of this v2 and deciding whether Stage A is worth running later. No public accounts are selected by this note. No builders, matchers, participants, paid models, recruitment, inference or public claim are authorised.

`CALIBRATION_SET != HOLDOUT`  
`AGREEMENT != TRUTH`  
`DESIGN_NULL != PROJECT_FAILURE`
