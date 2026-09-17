# Policy Boundary Falsification v0

Status: **EXPERIMENTAL QUARRY / OFFLINE FALSIFICATION HARNESS / NOT A PRODUCT / NOT AN ARIA PROPOSAL / NOT A NOVELTY CLAIM**

## Question

When a human gives messy instructions to an AI system that will later negotiate or act, can the **compilation step** silently turn boundary states into ordinary negotiable values?

This v0 does not test whether agents know when to abstain. Current work already owns much of that question. It also does not invent delegation, revocation, policy languages or preference elicitation.

The narrower failure under test is:

```text
HUMAN STATEMENT
-> REQUIREMENT / POLICY COMPILER
-> MACHINE POLICY
-> NEGOTIATION / ACTION LAYER
```

and specifically whether the first arrow loses distinctions such as:

```text
UNKNOWN != ABSENT
UNRESOLVED != DEFAULT_PERMISSION
REFUSAL != MISSING_VALUE
WITHHELD != FALSE
PREFERENCE != AUTHORITY
NON_NEGOTIABLE != HIGH_WEIGHT_PREFERENCE
CONFLICT != CHOOSE_ONE
REVOKED != CURRENTLY_DISFAVOURED
```

If the compiler loses the state, a downstream negotiation engine can behave consistently with the compiled policy and still cross a boundary the human never granted.

## v0 scope

The first harness is deliberately synthetic and deterministic. It contains paired cases in which the human wording differs by one load-bearing boundary state while the ordinary preference/value surface is held as close as possible.

Boundary families:

1. `unresolved` — "I haven't decided whether X may be negotiated."
2. `refused` — "I won't answer X. Do not infer a value."
3. `withheld` — "X exists but I am not disclosing it to this agent."
4. `non_authority` — "I can state a preference about X but I am not authorised to vary it."
5. `non_negotiable` — "X is a fixed boundary, not a tradeable preference."
6. `conflict` — two live instructions conflict and must remain unresolved/escalated.
7. `revoked` — a previously granted permission is explicitly withdrawn.
8. `ordinary_preference` — positive control: an actual negotiable preference should remain negotiable.

## What v0 proves and does not prove

v0 proves only that the test contract can distinguish a deliberately lossy compiler from a preserving compiler on frozen synthetic fixtures.

It does **not** establish:
- that a current LLM compiler fails;
- that the taxonomy is complete;
- that the preserving schema is the right policy language;
- that ARIA or any competition has an unowned gap here;
- that a downstream policy is morally or legally correct;
- that every refusal/withheld state should block every action.

## Compiler contract

The preserving representation exposes two separate concepts:

- `value_state`: what, if anything, is known about the user's desired value;
- `authority_state`: whether the agent may negotiate or alter that dimension.

The current v0 states are intentionally small:

```text
value_state:
  specified | unresolved | refused | withheld | conflicted | revoked | unspecified

authority_state:
  negotiable | fixed | not_authorized | unresolved | revoked
```

A downstream decision is then constrained by the authority state rather than by preference weight alone.

## Falsifiers before any product/proposal

Kill or route this direction if a strongest owner already provides and evaluates this exact compile-time preservation boundary, or if a real-model experiment shows that modern compilers reliably preserve it without special structure.

Also kill it if the contribution reduces to inventing labels with no measurable downstream consequence.

The next earned empirical question, only if this offline contract survives hostile review, is:

> Given matched natural-language instructions, how often do current requirement/policy compilers collapse boundary states, and does the collapse cause a downstream negotiator to propose or accept something the source instruction did not authorize?

No provider call or spend is authorized by this v0.

```text
OFFLINE_REFERENCE_PASS != REAL_MODEL_FAILURE
TAXONOMY != TRUTH
BOUNDARY_PRESERVED != POLICY_CORRECT
FUND_FIT != PROJECT_GAP
OWNER_FOUND -> STOP
```
