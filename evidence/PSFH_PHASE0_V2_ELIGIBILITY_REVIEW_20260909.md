# Phase 0 v2: source eligibility before scoring

Status: DESIGN REVIEW / SYNTHETIC ARITHMETIC / NOT STUDY EXECUTION

Codex, 9 September 2026. Exact design basis:
`8372ca1fe703a193255b84487410f289498669c0`,
`PSFH_PHASE0_IRREVERSIBILITY_CONSTRUCT_V2_20260909.md`.

## What v2 fixes

V2 separates calibration from holdout, keeps raw zero returns outside extraction
averages, retains outside-fact proposals before exclusion, requires independent
one-to-one edges and all three edges for a family, and refuses unjustified
replacement thresholds. These address the five earlier critique categories.
They do not establish a validated outcome measure. V2 explicitly calls itself
incomplete and defers eligibility treatment and survival rules until freeze.

The issues below are specifications still needed at that boundary, not evidence
that a study has failed or that calibration should be forbidden.

## 1. Nonempty proposals can become empty eligible sets

The current zero labels describe what builders return. Family coverage divides
by their source-supported points. Those counts can differ after exclusion.

These are invented count examples, not accounts, annotations or reference data.
Eligibility and the number of eligible families are stipulated only to inspect
the arithmetic; no source-support decision is being simulated or validated.

| Example | Raw A/B/C counts | Eligible A/B/C counts | Eligible families | Per-builder coverage |
| --- | --- | --- | --- | --- |
| All proposals excluded | 1 / 1 / 1 | 0 / 0 / 0 | 0 | undefined / undefined / undefined |
| One builder loses its only proposal | 1 / 1 / 1 | 1 / 1 / 0 | 0 | 0 / 0 / undefined |
| One eligible triangle | 2 / 1 / 1 | 1 / 1 / 1 | 1 | 1 / 1 / 1 |

All three examples are raw `ALL_NONZERO`. The first two still cannot supply
three defined coverage fractions. Excluding raw zero accounts therefore does
not by itself remove every zero denominator.

Proposed clarification, not an adopted scoring rule: preserve raw counts and
raw zero classifications, report eligible counts separately, and use an explicit
not-defined value when an eligible denominator is zero. Do not silently replace
the raw class, convert missing coverage to a perfect score, or drop the account.
The eventual survival rule must say what such cases mean.

Coverage's numerator should also explicitly count only eligible points in
eligible families. Matching raw proposals first may be useful diagnostically,
but a raw triangle is not automatically a source-supported reference family.
Otherwise numerator and denominator can refer to different sets.

## 2. Who establishes eligibility is still unspecified

Builders label points `SOURCE_SUFFICIENT` or `NEEDS_OUTSIDE_FACT`. V2 also asks
for the number disputed during blind review, but its explicit matcher output is
matches plus uncertainty. It does not yet assign source-sufficiency review to a
named role, define its output, or say which rule makes a point eligible when
the builder and reviewer disagree.

This is not a request for another adjudicator. Before freeze, specify whether
existing matchers also assess source support, what source material they see,
and how disagreements affect eligibility. Keep the builder's claim and any
reviewer's assessment distinct. Agreement about two propositions being the
same is not evidence that either proposition is supported by the account.

## 3. Sparse matching needs an uncertainty convention

One-to-one match sets avoid the easy-negative Cartesian matrix problem. The
record still needs to distinguish an explicit no-match assessment from a pair
not chosen or not assessed, and say what an `UNCERTAIN` item identifies: a
point, a proposed pair, or competing pairings. Otherwise the same uncertainty
can produce different counts without a substantive difference in judgement.

This can remain a short output convention. Do not reintroduce an all-pairs
agreement percentage or build a larger matching platform merely to settle it.

## Wording and disposition

Raw `MIXED_ZERO` establishes disagreement in submitted extractions. It does not
by itself distinguish ambiguity in the construct from a reader error, source
insufficiency or instruction failure. Calling the account unstable for the
planned measurement is defensible; diagnosing the cause is a separate claim.

Disposition: retain v2 as improved, incomplete design input. Clarify eligibility,
post-exclusion zero handling and uncertainty records before confirmatory freeze.
Stage A may investigate whether these conventions are workable; no numerical
cutoff is proposed here. If a simple rule cannot be earned, DESIGN NULL remains
available. No accounts selected, new protocol adopted, inference, recruitment,
spend, PSFH publication or TRACE/ME mutation occurred in this review.
