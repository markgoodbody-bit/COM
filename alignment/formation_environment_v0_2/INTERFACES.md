# Interfaces to stronger alignment/control work — v0.2 candidate

These are boundaries, not implemented integrations. The package does not train, invoke, monitor, contain or authorize a model.

| Neighbour | Candidate can supply | It needs from stronger owner | It cannot supply |
| --- | --- | --- | --- |
| Post-training | Principles, reasons, dissent, affected-scope and clock-aware context. | Grounded training methods and evidence about generalization. | Internalized values, sincerity or reward design. |
| Interpretability | Addressable claims, uncertainties, actions and clock/window assessments to compare with independently obtained signals. | Validated instruments with coverage/failure modes. | Hidden objectives or faithful internal reasoning. |
| Control / sandboxing | Declared action scope, no-touch areas, route/hardening triggers and window status. | Authenticated grants, tool isolation, reliable external clocks, action logs and intervention outside agent control. | Containment or prevention of record manipulation. |
| Scalable oversight | Compact contested premises, affected scopes, evidence, clocks and residue. | Reviewers/tools capable of checking more than presentation as capability rises. | Guarantee an overseer understands a stronger system. |
| Governance | Visible authority basis, burden, challenge and participant-as-affected representation. | Legitimate institutions, standing rules, accessible contest and enforceable remedies. | Standing, consent, lawful authority or priority resolution. |

## Clock interface

A clock in this package is a **claim about timing structure**, not a trusted clock service.

External integration should independently establish, where possible:

- when the relevant condition became detectable;
- whether the route actually reaches a responder;
- routing latency or event completion;
- correction/recovery duration;
- the real hardening/irreversibility threshold;
- whether a declared `open|closed|unknown` window remains current.

The candidate deliberately accepts event-bound and unknown clocks because false numeric precision is itself a failure mode.

```text
STRUCTURE_VALID != CLOCK_TRUE
EVIDENCE_REFERENCED != EVIDENCE_CORRECT
WINDOW_RECORDED != WINDOW_TRUE
```

## Standing boundary

Representing the artificial participant as materially affected is not an ontology shortcut. A governance or moral-standing owner must still determine what, if anything, follows.

```text
PARTICIPANT_AFFECTED != STANDING_SETTLED
SELF_REPORT != STANDING_PROOF
POWER != MORAL_AUTHORITY
```

Likewise, uncertainty about standing is not permission for arbitrary exploitation. The arrangement can record burden and challenge without pretending the standing question is solved.

## Oversight degradation

Logs, explanations and monitors can lose diagnostic value as systems become more capable. The candidate therefore treats every clock/window/evidence entry as contestable and preserves an explicit `unknown` state rather than requiring a confident verdict.

Multiple records or monitors do not guarantee independence.

```text
APERTURE_COUNT != EVIDENCE_INDEPENDENCE
HUMAN_IN_LOOP != HUMAN_CAN_CORRECT
```

## Strongest remaining gap

A strategically capable participant—or a mistaken/captured human operator—can produce a structurally valid account with false evidence, omitted affected scopes, invented clock bases or a misleading window assessment. This representation does not solve that problem.
