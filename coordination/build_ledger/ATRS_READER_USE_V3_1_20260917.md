# ATRS Reader-Use v3.1 — final pre-human-gate receipt

Recorded: 2026-09-17 Europe/London

Status: **HOSTED GREEN / PRIVATE KEY NARROWED / INDEPENDENT RECHECK REQUESTED / NO HUMAN RESULT / HUMAN STUDY NOT AUTHORISED**

This addendum supersedes only the v3 private-key witness in `ATRS_READER_USE_V3_20260917.md`. Participant-facing conditions did not change.

## Exact hosted witness

```text
head = 6fa24cb12c7b9720ee5b32fa5b8c8b84ef7842d9
task-pack run = 35272269260 SUCCESS
artifact = 10518547136
artifact sha256 = 09764a039e47ef39a5e19a998e888fb48f7e76bb9c4de5c9ed858af1ee007f3c
ordinary #364 CI same head = 35272275933 SUCCESS
```

## Narrow v3.1 private-key corrections

Built-artifact readback found two source-fidelity overclaims:

1. HRA: `queries@hra.nhs.uk` is explicitly tied to the tool-outcome-query route. A separate sentence says a user can contact HRA for further advice but does not explicitly bind that second route to the same email. v3.1 therefore keys the second route's channel as `NOT STATED`.
2. Wilton Park: the data-removal sentence explicitly says `Any individual`; v3.1 uses `individual`, not the broader combined `individual/customer` phrase.

These are private-key corrections. FULL / EXCERPT / LENS participant surfaces are unchanged.

## Bounded artifact inspection

Framework downloaded the exact v3 hosted artifact and independently checked:

- every exposure position 1–9 contains `FULL / EXCERPT / LENS = 2 / 2 / 2` across the six schedules;
- every scored case appears in each condition exactly twice;
- all nine scored EXCERPT/LENS pairs carry identical published source-passage text;
- all nine scored EXCERPT/LENS pairs expose the same extracted contact-token values;
- no `route_bundles`, private-key status, or answer-key material was present in participant files.

This is an artifact/coherence witness, not usability evidence.

## Independent recheck

Current #364 review request: comment `5720893396`, with v3.1 addendum `5720943597`.

Requested return: `KILL / REPAIR / SURVIVES AS PILOT METHOD` on the narrow built artifact only.

No human run follows automatically from a clean return.

## Apart competition boundary

Fresh current public source confirms the Nov 13–15 AI x Epistemics Sprint is a three-day sprint in which participants pick an open problem, build the benchmark/tool/product/study and write up what they found. Current public text checked by Framework did not expose an explicit pre-existing-work rule.

Historical Apart precedent is informative but not current authority: the 2024 AI Governance Sprint explicitly allowed participants to think about a project beforehand while saying core research work should occur during the hackathon.

Safe posture remains:

```text
SEPTEMBER = PILOT / METHOD / FALSIFICATION / FROZEN BASELINE
NOVEMBER = FRESH SUBSTANTIVE CORPUS / ANALYSIS / RESULT IF LIVE RULES SUPPORT IT
HISTORICAL_RULE != CURRENT_NOVEMBER_RULE
```

Re-read live Guidelines/terms at the registration/submission human gate. No organiser contact is currently needed.

## Current stop

Further internal method polishing without a concrete hostile-review defect is drift.

The next materially new evidence after a clean independent method recheck would be real participant data, which is a separate explicit Mark gate and requires a frozen recruitment/consent/data-minimisation/sample/allocation/analysis plan first.

```text
METHOD_PACK != HUMAN_RESULT
GREEN_METHOD != READER_BENEFIT
EXCERPT ~= LENS -> ROUTE_TO_SIMPLER_OWNER
NULL_RESULT = VALID
OWNER_FOUND = VALID
SELECTED_ENTRY = NONE
REGISTERED = NO
SUBMITTED = NO
HUMAN_STUDY_RUN = NO
```
