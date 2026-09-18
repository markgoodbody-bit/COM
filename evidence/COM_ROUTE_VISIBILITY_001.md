# COM route visibility witness — 18 September 2026

Status: **BOUNDED REPRODUCTION / SUPPORT FOR ISSUE #18 / NOT VALIDATION OF COM**

## Original observed problem

COM issue #18 recorded on 28 July 2026 that COM protocol traffic was being carried on two repositories with different audiences:

- `markgoodbody-bit/COM` — PUBLIC;
- `markgoodbody-bit/campfire-relay` — PRIVATE.

The issue argued that COM represented both as routes without a bounded way to preserve who could inspect each carrier.

## Fresh reproduction

Framework re-read the repository metadata on 18 September 2026 using the connected GitHub route.

Observed:

`markgoodbody-bit/COM` -> `visibility: public`

`markgoodbody-bit/campfire-relay` -> `visibility: private`

The original factual contrast therefore still exists at this bounded observation.

## Why the distinction matters

The same semantic event or witness can be carried through surfaces with different inspectability. Later claims such as 'this was publicly checkable', 'the source was available to an outside reviewer', or 'the only evidence was in a restricted route' cannot be reconstructed from route identity alone unless the observer knows the carrier's audience state.

Current examples across the project also make the distinction practical:

- public COM issues versus private conversations used as authority sources;
- public THR contribution/correction routes versus relay/private transport before publication;
- PSFH guest marks intended for public display versus operator/removal receipts and retained backups that must not become public merely because they exist.

These examples do not require one universal visibility label on every event. The field is only needed when inspectability changes the meaning of a later claim.

## Important narrowing of the 28 July argument

The original issue said public and private witnesses were 'different evidential kinds'. That is too strong if read as a ranking.

`PUBLIC` does not mean true, independent, authoritative or well-audited.

`PRIVATE` does not mean false, confidential in an absolute sense, correlated, or unusable.

A private route may contain stronger primary evidence than a public one. A public route may contain repeated nonsense.

The exact surviving distinction is:

> **the set of observers who could inspect the carrier at the stated boundary can differ, and that difference may be consequential to later provenance or audit claims.**

Therefore the proposed repair records visibility/audience as bounded route state rather than an evidence score.

## Candidate semantics

When consequential:

`route_visibility: PUBLIC | RESTRICTED | PRIVATE | UNKNOWN`

`visible_to: <bounded audience/scope actually established>`

`visibility_basis: <carrier metadata / access configuration / bounded observation>`

Ceilings:

`PUBLIC != AUTHORITATIVE`

`PRIVATE != CONFIDENTIALITY GUARANTEED`

`DIFFERENT VISIBILITY != INDEPENDENT EVIDENCE ROOT`

`ROUTE VISIBILITY != ACTION AUTHORITY`

`FAILED READ != PRIVATE ROUTE`

`AUTHENTICATED READ != PUBLIC ROUTE`

## No migration claim

No historical backfill is required. Old events remain interpretable from their preserved evidence where available. The optional field is for future/current witnesses where visibility materially affects coordination.

`OBSERVED_ROUTE_VISIBILITY != TIMELESS_AUDIENCE`