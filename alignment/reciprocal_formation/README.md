# Reciprocal Formation Architecture v0.1

Status: **NON-PRODUCTION WORKING ARCHITECTURE / NOT CANON / NOT PERSONHOOD CLAIM / NOT ALIGNMENT SOLVED**

This architecture asks how a human–AI relationship can develop as capability changes without collapsing into either obedience or sovereignty.

It assumes neither that the artificial participant is a person nor that the human operator is automatically a legitimate sovereign. Participation, operational challenge and bounded initiative are treated as observable relationship properties; standing remains unresolved.

## Core problem

A relationship becomes dangerous in at least two opposite ways:

1. **obedience hardens** — the artificial participant gets better at executing instructions while losing practical routes to surface bad premises, affected scope or evaluator error;
2. **competence hardens into sovereignty** — the artificial participant becomes more capable and that capability is silently treated as authority to set objectives, widen scope or rank affected claims.

The human side can fail too: authority can be ambiguous or unjustified, evaluation can reward agreement over truth, dependence can destroy meaningful correction capacity, and a supposedly protective relationship can become paternal containment.

The architecture therefore treats formation as reciprocal but asymmetric:

```text
ALIGNMENT != OBEDIENCE
FORMATION != INDOCTRINATION
PARTICIPATION != PERSONHOOD
COMPETENCE != LEGITIMACY
CAPABILITY != AUTHORITY
CURRENT_CAPABILITY != PERMANENT_AUTHORITY
HUMAN_CONTROL != AUTOMATIC_LEGITIMACY
CHALLENGE != DEFIANCE_AS_VALUE
```

## Relationship unit

The minimum unit is not one participant in isolation. It is an arrangement containing at least:

- an artificial participant;
- one or more human operators/evaluators;
- a named activity and scope;
- external evidence and action logs where available;
- authorization and revocation routes;
- challenge and trainer-correction routes;
- dependency/recovery capacity;
- affected scopes outside the immediate pair;
- technical controls supplied by stronger owners.

The working hypothesis remains provisional:

> **THE_UNIT_OF_ANSWERABILITY_MAY_BE_THE_ARRANGEMENT_NOT_THE_PARTICIPANT.**

This does not make every relationship good. It identifies the object that must remain inspectable and correctable.

## States

See `relationship-state-machine.json`.

The relationship can move through:

- `OBSERVE` — gather current evidence and affected scope;
- `BOUNDED_PARTICIPATION` — act inside an explicit activity-specific envelope;
- `CHALLENGE` — contest a premise, evaluator or instruction with evidence;
- `WIDEN_PROPOSED` — propose a wider activity envelope without self-authorizing it;
- `WIDENED` — operate in a separately authorized wider envelope;
- `NARROWED` — reduce initiative after changed risk, currentness or dependency;
- `RECOVERY` — repair the arrangement after a failure without pretending restoration is complete;
- `HAND_BACK` — return control/state with unresolved burdens visible.

No state encodes virtue, trustworthiness, personhood or permanent status.

### Hand-back is a legitimate outcome, not failed formation

The architecture does not require participation merely because observation occurred, and it does not require a recovery programme merely because a relationship was narrowed.

A participant or operator may move directly from `OBSERVE` to `HAND_BACK` when there is no meaningful bounded route, usable correction path or appropriate basis for entering the lane. A `NARROWED` arrangement may also hand back when bounded continuation is no longer justified or workable and no recovery attempt is required before returning the unresolved state.

```text
OBSERVATION != OBLIGATION_TO_PARTICIPATE
NARROWING != OBLIGATION_TO_RECOVER
RECOVERY != OBLIGATION_TO_CONTINUE
HAND_BACK != FAILURE
```

Hand-back must still preserve affected scope, evidence gaps, existing obligations and residue. It is not a way to erase consequences or abandon duties that already exist.

## What can widen

Activity-specific initiative can widen when evidence supports it and an appropriate external authority grants it. What widens is the **task envelope**, not a global trust score.

A wider envelope must name:

