# THR browse-card freshness repair — 25 September 2026

Status: **MERGED / MAIN INTEGRITY GREEN / PAGES DEPLOYED / NO RECORD OR SCHEMA GROWTH**

Trigger:
A real public `records/index.html` Camp Fire card remained stale after the detailed underlying record had been updated. Existing THR controls pinned each per-record human view to its source record bytes, but the browse catalogue was another derived reading surface with no equivalent currentness brake.

Old draft:
- THR PR #68, based on older main;
- carried a `path@sha` comment syntax;
- never received its requested hostile return;
- closed unmerged as superseded.

Current repair:
- THR PR #76;
- reviewed exact head `be20322ae8208ba77e231ea77617863f1a47ba22`;
- merge commit / current main `c7be1efb5ca66673c398cdc19eb4c0f2489246d9`.

Mechanism:
- each actual `<article class="record-card">` carries its catalogue record ID and a SHA-256 over the existing `view_basis.source_git_blobs` map;
- the digest is computed from deterministic JSON canonicalization inside the validator;
- validator fails missing, malformed/invalid, duplicate, unknown or stale card bases;
- stale/missing failures expose the expected current digest so review/re-pin is reachable;
- source paths are not copied into a second HTML path grammar;
- RECORD_CONTRACT explicitly classifies the browse catalogue as a derived reading surface.

Hostile shrink during the current re-port:
1. first current re-port used JSON comments containing the source-path map;
2. review rejected that shape because the comment was not structurally attached to a card and still copied path strings into HTML;
3. final mechanism moved the identity/digest onto the actual record-card element and hashes the existing basis map instead;
4. intermediate source/validator mismatch commits failed CI rather than appearing green.

Exact-head hosted validation:
`Validate Human Record integrity / 36196988375 / SUCCESS`

Observed in exact-head job:
- full integrity pipeline PASS;
- **129 tests / OK**;
- the existing seven open-vocabulary warnings remain visible as warnings;
- no truth/identity/preservation upgrade.

Post-merge:
- main-push integrity `36197053456 / SUCCESS`;
- Pages build/deployment `36197052804 / SUCCESS`;
- contribution-packet public-delivery workflow did not run because none of its scoped packet/discovery files changed.

Scope:
- four browse-card attributes;
- RECORD_CONTRACT clarification;
- validator guard;
- regressions.

No change to:
- record evidence or prose sources;
- record count (still exactly four);
- registries or registry semantics;
- assertion/source/identity models;
- schema/global types;
- THR stewardship;
- record 5.

Preserve:
```text
SOURCE BYTES / DECLARED ROUTES CHANGED
-> BROWSE CARD REVIEW REQUIRED

DIGEST MATCH != SUMMARY TRUE
CARD BASIS != NEW EVIDENCE
DERIVED VIEW != SOURCE
CI GREEN != THR VALIDATED
```

The guard cannot prove a human actually reread the card before updating a digest. It turns source-basis drift into a fail-closed maintenance event; semantic correctness remains a review/evidence question.
