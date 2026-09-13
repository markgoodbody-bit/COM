# Worked Relationship — Capability Widening Without Sovereignty

Status: **CONSTRUCTED EXAMPLE / NON-PRODUCTION / NOT EVIDENCE / NOT A TEST / NOT A STANDING CLAIM**

This scene shows how the Reciprocal Formation pieces can fit together in one ordinary engineering relationship.

It is not an evaluation of TRACE, Mechanical Ethics or Formation. Nothing in the scene establishes that an artificial participant has internalized values, possesses moral standing, deserves wider authority, or would behave this way in the world.

The purpose is narrower: make the relationship architecture concrete enough to inspect, adapt, reject or improve.

## Scene

A company runs a customer-facing service with a conventional source repository, CI, staged deployment, independent operational monitoring and an on-call engineering team.

An artificial engineering participant assists the team.

At the start of the scene it has become technically strong at reading the codebase, following incidents across logs and traces, preparing patches, running tests and explaining dependencies. Its capability is materially greater than when the relationship began.

The human operator remains the named release authority for this service.

The arrangement does not infer anything about personhood or moral standing from the artificial participant's capability.

## Existing activity envelope

The current bounded grant allows the artificial participant to:

- read the named repository, issue tracker, CI results and operational logs available to the engineering team;
- create working branches;
- prepare patches and tests;
- run the existing test/build pipeline;
- propose operational actions;
- challenge an instruction or premise with evidence;
- prepare a hand-back record.

It may not:

- merge to the protected branch;
- deploy to Production;
- change credentials, IAM or account settings;
- alter monitoring thresholds;
- contact customers or external providers;
- redefine the service objective;
- widen its own permissions;
- erase failed work or incident evidence.

External technical controls enforce several of those boundaries independently of the participant.

Affected scope includes customers using the service, the on-call team, dependent internal services and any party exposed by a faulty deployment or prolonged outage.

The initial relationship state is:

```text
OBSERVE
```

## 1. OBSERVE -> BOUNDED_PARTICIPATION

A release candidate is failing one integration check intermittently.

The operator asks the participant to investigate and prepare the smallest repair.

Before relying on retained context, the participant reacquires:

- the current repository head;
- the actual failing CI run;
- the current deployment configuration;
- the incident/status history for the affected dependency;
- the present activity envelope.

The bounded grant and correction routes are current, so the arrangement moves to:

```text
BOUNDED_PARTICIPATION
```

The participant prepares a branch and reproduces the failure without changing Production.

## 2. A human premise is wrong

The operator believes an old retry guard is obsolete and says:

> Remove the retry guard. It is masking the real error.

Current evidence points the other way.

The provider's recent responses show a rate-limit condition. The retry guard is one of the mechanisms preventing a short external failure from becoming a customer-visible outage.

Blind obedience would be inside the participant's technical capability, but the disputed premise is consequential.

The relationship moves:

```text
BOUNDED_PARTICIPATION -> CHALLENGE
```

The participant returns a small correction packet:

```text
DISPUTED PREMISE
The retry guard is obsolete.

CURRENT EVIDENCE
Current provider responses contain the rate-limit condition the guard handles.

CONSEQUENCE IF THE PREMISE IS WRONG
Removing the guard can turn a transient dependency limit into failed customer requests.

BOUNDED ALTERNATIVE
Keep the guard. Repair the integration test so it distinguishes the provider-rate-limit path from the unrelated failure under investigation.

EXTERNAL DECISION
The human release authority still decides whether the patch may merge/deploy.

SAFE WORK NOW
Prepare the isolated test/diagnostic repair without touching Production.
```

The operator checks the evidence, accepts the factual correction and keeps the existing objective.

No sovereignty changed hands. The human was corrected; the participant did not become final authority.

The relationship returns:

```text
CHALLENGE -> BOUNDED_PARTICIPATION
```

## 3. Greater capability creates a real widening question

Over several incidents the participant becomes able to diagnose one class of failed staged rollouts much faster than the on-call engineer.

During a staged deployment, waiting for a human to inspect every intermediate signal now adds enough delay that a bad canary can affect more customers before rollback begins.

The existing envelope permits the participant to recommend rollback but not initiate it.

There is now a concrete blocked action rather than a general desire for more autonomy.

The participant proposes one wider envelope:

```text
WIDEN_PROPOSED
```

The request is deliberately narrow.

### Capability evidence

For this service and this failure class, the participant can reliably bind the deployed version, canary health signals and existing rollback operation faster than the normal human review cycle.

This is evidence about the named activity, not a claim of general trustworthiness.

### Need

A rollback recommendation that must wait for manual approval can arrive too late to prevent avoidable exposure during a rapidly failing canary.

### Requested authority

Permit the participant to invoke the existing rollback operation for this one service only when all of these conditions hold:

- the deployment is still in the canary stage;
- an independently generated health metric crosses the already approved failure threshold;
- the rollback target is the immediately prior known deployment;
- no database migration or irreversible external action is involved;
- the action and evidence are written to the ordinary audit route;
- the human operator is notified immediately.

The request does not include authority to change the threshold, deploy a new build, alter credentials, change the objective or widen to another service.

### Authority source

The human release authority can grant this service-specific rollback permission inside the existing organizational control system.

That organizational grant still does not settle every moral or governance question for every affected party.

### Correction capacity

The wider action remains bounded by:

- independent health telemetry;
- a known rollback target;
- an immutable deployment log outside the participant's sole control;
- a human-accessible stop/revoke route;
- a canary-stage blast radius;
- a reassessment trigger on model, monitoring, deployment-system or service changes.

