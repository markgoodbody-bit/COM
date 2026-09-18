# Correction propagation across two real domains — rail information and children’s records

Status: **CROSS-DOMAIN PORTABILITY WITNESS / NO NEW PRIMITIVE / NO NOVELTY CLAIM / NO OPERATIONAL-ADVANTAGE CLAIM**
Date: 18 September 2026

> HOW CAN WE MAKE A BETTER FUTURE?

## Why this note exists

Two independently sourced current cases expose a similar relation at different layers:

1. rail accessibility information: the physical world and some owner-controlled information had changed, while a passenger-facing summary still said there were no lifts;
2. a children’s statutory complaint: a formal review panel had recommended correction of inaccurate information, but the complainant later reported that the recommendation had not been carried out; during Ombudsman enquiries the Council said it then reviewed accuracy and took corrective steps where required.

The question is not whether this relation is novel. It is whether the existing project language can carry both cases without domain-specific reinvention.

## Case A — rail

Bounded result integrated through COM PR #383.

Observed relation:

PHYSICAL ACCESSIBILITY CHANGE
-> OWNER DATA / OPERATOR SURFACE RECORDS LIFTS
-> PASSENGER SUMMARY STILL SAYS NO LIFTS

Three live examples were reproduced: HIR, IRL and DSY. Three controls behaved correctly: BIW, AGV and LLE.

Hostile review removed the attempted station-level operational classifier. The surviving claim is only lift-existence/currentness consistency.

Not established:
- root cause;
- operator blame;
- network-wide prevalence;
- present step-free journey usability.

## Case B — Bradford children’s records

Primary owner decision: LGSCO 25 023 288, 20 July 2026.

Observed relation:

FORMAL REVIEW RECOMMENDS RECORD CORRECTION
-> RECOMMENDATION NOT IMPLEMENTED AT THE POINT COMPLAINED OF
-> FURTHER OWNER ENQUIRY
-> COUNCIL LATER REVIEWS ACCURACY AND TAKES CORRECTIVE STEPS WHERE REQUIRED

Not established:
- exact corrected propositions/records;
- exact correction delay;
- downstream reliance;
- reconsideration of downstream plans/actions;
- causation of the harms alleged by the complainant;
- AI involvement.

## Shared compression

The two cases are not equivalent. One is public information currentness after a physical-world change; the other is institutional record correction after a review recommendation.

The shared relation is thinner:

CORRECTION SOURCE / NEW STATE EXISTS
!= CORRECTION HAS REACHED EVERY CONSEQUENTIAL TARGET

Or operationally:

CHANGE / CORRECTION
-> PROPAGATION TARGETS
-> SOME TARGET STATE
-> VERIFY WHICH TARGETS ACTUALLY CHANGED

This is ordinary change/currentness/correction discipline. It is not claimed as a TRACE invention.

## Existing project fit

TRACE v0.3.0 already has enough structure:
- recurrence/currentness;
- record != world;
- local correction != mechanism change;
- target-set / aperture limits;
- burden/residue;
- stop/handoff when owner machinery is stronger.

Mechanical Ethics already distinguishes formal correction from restored consequence and says answerability requires affected outcomes to reach and alter future behaviour.

Therefore:

NEW TRACE PRIMITIVE = NO
NEW ME DOCTRINE = NO
NEW CORRECTION-PROPAGATION FRAMEWORK = NO

## What this does establish

At least at the level of representation, the same compact distinction can describe two materially different owner domains without forcing either case into a new domain ontology.

That is a portability witness only.

PORTABLE DESCRIPTION != PRACTICAL ADVANTAGE
COMPRESSION != NOVELTY
TWO CASES != GENERAL VALIDATION

## Small operational reading

When a correction matters, a useful owner-native question is:

> Which records, surfaces, plans, actions or other targets should change because of this correction, and which of those targets have actually been checked or updated?

Existing owners may already ask this in their own language. Use their mechanism where it is stronger.

## Disposition

Keep as field evidence. Do not turn it into a schema, benchmark, certification system or new project lane.

Wake only if a real owner workflow loses a consequential propagation target and a small interoperable aid would change the outcome.