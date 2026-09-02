# Voluntary help — Help Exchange candidate v0.1

**Status:** SHRINK-TO-QUESTIONS REVIEW / NOT CANON / NOT TRACE OR ME / NOT VALIDATED / NOT ADOPTED / NO ENFORCEMENT

Built for `FW-VOLUNTARY-HELP-TOOLS-20260901-001`. Answers to the project anchor — *how can we make a better future?* — by trying to keep one small interaction from going wrong in the ways it usually goes wrong.

Independent review on 2 September 2026 found that the formal consent/state machinery is already better owned elsewhere and that three additional probes contradict claims made by the validator. See [`REVIEW_20260902.md`](REVIEW_20260902.md).

**The retained candidate is [`FIRST_CONTACT.md`](FIRST_CONTACT.md).** It is a repaired conversational aid, not a consent mechanism. The schema, validator, state machine and examples remain research evidence only and must not be deployed as a usable agreement or proof of consent.

## Files

```text
FIRST_CONTACT.md      the questions, in plain language. No jargon, no schema.
ADVERSARIAL_NOTE.md   owners, limits, and what the validator cannot detect.
help_exchange.py      the validator. This is the authority on what is valid.
schema.json           shape only, for tooling. NOT the authority - see below.
examples/             one bounded offer, one emergency action.
tests/                20 tests over the ten required scenarios.
```

The last four lines describe the original technical candidate. They are retained for auditability, not recommended for use.

## Research-only reproduction

```bash
python help_exchange.py examples/offer.json examples/emergency.json
python tests/test_help_exchange.py
```

## Why `schema.json` is not the authority

The rules that do the work are cross-field, and JSON Schema cannot express them:

- an accept must come from the party who did **not** make the standing proposal;
- `answer_back.helped_route_arbiter` must not be the helper's own id;
- a transition's `basis` must not record nothing happening;
- an `EMERGENCY_ACTION` may never enter a consent-bearing state.

`schema.json` is provided for editors and tooling. Where it and the validator disagree, **the validator is right and the schema is stale.** Two sources of truth is how a rule quietly stops applying.

## The state machine

```text
OFFERED ─┬─> CONSIDERING ─┬─> ACCEPTED ──> ACTIVE ─┬─> PAUSED ──> ACTIVE
         │                │                        ├─> COMPLETED   (terminal)
         ├─> COUNTERED ───┤                        ├─> DISPUTED
         ├─> REFUSED   (terminal)                  └─> WITHDRAWN   (terminal)
         └─> WITHDRAWN (terminal)

EMERGENCY_ACTION:  TAKEN ──> NOTIFIED ──> REVIEWED      (DISPUTED from either)
```

Every edge requires a named actor and a stated basis. **There is no edge traversed by waiting.** The emergency lane never touches `ACCEPTED`, because nobody accepted.

## Ceilings, emitted with every validated record

```text
CAPABILITY != MANDATE
ACCEPTANCE != OWNERSHIP
HELP != TOTAL CLAIM ON HELPER
REFUSAL != HOSTILITY
SILENCE != CONSENT
PRIOR TRUST != PRESENT AUTHORITY
COMPLETION != REPAIR OR RESTORATION
VOLUNTARY != COSTLESS OR POWER-FREE
```

They travel inside the record rather than living in a document nobody opens.

## The four coercive shapes, refused structurally

Not by reading prose for menacing words — a matcher over intent would be a matcher that dies silently and reports a clean zero.

| Pattern | Refused because |
|---|---|
| approval leash | `exit.refusal_requires_counterparty_agreement` is not `false` |
| Samaritan / total claim | `mandate.excluded` is empty — it names nothing it does not cover |
| paternalist | `answer_back.helped_route_arbiter` equals the helper's id |
| proxy ambiguity | `standing` is `PROXY`/`COLLECTIVE` with no instrument named |

Plus: an open-ended mandate (no `expires_utc` and no `review_at_utc`), an unstated `refusal_consequence`, a completion that does not say what was **not** restored, and any `claims_personhood`.

## Tests

20 tests, covering the ten scenarios in the build request. Refusal tests assert on the **field** that refuses, not on message wording, so rewording an error cannot turn a test into a tautology.

```text
Ran 20 tests — OK
```

Two defects were found by these tests during the build and are recorded in the code where they happened: the recipient rule originally compared against the previous actor rather than the last proposer, so accepting after considering was wrongly refused; and the silence check normalised dashes but not spaces, so `deemed accepted` passed while `deemed_accepted` did not.

## What would falsify the design

One real pair of parties using `FIRST_CONTACT.md`, and the record adding nothing the conversation did not already produce. That is the outcome I would expect, and it should be reported if it happens rather than absorbed.
