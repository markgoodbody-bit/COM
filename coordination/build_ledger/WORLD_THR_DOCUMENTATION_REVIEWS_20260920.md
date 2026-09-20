# Human Record documentation reviews — bounded return

Date: 20 September 2026 — Europe/London

Status: **TWO EXACT-HEAD HOSTILE REVIEWS RETURNED / NO MERGE APPROVAL**

## Source basis

Reacquired before review:

- COM main: `f1483f95077f96ae9d97d098475b97b2ab1d67bf`;
- Human Record main: `9f9246c76348cd2f3a4d4f3501b4bf5af65e96db`;
- PR #70 head: `6ee3faf75ea8b0198b7ef1f79d882c8d097dba7f`;
- PR #72 head: `08e0bb9e836046f52b8fbadb54ce765afd2b0fa4`.

Reads were bounded to the complete PR diffs/comments plus the relevant current `SOURCE_MODEL.md` and `RECORD_CONTRACT.md` sections. These reviews do not establish correctness of every Human Record document or completeness of external provenance practice.

## PR #70 — source genesis

Return: **PASS_WITH_CEILINGS**

Receipt comment:
https://github.com/markgoodbody-bit/human-record/pull/70#issuecomment-5753264242

Findings:

- current THR observation records preserve bounded retrieval/inspection time, not source generation time;
- the draft does not infer generation time from observation time;
- claimant-created support is treated as downstream/non-independent for the support question, not automatically false;
- W3C PROV and C2PA remain the stronger semantic owners;
- the materiality-qualified RECORD_CONTRACT question is a justified checklist surface;
- no registry field, source type, schema/validator change or fifth record is earned.

## PR #72 — missing-value reason

Return: **PASS_WITH_CEILINGS**

Receipt comment:
https://github.com/markgoodbody-bit/human-record/pull/72#issuecomment-5753264295

Findings:

- current THR preserves unknowns and bounded misses but does not explicitly preserve the action-relevant reason for missingness;
- the addition remains record-level guidance and does not adopt CIDOC issue 723's unresolved modelling vocabulary;
- `not applicable` is limited to the particular subject;
- `known but withheld` remains separate from absence;
- bounded search language does not become a world claim;
- current inability does not establish `unknowable`;
- no enum, schema/validator change, new type or fifth record is earned.

## Preserved ceilings

```text
REVIEW RETURN != MERGE APPROVAL
DOCUMENTATION CANDIDATE != RECORD 5
OWNER ROUTING != THR NOVELTY
PASS_WITH_CEILINGS != GENERAL VALIDATION
```

Both pull requests remain drafts. This receipt does not merge or publish them.
