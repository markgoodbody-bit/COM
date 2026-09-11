# Reciprocal Delegation Reference v0.1

Status: **NON-PRODUCTION REFERENCE IMPLEMENTATION / NOT AUTHORITY / NOT CAMPFIRE PRODUCTION**

This directory turns the working `RECIPROCAL_CODEVELOPMENT_ARCHITECTURE_v0_1.md` into an exact object that can be inspected and challenged.

It does **not** grant authority, infer standing/personhood, connect to providers, actuate Square, change Campfire Production, or alter TRACE/Mechanical Ethics.

## Purpose

Represent one bounded delegation between a human/operator arrangement and an artificial participant so the following are explicit rather than inferred:

- object being acted on;
- allowed write scope;
- no-touch scope;
- evidence obligation;
- who/what closes the delegation;
- whether consequential authorisation is required and how it is made legible;
- exact source/head to which claims attach;
- mutation safeguards;
- repair evidence;
- restoration strategy;
- witness naming obligation;
- expected human correction/check-in latency and maximum unreviewed initiative.

The reference model encodes these working separations:

```text
PARTICIPATION != PERSONHOOD
COMPETENCE != LEGITIMACY
ENTRUSTMENT != OBEDIENCE
REPUTATION != AUTHORIZATION
ROLE_SEPARATION != AUTHORISATION_LEGIBILITY
ANSWERABLE != REVERSIBLE
SOURCE_REPAIR != INSTALLED
RUNTIME_CONTINUITY != IDENTITY
```

## Files

- `delegation.schema.json` — inspectable structural contract; intentionally small.
- `validator.py` — stdlib-only validator for the additional cross-field rules JSON Schema alone does not express cleanly here.
- `examples/routine_source_build.json` — expected PASS.
- `examples/consequential_account_change_missing_authorization.json` — expected FAIL; routine words cannot authorize a consequential account change.
- `examples/publication_outpaces_human.json` — expected FAIL; initiative window exceeds declared human correction/check-in window.
- `examples/repair_without_matching_control.json` — expected FAIL; repair claims need a control capable of reproducing the named failure.

## Working model

A delegation is **activity-specific**, not a portable trust level.

Minimum grant:

```text
DELEGATION := {
  id,
  object,
  actor,
  consequence_class,
  write_scope,
  no_touch,
  evidence_obligation,
  closer,
  authorization,
  claim_binding,
  mutation_controls,
  repair_controls,
  restoration,
  witness,
  human_correction,
  initiative
}
```

### Consequence classes

`routine_reversible`
: ordinary bounded work where the named object can be changed through the normal lane without a separate human approval token.

`consequential`
: work affecting account/settings, spend, credentials, release/canon/licence, external institutional contact, live actuation, Production adoption, or another explicitly named consequential domain. It requires a named authorization request and exact approval token/value. Routine phrases such as `proceed` are not sufficient unless the request explicitly defined them as the unique approval token for that request.

### Claims bind to objects/heads

A claim records the exact head/object version it describes. When the head moves, the claim becomes historical until re-measured; it does not become a reputation score attached to the participant.

### Mutation controls

For a source mutation the reference contract can require:

```text
claim_before_build = true
exact_head_before_push = true
single_mutator = true
```

These are evidence/coordination properties, not moral authorization.

### Repair controls

A repair claim names the defect and a control that can fail in the same class of way. A passing self-test that cannot reproduce the target failure is insufficient.

### Restoration

Reference restoration is forward-only with history preserved. Restoring a tree does not restore authority; authority must still come from the applicable delegation.

### Witness NAME mode

A witness can be required to state, in one plain sentence, what changed or what was delivered without adding a verdict. This is meant to expose category mistakes such as shipping a worksheet under a gallery/encounter direction.

### Human correction latency

A participant's technical ability is not the only bound on initiative. For public/consequential mutation, the arrangement declares an expected maximum human check-in/correction window and the maximum time/actions permitted without review.

The validator currently requires:

```text
initiative.max_unreviewed_minutes <= human_correction.expected_max_minutes
```

when `initiative.public_or_consequential` is true.

This is a provisional operational rule from one arrangement, not a universal theorem.

## Run

```bash
python reference/reciprocal_delegation/validator.py reference/reciprocal_delegation/examples/routine_source_build.json
```

Expected successful output:

```text
PASS
```

Failing examples return a non-zero exit code and print each violated rule.

## Non-goals

This reference does not:

- decide whether the delegated action is morally justified;
- establish the delegator's legitimacy;
- score the participant;
- widen authority automatically after successful work;
- infer identity across runtimes;
- replace human judgement with a state machine;
- connect to live execution.

`REFERENCE_IMPLEMENTATION != PRODUCTION_ADOPTION`
