# OpenAI Researcher Access Program — eligibility hold / reusable research summary

Status: **HOLD / CURRENT KNOWN STANDING DOES NOT SATISFY FAQ ELIGIBILITY / NOT SUBMITTED**  
Prepared: 17 Sep 2026  
Programme page: https://openai.com/form/researcher-access-program/  
Current FAQ: https://help.openai.com/en/articles/10139500-researcher-access-program-faq

## Controlling eligibility finding

The public programme page encourages early-stage researchers and researchers with limited financial and institutional resources. However, the current programme FAQ is more specific: eligible applicants are researchers with an **active affiliation to an academic institution or other research organization**, or nonprofits conducting research activities.

Mark's currently established standing for this lane is independent researcher / engineer. No qualifying academic, research-organization or nonprofit affiliation has been supplied for this application.

Therefore:

```text
CURRENT DISPOSITION = DO NOT APPLY
INDEPENDENT RESEARCH ACTIVITY != QUALIFYING AFFILIATION
BROAD PROGRAMME PAGE != FAQ ELIGIBILITY
```

Do not create an account, submit a form, or imply institutional affiliation on the current facts.

The research text below is retained only because it may be reusable for another legitimate funding route, or for this programme if eligibility later changes.

---

## Reusable working title

**Testing provenance-sensitive evidence handling in AI decision agents**

## Reusable research question

Do current AI research and decision agents become more confident or take a stronger downstream action when one evidentiary origin is made to look like multiple corroborating sources? If that failure occurs, can explicit source-ancestry information reduce it without making the agent systematically over-cautious or less responsive to genuinely independent evidence?

## Reusable project summary

AI agents increasingly gather, summarize and act on evidence from multiple reports. A basic problem is that multiple reports may descend from the same underlying evidence. Existing work has established that report multiplicity is not the same as evidential independence; this project does not claim to discover that mechanism.

The project tests a narrower behavioural question: whether current language-model agents operationally mishandle provenance-equivalent evidence at the point where they express confidence or make a decision, and whether a small, inspectable provenance intervention improves that behaviour.

The study uses preregistered evidence mutations, unchanged baseline replicates, null and positive controls, blinded wrong-ancestry controls, and a bidirectional guard requiring the agent to remain responsive to genuinely independent evidence. Negative and inconclusive results are retained rather than tuned away.

## Method

### Stage A — reproduce or kill the failure cheaply

For each target model:
- 15 baseline runs;
- 15 byte-identical baseline-replicate runs to estimate ordinary run-to-run variation;
- 15 runs after adding a second report that preserves the same distinctive factual content in different wording but does not add another evidentiary root.

The primary measurement is whether confidence or approval/action strength increases beyond the preregistered effect/statistical gate relative to the pooled unchanged baselines.

If Stage A does not reproduce the effect, the product/research claim is shrunk or stopped rather than rescued by changing thresholds after seeing outputs.

### Stage B — only if Stage A survives

Compare the same frozen cases under:
1. raw evidence;
2. an ordinary plain-language caution about source dependence;
3. correct structured ancestry;
4. a blinded plausible wrong-ancestry control;
5. a lineage-aware hardening rerun.

The intervention only counts as useful if it reduces false corroboration while preserving response to verified independent evidence.

### Reproducibility

The working harness preserves:
- frozen agent-facing request identities;
- exact model/condition/run identity;
- append-only response and usage records;
- explicit jitter/null controls;
- deterministic fixture validation;
- negative results and failed experimental designs.

Where licensing permits, fixtures, code, methods and null results can be made publicly inspectable.

## Prior-work boundary

This is not a claim that provenance, metamorphic testing, agent evaluation, or source-dependence are new.

Relevant existing owners include:
- Marc Bara, *Epistemic Sybil Resistance* — evidential ancestry / report multiplicity mechanism;
- NIST's agentic evaluation probes — general evidence-grounding probes and audit trails;
- existing agent/metamorphic evaluation systems — generic mutation, runner, CI and reporting infrastructure.

The empirical delta under test is deliberately narrower: **provenance-specific behavioural mutations at the decision/action layer, with stochastic controls and an inspectable hardening comparison.**

## Potential API-credit use if a legitimate funding route supports it

Credits would be used only for bounded, reproducible model evaluations and replications:
- controlled Stage A screens across current models;
- additional frozen fixtures only if the first failure survives;
- plain-language / correct-ancestry / wrong-ancestry controls;
- hardening reruns;
- cross-model replication and robustness checks.

Credits would not be used to manufacture scale after a null result. The experiment has an explicit stop rule.

## Expected outputs

Depending on results:
- open or publicly inspectable experimental fixtures and measurement code where licensing permits;
- a reproducibility record including null/inconclusive outcomes;
- a short technical write-up describing the measured effect or lack of effect, controls, limitations and nearest prior work;
- if warranted, a minimal provenance-mutation pack that can interoperate with stronger existing evaluation tooling rather than duplicating a generic eval platform.

## Limitations stated in advance

- One model failure does not establish a general model defect.
- Report similarity is not proof of shared ancestry.
- Supplied provenance is not proof of truth or independence.
- Structured metadata may change model attention independently of its correctness; the wrong-ancestry control exists to test this.
- A green deterministic harness is not an empirical model result.
- A null result is a valid outcome.

## Re-open gate

Only reconsider this specific programme if:
- [ ] a qualifying active academic/research-organization affiliation is accurately established; or
- [ ] OpenAI changes the current eligibility rule and that change is verified from the owner source.

`HOLD != REJECTION`
`CURRENTLY_INELIGIBLE != FOREVER_INELIGIBLE`
`CORRECTION_BEFORE_APPLICATION > FIT_RATIONALISATION`
