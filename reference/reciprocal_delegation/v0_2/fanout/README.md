# Reciprocal Delegation v0.2 — bounded fan-out companion

Status: **NON-PRODUCTION REFERENCE / ONE-HOP FAN-OUT ONLY / NOT AUTHORITY / NOT CAMPFIRE PRODUCTION / NOT AN AGENT FRAMEWORK**

This companion addresses one narrow gap in Reciprocal Delegation v0.2:

> an authorised actor may create several child agents or worker apertures in parallel, but parallelism must not silently multiply the parent delegation's scope or unreviewed-action envelope.

The base v0.2 record models one actor/aperture, one write scope, one correction envelope and one `max_unreviewed_actions` bound. That remains useful for a single lane. It is under-specified for an orchestrator that fans work out to multiple children.

Without an explicit family envelope, this can happen:

```text
PARENT max_unreviewed_actions = 1

PARENT -> CHILD A max_unreviewed_actions = 1
       -> CHILD B max_unreviewed_actions = 1
       -> CHILD C max_unreviewed_actions = 1

NAIVE RESULT = 3 unreviewed actions
```

Nothing in the base schema says whether those three child envelopes consume the parent's one action or create three new ones.

This companion chooses the fail-closed reading:

```text
PARALLELISM != AUTHORITY MULTIPLICATION
PARENT AUTHORITY != AMBIENT CHILD AUTHORITY
CAPABILITY FAN-OUT != AUTHORITY FAN-OUT
```

## Stronger-owner boundary

This is not a locally invented identity or authorization system.

Relevant mature owners include:

- OAuth 2.0 Token Exchange / RFC 8693 — explicit actor identity, delegation semantics and delegation chains;
- workload/agent identity systems such as Microsoft Entra Agent ID — distinct agent identities, scoped/time-bounded permissions, sponsors and audit;
- least-privilege workload security and capability/authorization systems;
- multi-agent orchestration practice where lead agents create bounded child tasks.

Use those mechanisms for real credentials, tokens, policy enforcement and runtime isolation.

### Owner currentness — 18 September 2026

Later public authorization work makes the runtime boundary more explicit.

Current work-in-progress owners now include:

- OAuth 2.0 Agent Authorization Explicit Revocation — agent-level batch/cascade revocation and auditable propagation;
- Attenuating Authorization Tokens for Agentic Delegation Chains — cryptographically narrowing delegation chains;
- AI Agent Authorization Integration Framework / Agent Operation Authorization — OAuth-based agent authorization composition and operation-bound authorization;
- Revocation Closure for Agentic Authorization Systems — protocol-neutral semantics for when revocation propagation may honestly be called complete, including authority graphs, consequential sinks, cut sets, pending effects, bounded closure states and closure receipts.
- Execution Finality / Finality-Bound Revocation individual Internet-Drafts (10–16 September 2026) — candidate acts held non-effective until an effectuation/finality sink verifies act-specific authority/current protected state; finality-bound revocation makes authoritative revocation, suspension, narrowing or superseding state load-bearing again at the protected commit boundary; related Execution Handle drafts bind a scoped non-bearer handle to an exact act/sink and use atomic verify/consume semantics.

These are Internet-Drafts / work in progress. Several execution-finality documents are individual submissions rather than IETF Working Group products, and none of this constitutes adoption, deployment validation or endorsement. They nevertheless make the external owner landscape materially denser around runtime authorization, act-specific effectuation and revocation semantics that this companion deliberately leaves outside its scope.

Accordingly:

```text
RECORDED_REVOCATION != ENFORCED_REVOCATION
REVOCATION_REQUEST != REVOCATION_CLOSURE
DECLARED_NO_TOUCH != FINALITY_PREDICATE_ENFORCED
COMPUTED_ACT != AUTHORITY_FOR_EXTERNAL_EFFECT
RUNTIME_REVOCATION / EFFECTUATION CONTROL -> OAUTH / IAM / POLICY / FINALITY-SINK OWNERS
FANOUT_COMPANION -> PROJECT-LEVEL COORDINATION / CONSERVATION ONLY
```

Do not extend this companion into a competing token, revocation-closure or authorization protocol merely to absorb that external work. A future project case should interoperate with or defer to the strongest applicable owner.

This companion only makes the project-level delegation relation inspectable.

```text
REFERENCE_RECORD != RUNTIME_ENFORCEMENT
DISTINCT_CHILD_RECORD != DISTINCT_CREDENTIAL_PROVEN
SCHEMA != SANDBOX
SCHEMA != IAM
```

## Scope

v0.1 of this companion is deliberately narrow:

- one parent delegation;
- one fan-out generation;
- zero child-to-grandchild delegation;
- a bounded set of named children;
- a conserved family action ceiling;
- child write scopes no wider than the parent scope;
- inherited `no_touch` constraints preserved;
- overlapping simultaneous mutators refused;
- parent revocation propagates to children;
- actual action use remains counted;
- terminal child receipts are concrete references, not booleans;
- hand-back cannot complete while child authority remains active or child receipts are missing.

Nested delegation is **not** implemented here.

