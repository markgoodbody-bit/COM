# EvidenceWatch — pre-pilot intake freeze hardening

Date: 26 September 2026

Status: **INTEGRATED / FREEZE-INTEGRITY REPAIR / NO CONTACT / NO PILOT DATA**

Current EvidenceWatch private main:
`9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f`

PR:
`#17 — Harden pre-unblinding pilot intake freeze`

Reviewed head:
`c30856266a18d0a05dbd7c6d3a2e1e15544f5ad2`

Exact-head cross-platform CI:
`36237885317 / SUCCESS`

Post-merge main CI:
`36237923895 / SUCCESS`
- Ubuntu: SUCCESS
- Windows: SUCCESS
- **62 tests / 62 pass / 0 fail**

## Defect found

PR #16 added a pre-pilot intake and freeze validator, but `requireFrozen: true` could still accept a packet whose minimal identity, completed episode, burden basis and freeze fields were filled while the material comparison surface remained blank.

Specifically, a nominally frozen packet could omit or leave blank:
- current monitoring/currentness handling;
- dependency-map form/ownership/cadence;
- correction/review authority path;
- team-defined success/stop criteria;
- provider/model, residency and retention constraints;
- completed episode's existing tool/signal and action taken.

That created a move-the-goalposts risk:

~~~text
PACKET MARKED FROZEN
+ COMPARATOR DETAILS STILL BLANK
-> DETAILS COULD BE FILLED AFTER EVIDENCEWATCH OUTPUT
~~~

## Repair

A frozen intake now requires:
- status `frozen_pre_unblinding`;
- bounded workflow time window;
- explicit current monitoring/currentness descriptions;
- completed episode existing tool/signal and action taken;
- dependency-map form / maintainer / cadence;
- reviewer / change-authority / disagreement / notification route;
- at least one team-defined success criterion and one stop criterion;
- external-model, residency and retention constraints;
- a real canonical SHA-256 freeze receipt.

Explicit `none`, `not applicable`, or bounded `unknown` text remains valid where true. The validator is not requiring a team to have machinery that does not exist; it is requiring the absence to be stated before unblinding.

## Canonical digest

A syntactically shaped `sha256:<64 hex>` value was not enough.

The final repair adds deterministic key-sorted JSON canonicalisation and computes the intake digest over the complete packet with only the self-referential `freeze.packetDigest` field set to `null`.

Validation recomputes and compares the digest.

Therefore:

~~~text
POST-FREEZE FIELD EDIT
-> DIGEST MISMATCH
-> REFUSE
~~~

Regression explicitly mutates the dependency-map field after freeze and verifies rejection.

## Falsification during build

Two build/test failures were preserved and corrected:

1. Framework's first automated test edit corrupted a dynamic regular-expression assertion. The validator itself compiled; the test file did not. Repaired by using an error-message predicate instead of fragile regex construction.

2. After canonical digest verification was added, the `unmeasured burden` regression changed `burden.basis` after freezing without recomputing the receipt. The validator correctly rejected the packet as tampered before reaching the intended burden guard. The test was corrected by recomputing the digest for the deliberately invalid-but-internally-consistent packet.

No validator weakening was used to make CI green.

## Boundaries

~~~text
FROZEN INTAKE != CONSENT
FROZEN INTAKE != RESEARCHER VALIDATION
VALID DIGEST != TRUE CONTENT
COMPLETE COMPARATOR != EVIDENCEWATCH USEFUL
62/62 TESTS GREEN != PILOT SUCCESS
~~~

No:
- researcher contact;
- participant/personal data;
- provider/model call;
- Digital Science form entry;
- grant submission;
- live Zotero/ReadCube integration.
