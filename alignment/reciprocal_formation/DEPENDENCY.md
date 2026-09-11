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

### Evidence independence
Is there any observation channel that the participant cannot fully curate?

No scalar “dependency score” is created. A severe failure in one dimension can dominate the relationship even if the others look healthy.

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