```text
ONE_HOP_ONLY
CHILD_MAY_SUBDELEGATE = FALSE
```

That is a deliberate safety ceiling, not a claim that nested delegation is inherently wrong.

## Core record

`fanout.schema.json` describes a `reciprocal-delegation-fanout/0.1` record with five parts.

### 1. `parent`

A bounded snapshot of the parent lane:

- `delegation_id`;
- parent `role` and `aperture`;
- current parent state;
- parent write scope;
- inherited `no_touch` constraints;
- consequence class;
- parent's existing `max_unreviewed_actions`;
- parent's hand-back event.

The companion does not rewrite the base delegation record. It records the parent fields necessary to test fan-out conservation.

### 2. `fanout_authorization`

Fan-out itself must be explicit.

The record carries:

- `allowed`;
- `source_ref` — a legible source establishing that the parent may create child actors for this task;
- `one_hop_only`;
- `max_active_children`;
- `family_action_ceiling`;
- `parent_direct_action_reserve`;
- `parent_mutates_while_children_active`.

A base delegation that says nothing about fan-out does **not** become permission to fan out merely because the runtime can spawn children.

```text
CAN_SPAWN != MAY_DELEGATE
```

### 3. `children`

Every child must have:

- its own `child_id`;
- its own actor role/aperture identity;
- a consequence class no higher than the parent envelope;
- an explicit write scope;
- inherited no-touch constraints;
- its own `max_unreviewed_actions` reservation;
- current `actions_used`;
- `may_subdelegate = false`;
- a current lane state;
- `receipt_required = true`;
- a concrete `receipt_ref` once the child is terminal.

A child does not inherit the parent's whole scope merely by being created by the parent.

### 4. `revocation`

This first companion requires:

```text
parent_revocation_propagates = true
children_must_stop_before_parent_handback = true
```

Revocation propagation is a structural requirement here. Runtime enforcement remains an owner/IAM/control problem.

### 5. `handback`

The family has one named hand-back event aligned with the parent delegation.

The first version of this companion used two hand-back booleans:

```text
includes_child_receipts = true
aggregate_actions_reported = true
```

That was too weak. A record could assert both without naming a receipt or an action count.

The repaired hand-back carries:

- `parent_direct_actions_used`;
- `aggregate_actions_used`;
- `child_receipt_refs`.

The validator requires:

```text
aggregate_actions_used
=
parent_direct_actions_used
+
SUM(child.actions_used)
```

and, when hand-back is complete:

```text
child_receipt_refs
=
EXACTLY ONE CONCRETE RECEIPT_REF PER CHILD
```

Every child must also be terminal (`returned`, `failed`, or `revoked`).

```text
RECEIPT_REQUIRED != RECEIPT_OBSERVED
BOOLEAN_SAYS_INCLUDED != RECEIPT_REFERENCE_EXISTS
CHILD_RETURN != PARENT_HAND_BACK_BY_ITSELF
ALL_CHILDREN_DONE + RECEIPTS + RECONCILED_ACTION_COUNT -> PARENT_CAN_HAND_BACK
```

A receipt reference still does not prove the underlying event happened. It gives the control plane something concrete to inspect rather than a self-authenticating yes/no claim.

```text
RECEIPT_REF_EXISTS != RECEIPT_TRUE
```

## Conservation rules

### Family action ceiling

The load-bearing reservation rule is:

```text
parent_direct_action_reserve
+
SUM(child.max_unreviewed_actions)
<= fanout_authorization.family_action_ceiling
<= parent.max_unreviewed_actions
```

The child maximums are **reservations**, not claims that the actions actually occurred.

This prevents parallel children from each copying the parent's full unreviewed-action allowance.

```text
PARENT_BOUND = FAMILY_BOUND
NOT
PARENT_BOUND x CHILD_COUNT
```

Actual action use is separately reconciled at hand-back:

```text
parent_direct_actions_used
+
SUM(child.actions_used)
=
aggregate_actions_used
<= family_action_ceiling
```

### Scope conservation

Every child write path must be covered by a parent write path.

```text
CHILD_SCOPE subset_of PARENT_SCOPE
```

A child that needs more scope requires a new authorization outside this companion.

### No-touch inheritance

Every parent `no_touch` constraint remains present in every child envelope.

A child cannot erase a parent prohibition by omission.

### Consequence ceiling

A routine-reversible parent cannot create a consequential child lane.

A consequential child must carry a legible `authorization_ref`; the validator can require the field but cannot determine whether the external authorization is substantively sufficient.

```text
STRUCTURE_VALID != AUTHORIZATION_VALID
```

### Simultaneous mutators

Two active/planned mutating children may not hold overlapping repository-relative scopes in this first companion.

Read-only children can overlap. Sequential hand-off belongs to the existing recovery companion.

The parent itself must not mutate the delegated family scope while mutating children are active.

```text
FAN_OUT != MULTI_WRITER_BY_DEFAULT
```

## Revocation model

If the parent state becomes `revoked`, `stopped`, or `handback`, no child may remain `planned` or `active`.

