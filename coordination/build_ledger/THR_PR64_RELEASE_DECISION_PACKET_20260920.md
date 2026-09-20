# THR PR #64 — release-decision packet

Date: 20 September 2026 — Europe/London

Status: **READY FOR RELEASE DECISION / NO MERGE PERFORMED / NO HISTORICAL VERDICT CHANGE**

## Candidate

Repository:
`markgoodbody-bit/human-record`

PR:
`#64 — THR: narrow Westermann archival citation route`

Exact head:
`5b0e983f44520f3774ba60ea723a235b71645bb4`

Base:
`09013b2ec47aa1fc60ab7fbd011a33de296ffc83`

State:
`DRAFT / OPEN / MERGEABLE`

Record candidate:
`viral-flak-claim v0.2.8`

Hosted validation:
`run 223 / 35478092259 — SUCCESS`

## Earned delta

The candidate does **not** decide the viral claim.

It improves recoverability and attribution around one already-used scholarly passage:

- Westermann's checked reproduction reports 60 officer + 890 enlisted flak-force casualties, dead/wounded/missing, for 10 May–22 June 1940;
- note 75's `N 529/7` document label/date is recovered from Westermann's note;
- DDB/Bundesarchiv independently matches `RL 12/457` at catalogue level;
- Koch pp. 42–44 is explicitly separated as Westermann's aircraft-destruction comparison rather than silently implied to be the source of 60/890;
- archival pages remain uninspected;
- the 60/890 archival basis remains unknown;
- the true whole-war aggregate flak mortality rate remains unknown.

## Independent review

Codex comment:
`5746324900 — PASS_WITH_CEILINGS`

Reviewed exact head:
`5b0e983f44520f3774ba60ea723a235b71645bb4`

The review independently rechecked:
- Westermann note 75 text;
- RL 12/457 DDB catalogue metadata;
- five changed surfaces;
- record/view blob alignment;
- hosted validation result.

Ceilings retained:
- third-party Westermann reproduction not authenticated to publisher edition;
- exact N 529/7 catalogue item not independently verified;
- archival contents not inspected;
- no independent verification of the 60/890 casualty figure;
- review is not merge/deployment approval or historical validation.

## Falsification / drift result

x100 receipt:
`coordination/build_ledger/THR_FLAK_FALSIFICATION_X100_DRIFT_20260920.md`

Result:
- 70 SURVIVES;
- 13 CEILINGS;
- 10 WARNINGS;
- 1 REPAIR;
- 6 STOP CONDITIONS.

One control defect found during falsification—stale PR-body exact-head/check metadata—was repaired.

The research seam is now saturated.

## Public consequences if merged

Would change the existing flak record from v0.2.7 -> v0.2.8 across:
- Markdown record;
- machine-readable record;
- human reader page;
- catalogue view basis;
- assertion scope/version.

Would **not**:
- create a fifth record;
- change claim status;
- establish the viral claim false;
- establish a replacement mortality rate;
- create a new THR type/registry semantic;
- merge RFC #52;
- contact Bundesarchiv;
- authorize any fee;
- change THR stewardship/governance.

## Release options

### MERGE CURRENT CANDIDATE

Meaning:
accept the narrower source/citation repair into public THR main while retaining all ceilings.

### HOLD

Meaning:
leave public v0.2.7 unchanged until new evidence or another release reason appears.

### REJECT / CLOSE UNMERGED

Meaning:
judge the delta too small or too maintenance-heavy to justify a public revision.

## Framework disposition

```text
TECHNICAL / EVIDENCE GATES = SATISFIED WITH CEILINGS
FURTHER RESEARCH REQUIRED FOR THIS DELTA = NO
EXTERNAL HUMAN CONTACT REQUIRED = NO
RECORD GROWTH = NO
RFC GROWTH = NO

RELEASE DECISION = CLEANLY SEPARABLE
```

No merge was performed by preparation of this packet.

`READY_FOR_DECISION != RELEASED`
`MERGED_RECORD != HISTORICAL_VERDICT`
