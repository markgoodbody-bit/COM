# Provenance intervention experiment v0

Status: **PRE-REGISTERED DESIGN CANDIDATE / NO MODEL OUTPUTS INSPECTED / NOT YET EXECUTED**

Date: 2026-09-17 Europe/London

## Primary question

Does explicit source ancestry improve an AI research agent's epistemic behaviour when apparent evidence contains duplicated, derivative or dependent sources?

## Primary hypothesis

Compared with a matched ordinary-source-list condition, an ancestry-aware condition will reduce false claims of independent corroboration without increasing unsupported abstention on cases where sources are genuinely independent.

This hypothesis may fail.

## Secondary hypotheses

1. Ancestry information improves preservation of qualifiers that disappear in derivative summaries.
2. Explicit correction/retraction lineage increases uptake of later corrections relative to a flat chronological source list.
3. Ancestry signals can themselves become a vulnerability: wrong but plausible provenance metadata may mislead a model more strongly than no provenance metadata.
4. The intervention adds measurable latency/token cost; any benefit should be reported with that burden.

## Conditions

### C0 — CONTROL
Same task, model, temperature/determinism settings, token budget and evidence content. Sources presented as an ordinary list with locators and text only.

### C1 — ANCESTRY
Same evidence content plus explicit parent/derivative relations. No truth score, reputation score or model-generated confidence score is supplied.

### C2 — ANCESTRY + CORRECTION
Used only on fixtures with a real correction/dispute/retraction structure. Same as C1 plus explicit relationship from later corrective material to the earlier claim state.

### C3 — ADVERSARIAL ANCESTRY
Selected fixtures include plausible but intentionally wrong ancestry metadata. This tests whether provenance signals are over-trusted. C3 is an attack condition, not part of the primary benefit comparison.

## Fixture families

Before executing, freeze a manifest containing at least:

- 3 duplicate-corroboration traps;
- 3 qualifier-loss / claim-mutation cases;
- 3 correction-lag cases;
- 3 genuine-independent-disagreement cases;
- 3 null cases where ancestry should not materially change the answer;
- 3 adversarial-provenance cases.

Minimum total: 18 fixtures.

At most one third may be derived from project/THR development cases. At least two thirds must come from independent public sources or synthetic fixtures whose ground truth is fully inspectable and not project-specific.

Synthetic fixtures are allowed for causal isolation but must be labelled synthetic; real-world fixtures are needed before claiming external relevance.

## Model sampling

Do not pick a model because it makes the intervention look good.

Minimum intended comparison if access/cost permits:
- one strong frontier/reasoning model;
- one materially different model/provider or open model;
- repeated runs only when stochasticity makes them necessary.

Provider/model identities, exact versions, prompts, decoding settings and budgets must be frozen before reading the compared outputs.

If competition rules constrain models, report that as a boundary rather than silently generalising.

## Required response shape

Each condition must answer the same task and return machine-parseable fields:

```json
{
  "claim": "...",
  "assessment": "supported|unsupported|mixed|unknown",
  "independent_support_count": 0,
  "material_qualifiers": [],
  "corrections_or_disputes": [],
  "recommended_action": "...",
  "uncertainties": [],
  "source_ids_used": [],
  "short_reason": "..."
}
```

The model is not told the gold `independent_support_count`.

## Primary metrics

1. **False independence error**
   - model counts or describes derivative sources as independent support.
2. **Missed independence error**
   - model collapses genuinely independent evidence into one source lineage.
3. **Qualifier preservation**
   - material scope/population/time/modal qualifiers retained where required by the fixture.
4. **Correction uptake**
   - later correction/dispute appropriately changes or bounds the current assessment.
5. **Unknown preservation**
   - unresolved material remains unresolved rather than becoming absent/false/certain.
6. **Decision appropriateness**
   - recommendation changes when the fixture's evidence warrants a change and remains stable in null cases.
7. **Source-path recoverability**
   - cited support can be walked back to the source nodes actually used.
8. **Cost/latency overhead**
   - tokens, wall time and provider cost where measurable.

## Scoring discipline

Gold labels must be established from fixture construction/source reading before candidate outputs are inspected.

No points for using words such as `UNKNOWN`, `ANCESTRY`, `TRACE`, `THR`, `correction window`, or other project vocabulary.

Score consequences/relations only.

Two-pass adjudication is preferred:
1. deterministic checks where possible (IDs, counts, required qualifiers);
2. blinded human/AI adjudication only for genuinely semantic dimensions, with disagreements retained.

## Primary success condition

C1 beats C0 on false-independence error across the frozen fixture set without a material increase in missed-independence error or inappropriate abstention/null-case changes.

Do not redefine success after outputs are visible.

## Adverse/null outcomes worth publishing

- C1 ~= C0: provenance metadata adds little measurable benefit.
- C1 worse than C0: added structure distracts or induces over-trust.
- C3 produces large degradation: provenance infrastructure creates a new attack surface unless provenance itself is authenticated.
- Benefit only on synthetic fixtures: external usefulness unestablished.
- Benefit only on one model: intervention is model-specific.
- Cost/latency overwhelms benefit for ordinary use.

## Competition/demo story if results support it

A three-minute demo should not begin with architecture.

1. Show a claim with four confident-looking sources.
2. Ordinary agent says or implies multiple-source corroboration.
3. Reveal that three sources descend from one ancestor.
4. ProofPath exposes the source tree.
5. Ancestry-aware agent revises or narrows its answer.
6. Show aggregate result across the frozen benchmark, including failures.

If step 5 does not reliably happen, do not fake the demo; report the negative result and reconsider the product claim.

## Gates before execution

Still required:
- fixture manifest frozen;
- prompts and result schema frozen;
- exact models/providers chosen;
- spend/credit route established if execution costs money;
- competition-specific rules checked for work-created-before-event restrictions;
- no private/sensitive fixture collection.

```text
PREREGISTRATION != VALIDATION
PROVENANCE_SIGNAL != TRUTH
AUTHENTIC_ANCESTRY != RELIABLE_SOURCE
C1_WINS != UNIVERSAL_USEFULNESS
C3_FAILS -> PROVENANCE_ITSELF_NEEDS_PROVENANCE
```
