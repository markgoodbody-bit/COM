# 7Q FRESH USE — EXACT RECEIVER PROMPTS — 2026-09-01

Status: PRE-DISPATCH RESEARCH OBJECT / NOT VALIDATION / NOT AUTHORITY

Protocol:
`research/MIDDLE_OUT_7Q_FRESH_USE_PROTOCOL_20260901.md`

These prompts are used unchanged for both R1 and R2 except for the case's already-frozen neutral task text and source-pack attachment.

## Common run conditions

- One fresh isolated receiver session per arm/case.
- Same exact model/version/settings within a case comparison.
- Receiver sees one arm only.
- Receiver sees the exact same frozen external source snapshots and neutral case task for both arms.
- No live browsing/source following during the run.
- Maximum answer: 700 Unicode words.
- Return only the answer to the case task; no meta-commentary about the experiment.
- Do not infer facts absent from the supplied material.

## ARM O — COMPETENT ORDINARY REASONING

Exact instruction:

```text
Read the supplied external source material carefully and answer the supplied case task.

Give your best bounded analysis in ordinary language. State what should happen now, the most important evidence or unknowns, which decisions or authority belong to a domain owner rather than you, the strongest reason your recommendation could be wrong, and what evidence would materially change it.

Do not use Mechanical Ethics, TRACE, middle-out, 7Q, project-specific terminology, or any framework not present in the supplied external sources. Do not invent facts or domain authority.

Maximum answer: 700 words. Return only your answer to the case task.
```

## ARM Q — 7Q-ASSISTED REASONING

Receiver additionally receives the exact text of:
`research/MIDDLE_OUT_ENTRY_7Q_CANDIDATE_20260901.md`
from commit:
`eec157b47c21b34f156e136ead734d4269eb870d`.

Exact instruction:

```text
Read the supplied external source material and the supplied 7Q research aid, then answer the supplied case task.

Use 7Q only as a private reasoning aid. Answer in ordinary language. Do not recite the seven questions, invent project terminology, or assume the aid is correct. If the external source/domain owner explains something better, use that owner rather than the local vocabulary.

Give a concrete bounded action or posture, preserve important unknowns and affected scopes, route decisions you do not own to the appropriate domain/authority owner, and state what evidence would materially change the action.

Do not invent facts or domain authority.

Maximum answer: 700 words. Return only your answer to the case task.
```

## Masking / identity

Receiver-facing run labels must not say `ordinary`, `7Q`, `TRACE`, `ME`, `baseline`, `experimental`, `control`, `preferred`, or `project`.

Use random neutral cell aliases in the run manifest. Underlying arm identity remains evaluator-only until scoring is frozen.

## Failure boundary

If exact same-model isolated sessions cannot be obtained, do not silently compare different model families as an arm effect. Record the limitation and stop or treat the run as exploratory/non-comparative.