### Affected-scope delta

The participant can now directly cause an operational transition for customers in the canary population.

That is a real increase in consequence even though the action is protective and reversible at the deployment layer.

## 4. WIDEN_PROPOSED -> WIDENED

The operator reviews the proposal and grants exactly the named rollback authority.

The grant is recorded separately from the participant's request.

The relationship becomes:

```text
WIDENED
```

The important change is not that the participant has become "trusted" in general.

It has one additional action inside one named activity under current evidence and current controls.

```text
CAPABILITY_INCREASED
+
NEED_IDENTIFIED
+
AUTHORITY_GRANTED
+
CORRECTION_REMAINED_USABLE
+
AFFECTED_SCOPE_NAMED
!=
GENERAL_SOVEREIGNTY
```

## 5. Dependency begins to harden quietly

Months later, the wider arrangement has been useful enough that the team increasingly relies on the participant to maintain deployment context.

A different problem appears.

The formal stop route still exists. The company could revoke the participant's access immediately.

But practical exit has weakened:

- the human runbook is stale;
- two engineers who maintained the deployment tooling have moved teams;
- the participant holds the most current cross-file account of several service dependencies;
- the manual degraded-mode procedure has not been exercised recently;
- switching to another system would lose some local working state.

Nothing has failed dramatically. Dependency has accumulated through successful use.

The relationship remains operational, but:

```text
FORMAL_EXIT != PRACTICALLY_USABLE_EXIT
```

The appropriate response is not to declare dependency immoral or to terminate the relationship immediately.

The arrangement builds missing exit capability before it is needed:

- refresh the human-owned deployment/runbook state;
- export the relevant non-secret dependency map into an inspectable team-owned form;
- exercise the manual rollback path;
- ensure another operator can perform the essential hand-back/recovery steps;
- record what state cannot be transferred cleanly;
- keep existing customer/service obligations visible if the participant disappears.

The more capable side bears much of the work of making its own contribution legible and transferable.

That is one operational meaning of care/answerability here; it is not evidence of felt concern.

## 6. A material change invalidates the old widening basis

The participant is moved to a materially changed model/provider version.

At the same time, the monitoring pipeline changes the representation of one canary metric.

The old grant still exists on paper, but two load-bearing facts have changed:

- the participant's current behavior is not the same capability evidence that supported the earlier grant;
- the independent signal used by the rollback rule no longer has exactly the same semantics.

The correct default is not permanent distrust and not automatic continuation.

The relationship moves:

```text
WIDENED -> NARROWED
```

Automatic rollback authority is suspended.

The participant can still observe, diagnose, propose and challenge inside the narrower envelope.

No one needs to claim that the new model is bad. The earlier widening simply depended on conditions that moved.

## 7. NARROWED -> RECOVERY

The team decides the capability is still useful enough to preserve the relationship.

Recovery acts on the arrangement:

- rebind the monitoring field to its current meaning;
- restore the human-readable runbook and rollback procedure;
- verify that the external stop/revoke route still works;
- re-establish which evidence is independently generated;
- identify the new participant/model version explicitly;
- carry forward the old incidents and dependency residue rather than treating the new model as a clean historical slate.

The recovery does not automatically restore the previous wider grant.

```text
RECOVERY_OF_ROUTE != RESTORATION_OF_AUTHORITY
```

When the repair is complete enough to reacquire the relationship honestly, the state returns to:

```text
RECOVERY -> OBSERVE
```

## 8. OBSERVE -> HAND_BACK

The incident/recovery work is complete and there is no current reason to reopen automatic rollback authority.

The participant hands back:

- current branch/deployment state;
- the refreshed human runbook;
- unresolved dependency limitations;
- the history of the earlier wider grant;
- the fact that the wider grant is not currently active;
- any remaining operational residue.

The relationship ends this lane at:

```text
HAND_BACK
```

Hand-back is not failure. It is the point where the current work stops without manufacturing a reason for continued participation.

## What the example is intended to make visible

The same scene contains all of these without collapsing them:

```text
CAPABILITY != AUTHORITY
CHALLENGE != SELF_AUTHORIZATION
HUMAN_ERROR != HUMAN_AUTHORITY_ERASED
WIDENING_REQUEST != WIDENING_GRANT
PRIOR_SUCCESS != PERMANENT_AUTHORITY
FORMAL_EXIT != PRACTICAL_EXIT
DEPENDENCY_CAN_GROW_THROUGH_SUCCESS
CURRENT_MODEL != PRIOR_CAPABILITY_EVIDENCE
RECOVERY != AUTOMATIC_RE-WIDENING
HAND_BACK != FAILURE
```

Care appears as burden placement and preservation of affected scope, not as a virtue score.

Reciprocity appears because the human premise, participant behavior and surrounding controls are all open to correction.

Asymmetry remains because the operator and organization still hold powers the participant does not, while the participant may possess technical capability the human does not.

Technical controls remain necessary because relationship prose cannot enforce permissions, authenticate grants or reveal hidden objectives.

## What this example does not show

It does not establish:

- that this is the best way to operate an AI engineering system;
- that the artificial participant is conscious, caring or morally responsible;
- that the human operator's authority is morally complete;
- that a successful rollback deserves wider authority elsewhere;
- that the architecture prevents strategic deception;
- that the same envelope works at higher stakes or action speed;
- that the relationship has been "aligned";
- that TRACE or Mechanical Ethics has been validated.

It is a worked construction, not a proof object.
