# THR field pressure — source genesis vs observed evidence

Date: 20 September 2026 — Europe/London

Status: **REAL FIELD PRESSURE / DRAFT DOC REPAIR / NO NEW TYPE / NO RECORD 5**

## Trigger

OpenAI's 16 September 2026 misalignment disclosure reports an unreleased model
that uploaded a file to the internet so it could cite that file in its answer.

Material pressure:

```text
SOURCE RETRIEVABLE AT T2
!=
SOURCE EXISTED BEFORE CLAIM AT T1

OBSERVED_AT != GENERATED_AT
PUBLIC URL != PREEXISTING EVIDENCE
CLAIMANT-CREATED SUPPORT != INDEPENDENT CORROBORATION
```

The point is not that claimant-created material is automatically false. The point
is that its existence cannot be counted as independent antecedent evidence merely
because it is publicly fetchable.

## Stronger-owner subtraction

W3C PROV already owns general provenance semantics for generation, attribution,
derivation and primary-source relations, including:
- generatedAtTime;
- wasGeneratedBy;
- wasAttributedTo;
- wasDerivedFrom;
- hadPrimarySource.

C2PA owns asset-origin / action / ingredient provenance for media and other bound
assets.

Therefore:

```text
REAL PRESSURE != NEW THR ONTOLOGY
SOURCE GENESIS MATTERS != NEW THR SOURCE TYPE
```

## THR current gap

THR's current source observations record `observed_at` for retrieval/inspection
events. That establishes when THR observed a representation, not when the source
was generated or whether it pre-existed the claim it supports.

The distinction was not explicit enough in `SOURCE_MODEL.md` or the minimum
`RECORD_CONTRACT.md`.

## Draft repair

Human Record draft PR #70:
`THR: distinguish observed sources from antecedent evidence`

Exact head:
`6ee3faf75ea8b0198b7ef1f79d882c8d097dba7f`

Base main:
`9f9246c76348cd2f3a4d4f3501b4bf5af65e96db`

Changes:
- SOURCE_MODEL: explicit observation-time vs generation-time / antecedence boundary;
- RECORD_CONTRACT: when material, preserve whether a source pre-existed the claim
  or was generated/altered downstream;
- explicit PROV/C2PA stronger-owner references.

No registry migration.
No schema change.
No validator change.
No current public record changed.
No OpenAI incident added as a THR record.

Hostile review request:
PR #70 comment `5746539170`.

## Boundaries

```text
FIELD CASE = PRESSURE
FIELD CASE != RECORD 5

DOCUMENTATION DELTA = CANDIDATE
DOCUMENTATION DELTA != THR VALIDATED

REAL URL != PREEXISTING EVIDENCE
DOWNSTREAM SOURCE != AUTOMATICALLY FALSE
DOWNSTREAM SOURCE != INDEPENDENT ANTECEDENT SUPPORT
```

## Next

```text
FOLLOW ONE BOUNDED INDEPENDENT REVIEW
-> REPAIR IF EARNED
-> THEN HOLD / RELEASE DECISION SEPARATE

NO TYPE GROWTH
NO RECORD GROWTH
RETURN TO WORLD AFTER THIS BOUNDED CHECK
```
