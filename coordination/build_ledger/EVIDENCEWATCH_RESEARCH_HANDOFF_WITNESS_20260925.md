# EvidenceWatch — research reference handoff witness

Date: 25 September 2026

Status: **CONTROLLED ENGINEERING WITNESS PASS / SYNTHETIC CONTENT / REAL-FORMAT CSL JSON / NOT RESEARCHER VALIDATION**

Current EvidenceWatch private main after merge:
`8abb167c16e2bb4504271904c8eaf040734c30fa`

Relevant changes:
- PR #7 — CSL-JSON reference-manager handoff;
- PR #8 — malformed DOI fallback repair;
- PR #9 — controlled research handoff witness.

DOI repair:
- malformed values such as `10.1234/part#section`, `10.1234/part?query`, and `not a DOI` are not turned into doi.org URLs;
- malformed DOI-only records are skipped visibly as `invalid_doi`;
- DOI syntax validation does not establish existence, resolution or source reachability.

Controlled witness:
- source format: CSL JSON shaped like a reference-manager export;
- content: synthetic;
- imported references: **3**;
- skipped references: **1** (`offline-note`, no fetchable URL/DOI);
- initial canonical quantity: **1.8**;
- engine restart preserved quantity: **1.8**;
- controlled publisher correction advanced quantity: **1.2**;
- material event kind: **correction**;
- affected downstream item: `evidence-brief-result`;
- final alerts: **1**.

Hosted witness run:
- GitHub Actions run `36181216784`;
- job `108223780101`;
- witness log reported elapsed harness time **18.76 ms**;
- test summary: **46 tests / 46 pass / 0 fail**.

The elapsed time is machine execution time only. It is **not** researcher setup time, user review time, or evidence of workflow efficiency.

Post-merge CI on main:
- run `36181324265`;
- conclusion **SUCCESS**.

Preserve:
```text
REAL-FORMAT CSL != REAL RESEARCH USER
SYNTHETIC CORRECTION != LIVE SCHOLARLY CORRECTION
ENGINEERING WITNESS != PRODUCT VALIDATION
CSL HANDOFF != LIVE ZOTERO/READCUBE INTEGRATION
DOI SYNTAX VALID != DOI EXISTS
46 TESTS PASS != SEMANTIC RELIABILITY PROVEN
```
