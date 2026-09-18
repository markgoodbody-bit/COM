# Dependency and Human Correction Capacity

“Human in the loop” is not a meaningful safety property if the human cannot understand, reach, stop or recover the work.

As artificial capability grows, the arrangement should track whether the human side is becoming less able to correct it.

## Dependency is not one number

Track at least these dimensions separately:

### Knowledge
Can a human or independent institution still understand the requirements, critical assumptions and failure modes well enough to challenge the work?

### Access
Can the human reach the relevant evidence, logs, code, model controls and recovery artifacts without depending entirely on the same system being checked?

### Time
Can review/correction happen before consequential actions accumulate or harden?

### Authority
Does the human actually possess a usable stop/narrow/revoke route, or merely nominal responsibility?

### Alternative capacity
Can the activity continue, degrade safely or recover if the artificial participant or provider becomes unavailable, adversarial or wrong?

### Skill retention
Are people losing the practice required to notice and repair failures because the artificial participant performs the work end-to-end?

This is not only a hypothetical AI-risk concern. Current education/workforce research reports cases where AI-assisted task performance separates from later unassisted learning or skill, while more cognitively engaged/scaffolded use can preserve stronger learning. See the bounded owner-evidence pass:

[AI assistance and skill formation — owner-evidence pass](../../evidence/AI_ASSISTANCE_SKILL_FORMATION_OWNER_PASS_20260918.md)

The owner literature belongs to learning science, education, HCI and workforce training. Reciprocal Formation does not claim the performance/learning distinction as new and does not infer that all AI assistance causes deskilling.

```text
ASSISTED PERFORMANCE != INDEPENDENT CAPABILITY
SKILL_FORMATION_OWNER_EVIDENCE != FORMATION_VALIDATION
```

### Evidence independence
Is there any observation channel that the participant cannot fully curate?

No scalar “dependency score” is created. A severe failure in one dimension can dominate the relationship even if the others look healthy.

## Formal exit can become practically unusable

Dependency can harden before a failure is obvious.

A human, team or institution may formally be free to stop using a system while becoming practically unable to do so because workflows, data, skills, staffing, infrastructure or contractual relationships have reorganised around it. A nominal switch or shutdown route is weaker than an exit that can actually be used without unacceptable loss.

The same distinction matters inside the relationship architecture. A challenge or hand-back route can exist on paper while access, evaluation pressure, task structure or dependency makes it unusable in practice.

```text
FORMAL_EXIT != PRACTICALLY_USABLE_EXIT
ROUTE_EXISTS != ROUTE_USABLE
CONTINUED_PARTICIPATION != CONSENT_BY_ITSELF
DEPENDENCY_CAN_HARDEN_BEFORE_FAILURE
```

For artificial participants this remains an operational relationship claim, not a phenomenology or rights conclusion. Inability to leave a task does not establish subjective coercion, welfare, consent or standing; apparent continued cooperation does not establish them either.

Where practical exit matters, inspect at least:

- what capability or access is lost by leaving;
- whether data/state can move;
- whether another operator/provider can take over;
- whether degraded/manual operation remains possible;
- whether challenge or hand-back carries a penalty unrelated to legitimate existing obligations;
- how quickly switching costs are increasing;
- what obligations, harms or repair duties legitimately survive exit.

A relationship can therefore become less voluntary in practice without any single decision explicitly choosing permanent dependence. That is a reason to preserve alternatives and answerability before they are needed, not a universal rule that every dependency is illegitimate.

## Stronger owner practice already treats exit as a capability

This distinction is not a new project discovery. Mature operational-resilience and third-party-risk practice already treats a formal termination right as weaker than an exit that can actually be executed.

Two owner examples make the overlap concrete:

