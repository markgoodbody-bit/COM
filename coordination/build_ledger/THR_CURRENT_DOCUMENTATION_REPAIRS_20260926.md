# The Human Record — current-main documentation repair receipt

Date: 26 September 2026

Status: **INTEGRATED / DOCUMENTATION ONLY / FOUR RECORDS REMAIN FOUR / NO SCHEMA GROWTH**

Current THR main:
`0694ea9f4b9371ff635035bd2cc90dfd08e9632a`

## Repair 1 — source genesis / antecedence

Fresh current-main PR #78 re-ported the useful residue from stale #70.

Integrated:
- `RECORD_CONTRACT.md`: when material, preserve whether a source pre-existed the claim it is used to support or was generated/altered downstream;
- `SOURCE_MODEL.md`: observation time does not establish generation time, prior existence or independence;
- stronger owners remain W3C PROV for generation/derivation/attribution/primary-source semantics and C2PA for bound-asset ingredient/action provenance.

Preserve:
```text
SOURCE RETRIEVABLE AT T2 != SOURCE EXISTED BEFORE CLAIM AT T1
OBSERVED_AT != GENERATED_AT
PUBLIC URL != PREEXISTING EVIDENCE
CLAIMANT-CREATED SUPPORT != INDEPENDENT CORROBORATION
SOURCE GENESIS MATTERS != NEW THR SOURCE TYPE
```

PR #78 exact head:
`14ce6384d671023819846014556107be9bd5fd5e`

Hosted candidate integrity:
`36200310614 / SUCCESS`

Merged:
`223b27a1f4fcce853e6e312bea4005d289c5ecf5`

Post-merge:
- integrity `36200381875 / SUCCESS`;
- Pages `36200381811 / SUCCESS`.

Original stale #70 is closed unmerged with lineage preserved.

## Repair 2 — action-relevant reasons for missing values

Fresh current-main PR #80 re-ported the useful residue from stale #72 **after #78 had merged**, so both documentation repairs were reviewed serially rather than relying on an automatic conflict merge.

Integrated into `RECORD_CONTRACT.md`:
- not examined / not yet sought;
- sought within a stated bound but not obtained;
- inaccessible or restricted;
- not applicable;
- known but withheld;
- explicit refusal to infer `unknowable` from current non-recovery.

The trigger remains CIDOC CRM issue 723, but THR adopts no proposed CIDOC enum/vocabulary and does not decide the unresolved CRM modelling question.

Preserve:
```text
EMPTY FIELD != ONE EPISTEMIC STATE
CURRENTLY UNRECOVERED != UNKNOWABLE
WITHHELD != ABSENT
DOCUMENTATION STATE != CLOSED-WORLD CLAIM
```

PR #80 exact head:
`b93df6c4a33c9eb9e68032eb32f83e60f5d1c2e2`

Hosted candidate integrity:
`36200440715 / SUCCESS`

Merged current main:
`0694ea9f4b9371ff635035bd2cc90dfd08e9632a`

Post-merge:
- integrity `36200466240 / SUCCESS`;
- Pages `36200465585 / SUCCESS`.

Original stale #72 and intermediate post-old-base #79 are closed unmerged with lineage preserved.

## Stale branch cleanup

Also closed as superseded:
- #61 — Hannibal edition/recovery draft, superseded by current-main #77;
- #60 — flak phrase-level analogue, whose useful RAF/Bomber Command 80-percent residue already exists in current main;
- #64 — Westermann archival route, whose `N 529/7` / `RL 12/457` recoverability residue already exists in current main.

No evidence was deleted; Git/PR history remains.

Current THR open-PR surface after cleanup:
- #52 only — exploratory fractal record architecture RFC / deliberately provisional.

## Non-changes

```text
PUBLIC RECORDS = 4
RECORD 5 = NOT EARNED
NEW GLOBAL TYPE = NO
SCHEMA MIGRATION = NO
VALIDATOR SEMANTIC GROWTH = NO
CATALOGUE RECORD ADDITION = NO
DOCUMENTATION REPAIR != THR VALIDATION
```
