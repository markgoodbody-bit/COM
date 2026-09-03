# Bounded Adaptation v0 — source verification / live-target currentness repair

Status: NON-CANONICAL / CONTRACT NARROWING / NO ACTIVATION

## Failure that forced the repair

The 2026-09-03 Square payout field case preserved a concrete public-source failure in which production had been serving settlement changes not yet present in `main`. Reviewing the repository head and reviewing the live operating target were therefore different acts.

That exposes an ambiguity in the v0 cycle receipt. `source_refs[].state = VERIFIED` can establish that the named source coordinate/hash was actually observed and verified. It cannot by itself establish that a repository/source is identical to a live deployed target.

```text
SOURCE_REFERENCE_VERIFIED != LIVE_TARGET_CURRENT
REPOSITORY_CURRENT != DEPLOYMENT_CURRENT
```

## v0 narrowing

The profile now freezes these semantics:

- `VERIFIED` means only that the named source reference was verified as the cycle's observed evidence basis;
- it never means `DEPLOYMENT_MATCH` or `LIVE_TARGET_CURRENT` by implication;
- where a proposed move materially depends on the relationship between a source artifact and a live operating target, that relationship requires separate evidence;
- until that evidence exists, the receipt must preserve `SOURCE_CURRENTNESS_UNKNOWN` rather than convert source verification into deployment assurance.

No new deployment ontology or broad live-control surface is introduced in v0. A later design may add a typed source-to-target relation only if real use shows the unknown code is too lossy.

## Contract identity

The same repair cycle also closes exact identity propagation:

- the profile binds the exact receipt-schema SHA-256;
- the profile binds the exact purpose-constitution SHA-256;
- validated files are pinned to LF and exercised on Windows and Ubuntu;
- fixture receipts use the fixture bundle's prior profile digest only as a template alias, while the validator substitutes the exact current profile digest for ordinary cases and separately proves the stale alias is refused.

This is a contract repair, not evidence that the adaptation loop is useful, safe, autonomous or ready to activate.