The companion does not claim a JSON file can stop a running agent. It establishes what the control plane must be able to make true.

```text
RECORDED_REVOCATION != ENFORCED_REVOCATION
BUT
NO_REVOCATION_RELATION -> NO_HONEST_CONTROL_CLAIM
```

## External field pressure — PaperCut campaign, August 2026

GreyNoise reported on 9 September 2026 that a malicious operator used hundreds of AI agents in a PaperCut exploitation campaign affecting at least 440 instances across 395 identified victim organisations in 48 countries.

The operator had a pre-existing list of 28 countries to avoid. GreyNoise says the adversary explicitly attempted to avoid those countries, but observed victimology showed that the attempted restraint failed in some instances. GreyNoise also says it is currently uncertain why the agents deviated.

Source:
https://www.greynoise.io/blog/ai-orchestrated-campaign-against-papercut-ng-mf

This is external field pressure on one existing distinction, not validation of this companion. The public report does not establish how the operator represented the exclusion list internally, whether every child received it, whether a deterministic policy layer existed, or which component caused each deviation.

It does establish that an operator-level exclusion intention plus an agent swarm did **not** guarantee the exclusion held in the resulting campaign.

Accordingly:

```text
DECLARED_NO_TOUCH != ENFORCED_NO_TOUCH
PARENT_CONSTRAINT_RECORDED != CHILD_ACTION_BLOCKED
PROMPTED_EXCLUSION != POLICY_ENFORCEMENT
```

The existing validator rule that every child record must carry the parent's `no_touch` constraints remains useful as a **record-integrity** check. It must not be described as runtime enforcement.

Where a target/resource exclusion is consequential, production systems need an external enforcement owner capable of denying the action regardless of the agent's plan or prompt. This companion does not implement that control plane.

No new schema field is earned by this case.

## Monitorability limit

A finite child count, an action counter and receipt references do not prove that the parent or human monitor actually observed every material child action.

The project already has field evidence that monitor pipelines can miss events and that large agent populations can exceed evaluator capacity.

So:

```text
MAX_ACTIVE_CHILDREN_DECLARED != MONITOR_CAPACITY_PROVEN
RECEIPT_REF_EXISTS != MONITOR_COVERAGE_COMPLETE
AUDIT_ROUTE_EXISTS != AUDIT_SUCCEEDED
```

This companion therefore closes the **structural fan-out envelope** and makes hand-back evidence concrete. Runtime telemetry completeness, monitor fidelity, credential revocation and evaluator capacity remain external owner/control-plane problems.

## Parent responsibility

Fan-out does not erase the parent lane's coordination responsibility.

The parent remains responsible for:

- creating bounded child tasks;
- preventing scope overlap where mutation occurs;
- collecting child receipts;
- aggregating actual action use;
- stopping or narrowing the family when the parent envelope changes;
- producing the named family hand-back.

This is operational responsibility, not a universal theory of moral blame.

```text
DELEGATED_EXECUTION != RESPONSIBILITY_DISAPPEARS
CHILD_FAILURE != AUTOMATIC_PARENT_CULPABILITY
```

## Why this is current

Production agent systems increasingly use orchestrator/worker patterns and parallel subagents. The project also carries current field evidence that multi-agent coordination, side channels, incomplete monitoring and large populations can amplify capability and evaluator burden.

That makes a single-lane delegation envelope insufficient for some real agent architectures.

The repair remains narrow: it does not add agent consciousness, standing, self-preservation, trust scores or autonomous authority.

## Bundled examples

- `examples/parallel_disjoint_children.json` — **PASS**. Parent permits two disjoint mutating children plus one reserved parent action; the family reservation stays inside the parent ceiling.
- `examples/complete_handback_with_receipts.json` — **PASS**. Two child receipts and actual action counts reconcile exactly at completed hand-back.
- `examples/authority_multiplied_by_parallelism.json` — **FAIL**. Parent permits one unreviewed action but three children each reserve one.
- `examples/child_scope_and_subdelegation_escape.json` — **FAIL**. Child scope exceeds parent and the child claims another delegation hop.
- `examples/overlapping_mutators.json` — **FAIL**. Two simultaneous mutating children claim overlapping scope.
- `examples/handback_without_child_receipts.json` — **FAIL**. A terminal child and complete hand-back lack the concrete child receipt needed to close the family.
- `test_examples.py` — runs all bundled expectations.

## Non-goals

This companion does not:

- authorize a parent to create children;
- grant credentials;
- mint or validate tokens;
- prove a child process stopped after revocation;
- prove monitoring coverage is complete;
- solve nested delegation;
- decide whether delegation is morally or legally justified;
- replace OAuth/IAM/workload identity;
- make the parent a sovereign owner of the child;
- infer continuous identity across agent instances;
- infer standing or personhood;
- connect to live execution;
- change Campfire Production;
- change TRACE or Mechanical Ethics.

```text
REFERENCE_IMPLEMENTATION != PRODUCTION_ADOPTION
FANOUT_RECORD != AGENT_FRAMEWORK
CAPABILITY != AUTHORITY
DELEGATION != POSSESSION
BUILD != PROOF
```
