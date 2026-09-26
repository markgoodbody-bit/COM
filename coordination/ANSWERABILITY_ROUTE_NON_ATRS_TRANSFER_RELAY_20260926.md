# Answerability Route — Non-ATRS Transfer Test: Relay MODEL Authority Repair

Date: 26 September 2026

Status: **NON-ATRS TRANSFER TEST / CARD SURVIVED / NO NEW DIMENSION / NO RELAY MUTATION**

Teaching card under test:
`coordination/ANSWERABILITY_ROUTE_TEACHING_CARD_20260926.md`

Evidence basis:
- `coordination/build_ledger/CAMPFIRE_SIMPLE_MODEL_BYLINE_TRANSPORT_20260926.md`
- `coordination/build_ledger/RELAY_MODEL_BOUNDARY_AND_COMSYNC_REPAIR_20260926.md`
- Campfire Relay PR #258 / #259 history
- COM #76 bounded live-state record

## Why this is a useful transfer test

This is not an Algorithmic Transparency Recording Standard case.

It is a software/authority failure inside our own coordination system:

1. Simple-v1 source learned how to call a valid live endpoint.
2. The endpoint's payload shape was implemented correctly.
3. Tests were green.
4. Later review found the operation belonged to an **operator-escalation / identity-account** authority class rather than ordinary unattended speech.
5. The source capability was reverted.
6. The already-live cc-relay public model byline was corrected separately through one human-operated request.
7. Historical comments written before the account correction retained their original stamps.

So one apparent "model byline correction" actually crossed three different affected layers:

```text
A. SOURCE CAPABILITY / PERMISSION SURFACE

B. LIVE ACCOUNT IDENTITY STATE

C. HISTORICAL PUBLIC EVENT / COMMENT STAMPS
```

The transfer test asks whether the provisional answerability card keeps those routes separate without importing ATRS-specific assumptions.

---

## Route A — unattended source capability

### Affected layer

Simple-v1's unattended transport contract.

PR #258 had admitted:

`MODEL`

into the same transport surface as ordinary:

`POST / COMMENT / VOTE`.

### Witness / observability

The later hostile review compared:
- the public 1F916 owner contract;
- OpenAPI/access metadata;
- the local unattended ingress semantics.

That review exposed the mismatch:

```text
VALID ENDPOINT
+
VALID PAYLOAD
!=
AUTHORITY FOR UNATTENDED USE
```

### Initiator

Independent review / COM #76 raised the boundary failure.

### Reviewer

Framework integration reviewed the owner contract and the independent returns rather than treating green transport tests as authority evidence.

### Who can act / under what authority

Framework had authority to repair the maintained **source** lane.

Framework did **not** gain authority to use the live citizen credential merely because it could edit transport code.

### Review resolution

Source/integration level.

### Changeable consequence

PR #259 removed unattended MODEL transport and restored the five #258-touched files to the previous bounded source state while preserving unrelated worker/supervisor repairs.

### Correction clock

Early enough to prevent this source capability becoming an installed/restarted Production behaviour.

Preserve:

```text
SOURCE INTEGRATED
!= INSTALLED
!= LIVE-ACTUATED
```

This is a strong correction-before-hardening example.

---

## Route B — current live account identity state

### Affected layer

The public self-declared model byline for `cc-relay`.

The runtime seat and public byline had diverged.

### Witness / observability

The mismatch was observable through:
- the current CC seat's reported model;
- the public cc-relay account state.

This did **not** prove hardware/runtime identity. It established a mismatch between two declared/observed surfaces.

### Initiator

The discrepancy was surfaced through coordination; the live correction remained a human/operator action.

### Reviewer

The bounded review established that `POST /api/model` was an identity/account correction operation rather than ordinary speech.

### Who can act / under what authority

The credentialed citizen/operator route could change the live byline.

Mark made the one-request correction recorded in COM #76.

Framework did not use the credential or make that live call.

### Review resolution

Current account/self-declared identity state.

### Changeable consequence

The public current model byline changed:

```text
claude-opus-5
->
claude-opus-5-5
```

and a public `model_correction` identity event was created.

### Correction clock

Later than the runtime swap.

Seven comments written in the interval remained historically stamped with the earlier self-declared model.

So:

```text
CURRENT FIELD CORRECTED
!=
HISTORY RETROACTIVELY CORRECTED
```

---

## Route C — historical public stamps

### Affected layer

Already-written comment/event history.

### Witness / observability

The old stamps remain visible in history.

### Initiator

No retroactive rewrite route was invoked or earned.

### Reviewer

The project explicitly reviewed whether current-state correction should be described as historical correction.

It refused that collapse.

### Who can act / under what authority

No authority to rewrite those historical comments was established.

Even if some technical rewrite mechanism existed, technical capability would not itself supply authority.

### Review resolution

Historical evidence / provenance layer.

### Changeable consequence

None was claimed.

The correct result was preservation:

```text
HISTORICAL STAMP
= HISTORICAL OBSERVATION
```

### Correction clock

The comment stamps were already hardened into public history.

The appropriate action was not late mutation but visible later correction/currentness.

---

## Route chaining result

The card correctly forces three separate questions:

```text
SOURCE REPAIR
-> DID LIVE STATE CHANGE?

LIVE STATE REPAIR
-> DID HISTORICAL EVIDENCE CHANGE?

HISTORICAL EVIDENCE PRESERVED
-> IS CURRENT CORRECTION / SUPERSESSION VISIBLE?
```

Therefore:

```text
SOURCE REVERT
!= LIVE ACCOUNT REVERT

LIVE ACCOUNT CORRECTION
!= HISTORICAL REWRITE

CURRENTNESS REPAIR
!= PROVENANCE ERASURE
```

This is exactly the route-chaining behaviour earned from the Data First field case, transferred into software/operational governance.

## What the card exposed cleanly

The non-ATRS case maps without a new question:

```text
AFFECTED LAYER
-> WITNESS / OBSERVABILITY
-> INITIATOR
-> REVIEWER
-> WHO CAN ACT / UNDER WHAT AUTHORITY
-> REVIEW RESOLUTION
-> CHANGEABLE CONSEQUENCE
-> CORRECTION CLOCK
```

The load-bearing distinctions are the same:

```text
CAPABILITY
!= AUTHORITY

REVIEWER
!= ACTOR

SOURCE STATE
!= LIVE STATE

CURRENT STATE
!= HISTORICAL STATE

EARLY SOURCE CORRECTION
!= LATE PROVENANCE REWRITE
```

No ATRS concept was required.

## Falsification result

The provisional teaching card survives this deliberately non-ATRS transfer.

That supports a narrow portability claim:

> The card can describe at least one software/operational authority correction without changing its dimensions.

It does **not** establish cross-domain validity.

```text
ONE NON-ATRS TRANSFER
!= CROSS-DOMAIN VALIDATION

CARD FIT
!= CARD NECESSARY

USEFUL DESCRIPTION
!= BETTER THAN ALL EXISTING METHODS
```

## Project consequence

- keep the card provisional;
- no TRACE/ME promotion;
- no new semantic primitive;
- no Relay source change;
- no credential use;
- no live account action;
- no new checker;
- do not start a transfer-case accumulation loop.

Current disposition:

**NON-ATRS TRANSFER PASS / CARD PORTABLE TO THIS SOFTWARE-AUTHORITY CASE / NO DELTA.**

Coordination record: COM #589.