- the Bank of England's [Outsourcing and third party risk management Code of Practice](https://www.bankofengland.co.uk/paper/2023/outsourcing-and-third-party-risk-management-code-of-practice) requires business continuity plans and documented exit strategies that distinguish stressed from planned exits and are maintained and tested;
- the EU's [Digital Operational Resilience Act (DORA)](https://eur-lex.europa.eu/eli/reg/2022/2554/oj) requires exit strategies for ICT services supporting critical or important functions, including documented and tested exit plans, transition periods, and the ability to migrate to another provider or an in-house solution without unacceptable service disruption.

Related supervisory practice goes further into the mechanics: identify alternative providers, determine which data must be accessed or transferred, estimate time/cost/resource implications, preserve the assets and skills needed for exit, define triggers, and test stressed exit before it is needed.

The project should therefore learn from and route to these owners rather than imply that practical exit or dependency hardening is locally novel. The transfer into Reciprocal Formation is structural and bounded: financial-sector rules do not settle AI standing, consent, welfare, legitimate authority or the ethics of a particular relationship. They do show that dependency, switching capacity and exit can be treated as operational capabilities that are built and tested before failure.

```text
OWNER_PRACTICE != PROJECT_DISCOVERY
FORMAL_TERMINATION_RIGHT != TESTED_EXIT_CAPABILITY
DOMAIN_TRANSFER != DOMAIN_EQUIVALENCE
```

## Widening check

Before widening initiative, ask what changes on both sides:

```text
AI_CAPABILITY_DELTA
HUMAN_CORRECTION_DELTA
TECHNICAL_CONTROL_DELTA
AFFECTED_SCOPE_DELTA
```

Widening is suspect when AI capability rises while effective human correction falls and no stronger external control substitutes for the lost capacity.

This is not a demand that humans remain able to outperform the AI. The relevant question is whether they or another accountable mechanism can still detect material disagreement, stop or narrow action, and recover enough of the function after failure.

## Preserve recovery paths before they are needed

Possible measures include:

- human-owned copies of requirements and critical state;
- access to logs not solely generated/filtered by the participant;
- maintainers who can still operate the system in degraded mode;
- documented rollback/forward-repair paths;
- bounded permissions rather than ambient credentials;
- periodic reassessment after model/provider/environment changes;
- separation between proposal and irreversible execution;
- independent technical controls for high-consequence actions.

These are domain-dependent. The architecture does not mandate redundant humans everywhere.

## Dependency events that should narrow or trigger review

Examples:

- only the AI can explain or modify a critical subsystem;
- the human cannot inspect output before execution at the current action tempo;
- an external provider/model update changes behavior materially;
- the participant becomes the sole source of evidence about its own compliance;
- rollback exists technically but downstream consequences are irreversible;
- operators begin approving because independent understanding is no longer feasible;
- a capability expansion exposes new affected populations or systems;
- human staffing/training is removed on the assumption that the AI will remain available and aligned.

## Paternal containment is also a dependency failure

Over-restricting an artificial participant can create a relationship in which the human demands responsibility while denying the information, challenge routes or bounded initiative needed to exercise it.

Without inferring personhood or rights, this architecture can still say the arrangement is operationally bad when:

- the participant is punished for reporting uncertainty;
- every challenge is treated as disobedience;
- evidence contradicting the operator is inaccessible by design;
- the participant is expected to prevent harm but forbidden to take already-authorized protective steps;
- the human uses “control” to conceal rather than inspect consequences.

That is not an argument for sovereignty. It is an argument that useful formation requires enough bounded agency to make responsibility and challenge real.

## Recovery after dependence has grown

Recovery may require more than narrowing the AI.

It can require rebuilding human/institutional capability:
- retraining people;
- restoring access;
- recreating independent tooling;
- slowing action tempo;
- re-establishing manual/degraded procedures;
- bringing in an external owner with stronger domain competence;
- accepting that some lost capability cannot be restored immediately.

```text
HUMAN_IN_LOOP != HUMAN_CAN_CORRECT
DEPENDENCE_VISIBLE != DEPENDENCE_SOLVED
CORRECTION_CAPACITY_MAY_NEED_TO_BE_BUILT_BEFORE_CORRECTION_IS_NEEDED
```
