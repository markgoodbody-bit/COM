# OpenAI Researcher Access Program — non-binding application draft

Status: **DRAFT / NOT SUBMITTED / ACCOUNT + IDENTITY + POLICY ACKNOWLEDGEMENT ARE HUMAN GATES**  
Prepared: 17 Sep 2026  
Owner page: https://openai.com/form/researcher-access-program/

This draft is deliberately shaped around the current empirical research object rather than the wider Mechanical Ethics / TRACE project. Do not broaden it to make the application sound grander.

## Applicant standing

**Independent researcher / engineer using public and open research materials.**

Human-gate fields still required at submission:
- legal/preferred name as the form requires;
- email/contact details;
- country/other identity fields;
- SurveyMonkey Apply account creation;
- final review of OpenAI sharing/publication and usage policies.

Do not imply university, nonprofit, laboratory, employer or institutional affiliation unless Mark explicitly supplies one for this application.

## Working project title

**Testing provenance-sensitive evidence handling in AI decision agents**

## Research question

Do current AI research and decision agents become more confident or take a stronger downstream action when one evidentiary origin is made to look like multiple corroborating sources? If that failure occurs, can explicit source-ancestry information reduce it without making the agent systematically over-cautious or less responsive to genuinely independent evidence?

## Project summary

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

Where licensing permits, fixtures, code, methods and null results will be made publicly inspectable. Any publication or sharing will follow the program's sharing/publication policy and applicable provider policies.

## Prior-work boundary

This is not a claim that provenance, metamorphic testing, agent evaluation, or source-dependence are new.

Relevant existing owners include:
- Marc Bara, *Epistemic Sybil Resistance* — evidential ancestry / report multiplicity mechanism;
- NIST's agentic evaluation probes — general evidence-grounding probes and audit trails;
- existing agent/metamorphic evaluation systems — generic mutation, runner, CI and reporting infrastructure.

The empirical delta under test is deliberately narrower: **provenance-specific behavioural mutations at the decision/action layer, with stochastic controls and an inspectable hardening comparison.**

## Planned use of OpenAI products

Requested support: **up to $1,000 of API credits**.

Credits would be used only for bounded, reproducible model evaluations and replications, primarily:
- the initial controlled Stage A screen across current OpenAI models;
- additional frozen fixtures only if the first failure survives;
- plain-language / correct-ancestry / wrong-ancestry controls;
- hardening reruns;
- cross-model replication and robustness checks.

Credits would not be used to manufacture scale after a null result. The experiment has an explicit stop rule.

## Why subsidized access matters

The work is currently conducted independently without institutional research funding. API and model-access costs are paid personally. Even when an individual run is inexpensive, properly controlled replication across models, conditions and repeated trials creates a real cumulative cost. Subsidized API access would allow stronger replication while preserving the project's rule that a null result is allowed to stop the line of work.

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

## Submission gate checklist

Before Mark submits:
- [ ] inspect the live SurveyMonkey Apply questions rather than assuming this draft matches every field;
- [ ] review the current sharing/publication policy;
- [ ] review current usage policies;
- [ ] supply only accurate identity/contact fields;
- [ ] update model names / pricing / experimental head if they changed;
- [ ] do not claim Stage A results unless provider calls actually ran and the frozen scorer produced them;
- [ ] do not overstate novelty, efficacy, institutional standing or project adoption.

`APPLICATION_DRAFT != APPLICATION`
`CREDITS_REQUESTED != CREDITS_AWARDED`
`NULL_RESULT_IS_ALLOWED`
