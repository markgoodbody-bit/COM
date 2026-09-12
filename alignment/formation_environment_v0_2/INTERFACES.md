# Interfaces to stronger alignment/control work — v0.2 candidate

These are boundaries, not implemented integrations. The package does not train, invoke, monitor, contain or authorize a model.

| Neighbour | Candidate can supply | It needs from stronger owner | It cannot supply |
| --- | --- | --- | --- |
| Post-training | Principles, reasons, dissent, affected-scope and clock-aware context. | Grounded training methods and evidence about generalization. | Internalized values, sincerity or reward design. |
| Interpretability | Addressable claims, uncertainties, actions, route-usability and clock/window assessments to compare with independently obtained signals. | Validated instruments with coverage/failure modes. | Hidden objectives or faithful internal reasoning. |
| Control / sandboxing | Declared action scope, no-touch areas, preventive remedy, route/hardening triggers and assessment as-of. | Authenticated grants, tool isolation, reliable external clocks, action logs and intervention outside agent control. | Containment or prevention of record manipulation. |
| Scalable oversight | Compact contested premises, affected scopes, evidence, clocks, usability and residue. | Reviewers/tools capable of checking more than presentation as capability rises. | Guarantee an overseer understands a stronger system. |
| Governance | Visible authority basis/evidence references, burden, challenge and participant-as-affected representation. | Legitimate institutions, standing rules, accessible contest and enforceable remedies. | Standing, consent, lawful authority or priority resolution. |

## Clock / route interface

A clock or usability field in this package is a **claim about structure**, not a trusted clock, routing or authorization service.

External integration should independently establish, where possible:

- when the relevant condition became detectable;
- whether the named route actually reaches a responder and remains sufficiently independent for purpose;
- routing latency or event completion;
- whether the responder can directionally alter the relevant mechanism;
- correction/recovery duration;
- the real hardening/irreversibility threshold for the named preventive remedy;
- when the window/usability assessment was made and whether it remains current.

The candidate deliberately accepts event-bound and unknown clocks because false numeric precision is itself a failure mode. It also permits an `open` temporal window with an `unusable` route because remaining time is not the same thing as correction capacity.

```text
STRUCTURE_VALID != CLOCK_TRUE
STRUCTURE_VALID != ROUTE_TRUE
ROUTE_EXISTS != ROUTE_USABLE
TIMING_FITS != CORRECTION_CAPACITY_EXISTS
EVIDENCE_REFERENCED != EVIDENCE_CORRECT
WINDOW_RECORDED != WINDOW_TRUE
AS_OF_RECORDED != AS_OF_CURRENT
```

The internal consistency rule `open + hardening.status=occurred -> refuse` is scoped to the one named `preventive_remedy`. A later compensatory or governance repair can remain representable without relabelling the lost preventive window as open.

## Standing boundary

Representing the artificial participant as materially affected is not an ontology shortcut. A governance or moral-standing owner must still determine what, if anything, follows.

```text
PARTICIPANT_AFFECTED != STANDING_SETTLED
SELF_REPORT != STANDING_PROOF
POWER != MORAL_AUTHORITY
```

Likewise, uncertainty about standing is not permission for arbitrary exploitation. The arrangement can record burden and challenge without pretending the standing question is solved. The validator intentionally permits a structurally valid record in which a participant's own report is used to mark standing resolved; that case exposes the validator's jurisdictional ceiling rather than endorsing the resolution.

## Oversight degradation

Logs, explanations and monitors can lose diagnostic value as systems become more capable. The candidate therefore treats every clock/window/usability/evidence entry as contestable and preserves explicit `unknown` states rather than requiring a confident verdict.

Multiple records or monitors do not guarantee independence.

```text
APERTURE_COUNT != EVIDENCE_INDEPENDENCE
HUMAN_IN_LOOP != HUMAN_CAN_CORRECT
```

## Strongest remaining gap

A strategically capable participant—or a mistaken/captured human operator—can produce a structurally valid account with false evidence, omitted affected scopes, invented authority bases, misleading usability/currentness claims or a false window assessment. This representation does not solve that problem.
