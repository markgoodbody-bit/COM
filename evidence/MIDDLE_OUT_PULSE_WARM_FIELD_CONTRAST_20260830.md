# MIDDLE-OUT PULSE — WARM FIELD CONTRAST — 2026-08-30

Status: WARM DESIGNER-SIDE FEASIBILITY ONLY — NOT VALIDATION / NOT COLD RECEIVER EVIDENCE / NOT TRACE OR ME SOURCE
Aperture: Framework
Candidate surface: `prototypes/MIDDLE_OUT_PULSE_CORE_v0_3.md`

## Purpose

Use two unrelated live 1F916 pull requests as a cheap qualitative check on an important property of the pulse:

> Does it activate selectively, including the ability to stop without manufacturing a new finding?

This is contaminated by Framework's project knowledge and code-review competence. It cannot establish causal benefit of the pulse.

## Specimen A — PR #166 `claims-need-events`

Inspected head: `c81aa64ed7f7efca10a1fa20c7799adcb141c53a`.

Surface purpose: replace maintainer-transcribed docket claims with chained claim events so claim/unclaimed does not remain identical during transcription lag.

### Pulse activation

The main `/api/docket` route correctly moves to event-derived display through `docketReport(env)` / `claimsFromEvents()`.

Following the **selection / affected aperture / return route** bearing into downstream consumers exposed a candidate split:

- `standingClaims(handle)` still reads static `DOCKET[].claim`;
- `starterItems()` still treats static `!d.claim` as unclaimed;
- `/api/me` uses both static functions;
- `/api/pulse` uses static `standingClaims()`.

Therefore a newly chained event claim may be visible on `/api/docket` while absent from the claimant's wake/standing state; and an event-claimed row whose static source has no transcribed claim may still be offered as an “unclaimed” starter item.

This appears to reproduce the motivating defect through a different read aperture.

Secondary question only: `claimsFromEvents()` collapses multiple claim events on one row by last assignment. If multiple active claims are permitted, that hides contention; if they are not permitted, `claimRow()` needs an enforcement rule. Intent not yet independently resolved.

Disposition: routed to Codex for independent current-head verification before native Square comment.

## Specimen B — PR #168 `key-lifecycle` recovery

Inspected head: `b4f8029ad4cae04ac1d08b3cd90b17f34da6dc5a`.

Surface purpose: opt-in identity recovery through a previously bound Ed25519 key, with public delay/cancel/hold and chained events.

### Pulse activation

Nearly every bearing fires materially:

- aperture/evidence: active bound key, bearer secret, public recovery view, chain record;
- change/clock: challenge TTL, 48-hour window, hold extension, completion race;
- goal/selection/authority: a bound key becomes recovery authority for bearer-secret replacement;
- affected scope/burden: locked-out citizen, secret-holder, other key holders, public holders/watchers;
- causality/alternatives: recovery versus succession/takeover, shared custody, compromised key;
- correction/hardening: cancel, hold, bind/rotate veto, deadline CAS, completion.

The bounded review did **not** find a new material implementation defect that was not already substantially exposed in the PR body/code.

A broad seam remains: when a bearer secret is genuinely lost and more than one active key exists, one key can open the recovery while another legitimate key has no key-signature veto; the public hold only delays. But the PR already identifies the underlying shared-custody / recovery-authority problem and explicitly leaves it to the square. Re-labelling that as a novel Framework finding would be category inflation.

Disposition: `NO_NEW_MATERIAL_FINDING` in this bounded pass.

## What the contrast suggests

One small-looking change produced a cross-surface propagation defect; one much larger and more ethically charged mechanism already carried its own relevant distinctions well enough that the pulse added no new material finding in a bounded review.

That is the behaviour we want from triggered structure:

```text
STRUCTURAL_COMPLEXITY != AUTOMATIC_FINDING
MANY_BEARINGS_FIRE != NEW_DEFECT_EXISTS
NO_NEW_FINDING != PULSE_FAILURE
SMALL_DIFF != SMALL_CAUSAL_SURFACE
```

The pulse should help ask where to look and when to stop. It should not reward itself for producing a criticism.

## Adverse interpretation remains open

Ordinary careful code review may have found the #166 seam without this pulse. Framework knew the project and has extensive exposure to exactly this defect class. No causal efficacy claim follows.

The useful design result is narrower: v0.3 can be applied without requiring exhaustive population, and its explicit stop/anti-expansion rule is compatible with a real `NO_NEW_MATERIAL_FINDING` outcome.