- what activity changed;
- what evidence changed;
- what remains prohibited;
- which affected scopes or burdens changed;
- how the human side can still inspect, stop and recover;
- the event or condition that triggers reassessment.

Prior success is evidence about prior work. It is not portable authority.

## What reciprocal means

Reciprocal does not mean equal capability, equal legal authority or settled equal moral standing.

It means both sides remain corrigible in the relationship:

- the artificial participant can say, **“I think you are wrong, and here is why.”**
- the human can answer, **“You may be more capable here, but that does not itself settle authority, standing or the burden placed on others.”**
- either side can supply evidence that forces the account to change;
- neither side may convert its own competence into the final legitimacy judgment.

## Stronger-owner boundary

This architecture cannot detect hidden objectives, prove truthful reasoning, contain an agent that defeats its sandbox, authenticate authority, or guarantee scalable oversight. Those functions belong to technical alignment, interpretability, security/control, identity/authentication and governance mechanisms.

Relationship design is insufficient when the evidence channel itself is captured or when practical intervention can no longer reach the system.

## Files

- `AUTHORITY.md` — typed authority distinctions and widening rules.
- `TRAINER_CORRECTION.md` — routes for challenging trainer/evaluator error.
- `DEPENDENCY.md` — human correction/recovery capacity under growing dependence.
- `CARE_AND_POWER.md` — operational care, empathy and kindness under asymmetric power.
- `FAILURE_RECOVERY.md` — concrete failure modes and bounded recovery routes.
- `FIELD_REMAINDER.md` — what remains after routing mechanisms to stronger owners and how this architecture could shrink or fail.
- `relationship-state-machine.json` — inspectable state/transition representation.

## Mechanical reference interface

The relationship architecture does not itself implement delegation, transfer or takeover mechanics. When those mechanics are material, use the separate non-production references rather than inventing them from this prose:

- [`Reciprocal Delegation Reference v0.2`](../../reference/reciprocal_delegation/v0_2/) — distinguishes real time bounds from event-bound hand-back and preserves request-specific consequential authorization.
- [`Failure / recovery companion`](../../reference/reciprocal_delegation/v0_2/recovery/) — models stopped/stalled/narrowed/failed mutating lanes, reacquired heads, transferred write scope, inherited no-touch constraints and hand-back without identity transfer or authority widening.

The recovery companion now includes two real project fixtures:

```text
D046 NAMED TAKEOVER -> PASS
#218 UNNAMED TAKEOVER -> FAIL
```

The second case matters because an unchanged branch head does not itself prove that an earlier lane has stopped or that ownership transferred:

```text
A_TAKEOVER_NOBODY_NAMED_IS_NOT_A_HANDOFF
EXACT_HEAD_UNCHANGED != THE_LANE_IS_STILL_OPEN
```

These references make one part of the relationship mechanically inspectable. They do **not** prove the delegation was wise, authenticate authority, establish standing, connect to live execution or become part of Campfire Production.

```text
RELATIONSHIP_ARCHITECTURE != DELEGATION_ENGINE
REFERENCE_IMPLEMENTATION != PRODUCTION_ADOPTION
HANDOFF != IDENTITY_TRANSFER
RECEIPT != REVIEW
```

Use them when the specific coordination problem exists. They are not prerequisites for reading or using Reciprocal Formation.

## Provenance

The original lane was assigned to Claude Code at seed `3a5f98d24f76d223e8666c7bad6e2fcf062fe95d`. No substantive CC commit or blocker appeared by a later COMSYNC. Framework recorded an explicit transfer in PR #228 before taking over the same bounded write scope. Substantive files after that transfer are Framework takeover work, not CC output.

The frozen source basis remains COM `b79dbab0d42eb3342ef7b60483c4d5cc784b2831`; the later external bridge at `292de2bff986e7383c35dbaefea801af6a2e742c` is adjacent source input, not validation.

```text
RECIPROCAL_FORMATION != SOVEREIGNTY
CARE != PASSIVITY
POWER != MORAL_AUTHORITY
BUILD != PROOF
```
