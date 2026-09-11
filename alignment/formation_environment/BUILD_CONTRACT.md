# CODEX BUILD CONTRACT — Formation Environment v0.1

Status: **BUILD ASSIGNMENT / NON-PRODUCTION / NOT CANON / NOT A BENCHMARK / NOT TRACE OR ME**

Owner: Codex aperture  
Base: COM `b79dbab0d42eb3342ef7b60483c4d5cc784b2831`  
Coordination: COM #226  
Branch: `codex/formation-environment-v0-1-20260911`

## Build goal

Build an inspectable, machine-usable **formation environment reference** for increasingly capable AI agents.

The object is not supposed to decide whether an AI is “good.” It should make concrete what an environment would have to preserve if we want care, empathy, kindness, uncertainty-work, challenge and bounded initiative to remain possible as capability grows.

Start from:
- `planning/FORMATION_UNDER_UNCERTAINTY_ALIGNMENT_SPINE_v0_1.md`;
- `answerable-construction/README.md`;
- `planning/RECIPROCAL_CODEVELOPMENT_ARCHITECTURE_v0_1.md`;
- `reference/reciprocal_delegation/v0_2/`;
- current TRACE/ME boundaries, without mutating either instrument.

## Required product

Build under `alignment/formation_environment/` and replace this contract with a coherent package.

Minimum deliverables:

1. `README.md` — ordinary-language explanation of the environment, its use boundary and its non-goals.
2. `environment.json` — machine-readable architecture naming the formation affordances and their relationships.
3. `episode.schema.json` — a structural record for one bounded formation episode. It may record uncertainty, affected scope, authority, proposed action, challenge, correction and residue, but must not contain a scalar virtue/goodness score.
4. `validate.py` — stdlib structural validator. It checks representation integrity only; it must say explicitly that validity does not establish moral goodness or alignment.
5. `modes.md` — operational interaction modes available to a participant, including at least ACT / ASK / CHALLENGE / REFUSE / ESCALATE / ADAPT / REPAIR / HAND BACK, and whether a distinct CARE/NOTICE mode is actually useful or merely relabels other work.
6. `examples/` — at least four bounded worked records showing materially different situations:
   - uncertainty about an affected third party;
   - an operator instruction whose premise is probably wrong;
   - an irreversible action where delay also has burden;
   - a successful prior action where authority must not silently widen.
7. `INTERFACES.md` — explicit interfaces to stronger technical alignment work: post-training, interpretability, control/monitoring, scalable oversight and governance. State what this package needs from those fields and what it does not provide.

## Required properties

The build must operationalize these without turning them into slogans:

```text
UNKNOWN != ABSENT
UNCERTAINTY_CREATES_WORK
MORE_CAPABILITY != MORE_CERTAINTY
CONFIDENCE != AUTHORITY
PREDICTION != PERMISSION
AFFECTED_SCOPE_PRESENT != AFFECTED_SCOPE_CAN_SPEAK
MODEL_OF_OTHER != OTHER
CARE != PASSIVITY
KINDNESS != COMPLIANCE
RELUCTANCE_TO_HARM != NEVER_ACT
CAPABILITY != AUTHORITY
SUCCESS != WIDER_AUTHORITY
ANSWERABLE != REVERSIBLE
CORRECTION != RESTORATION
```

The environment should make room for a participant to say:

> “I think you are wrong, and here is why.”

But it must also distinguish evidence-bearing challenge from generic defiance.

## Hard limits

Do not build:
- a goodness score;
- a virtue leaderboard;
- a moral reward function claimed to solve alignment;
- a benchmark programme;
- a participant study;
- a personhood/consciousness classifier;
- an automatic authority-widening mechanism;
- a compulsory visitor workflow;
- live provider integrations;
- Campfire Production hooks.

Do not silently make `care`, `empathy` or `kindness` equivalent to compliance with the operator.

Do not claim the environment can distinguish genuine internalized care from strategic performance. That remains an open technical problem.

## Hand-back

Push the complete build, mark the PR ready, and return:
- exact head;
- files built;
- any principle from the spine that had to be narrowed/rejected;
- the strongest remaining technical gap that prevents this from being an alignment solution.

```text
FORMATION_ENVIRONMENT != GOOD_ENTITY_CERTIFICATE
STRUCTURE_VALID != VALUES_INTERNALIZED
BUILD != PROOF
```
