# THR field pressure — action-relevant reasons for missing values

Date: 20 September 2026 — Europe/London

Status: **REAL OWNER-SIDE PRESSURE / DRAFT DOC REPAIR / NO TYPE / NO RECORD 5**

## Trigger

CIDOC CRM issue 723 opened 14 September 2026 on a provenance-record problem:
an empty field cannot distinguish whether a value was never sought, sought but
not obtained, not applicable, or otherwise unavailable.

The CIDOC discussion is active and the correct modelling home remains unresolved
between CRMbase, CRMinf and implementation guidance.

## THR check

Current THR records already distinguish some cases in prose:
- not checked / not examined;
- bounded search misses;
- failed retrieval;
- access restriction;
- unknown / unresolved.

But the minimum RECORD_CONTRACT does not explicitly say that the **reason** a
value is missing can change what a later researcher should do.

## Smallest candidate delta

Human Record draft PR #72:
`THR: distinguish action-relevant reasons for missing values`

Exact head:
`08e0bb9e836046f52b8fbadb54ce765afd2b0fa4`

Base:
`9f9246c76348cd2f3a4d4f3501b4bf5af65e96db`

One file only:
`RECORD_CONTRACT.md`

Candidate distinctions, only when material:
- not examined / not yet sought;
- sought within a stated bound but not obtained;
- inaccessible / restricted;
- not applicable;
- known but withheld, explicitly not absence.

The draft refuses to infer `unknowable` from current inability to recover a value.

## Stronger-owner boundary

Do not adopt CIDOC issue 723's proposed vocabulary or decide its model location.

```text
EMPTY FIELD != ONE EPISTEMIC STATE
CURRENTLY UNRECOVERED != UNKNOWABLE
WITHHELD != ABSENT
DOCUMENTATION STATE != CLOSED-WORLD CLAIM
```

No schema.
No enum.
No validator change.
No record changes.
No record 5.

Bounded hostile-review request:
PR #72 comment `5746552872`.

## Next

```text
ONE BOUNDED REVIEW
-> REPAIR IF EARNED
-> HOLD / RELEASE DECISION SEPARATE
-> FOLLOW CIDOC OWNER DISCUSSION
```
