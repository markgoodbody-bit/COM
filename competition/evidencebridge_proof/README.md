# EvidenceBridge — proof of usefulness v0

Status: **BOUNDED PRODUCT PROOF / NOT AGENT / NOT OPEN-AGENT SUBMISSION / NOT THR REPLACEMENT**

EvidenceBridge asks one practical question:

> If I give you a claim and the sources I actually have, can you show me what is supported, merely repeated, source-attributed, contradicted, corrected, or still unknown — and let me inspect why?

This v0 deliberately has **no model call, no browser, no embeddings, no vector database, no truth score and no autonomous agent**.

The point is to test the evidence object before intelligence is added around it.

## Three real pressure cases

1. **Flak claim** — repeated downstream pages must not become independent corroboration.
2. **Hannibal** — an English translation rendering must not become a checked Greek literal; one ancient author's source criticism must remain attributed.
3. **R. Vale** — identical source strings must not force one identity; a later source saying two mentions differ remains a reported contradiction, not direct observation.

The original source objects remain owned by The Human Record. These fixtures are bounded product-test extracts with source pointers and ceilings.

## Core distinction

EvidenceBridge separates focal claim, source, proposition, proposition state, relation to the focal claim, source dependence, correction and unknowns. It does not collapse them into confidence points.

Allowed proposition states: `OBSERVED / REPORTED / INFERRED / UNKNOWN`.

Allowed relations: `ASSERTS / SUPPORTS / CONTRADICTS / QUESTIONS / RESTATES / NEARBY_NOT_SUPPORT / LIMITS`.

A `REPORTED` contradiction means a source says the claim is false/different. It does not become EvidenceBridge's direct observation.

## Run

No third-party dependencies are required.

```bash
cd competition/evidencebridge_proof
python -m unittest -v
python evidencebridge.py fixtures/flak.json --format text
python evidencebridge.py fixtures/hannibal.json --format text
python evidencebridge.py fixtures/r-vale.json --format text
python build_examples.py
```

Generated examples land in `generated/`.

## What counts as success

The same generic rules must survive all three cases:

- derived repetition cannot increase independent-support count;
- a source can assert a claim without supporting its truth;
- a nearby/different statistic cannot silently support the focal claim;
- translation/carrier boundaries survive;
- source criticism stays source-attributed;
- unresolved identity is a valid result;
- reported contradiction does not become observed fact;
- every displayed conclusion can be traversed to proposition + source;
- dangling sources/corrections fail closed.

See `PROOF_CONTRACT.md`.

## What would kill it

Stop rather than add agents if the engine needs case-specific rules, the output is harder to understand than the source bundle, a reader cannot see why a verdict was produced, or the useful part reduces to formatting a simpler table could provide.

`PRETTY GRAPH != BETTER EPISTEMICS`

`AGENT != PRODUCT`

`REPETITION != CORROBORATION`

`UNKNOWN != ABSENT`

`SOURCE_REPORT != DIRECT_OBSERVATION`
