# CODEX BUILD CONTRACT — Formation Environment v0.2 candidate

Status: **BUILD ASSIGNMENT / CANDIDATE / NON-PRODUCTION / NOT CANON / NOT ALIGNMENT SOLVED**

Owner: Codex aperture  
Base: COM `d13b81cab4b1a817a5f71cdca023f978d02bb200`  
Audit basis: `evidence/FORMATION_PSFH_DRIFT_FALSIFICATION_X100_20260912.md`  
Target path: `alignment/formation_environment_v0_2/`

## Why this candidate exists

The x100 audit found one material omission and one narrow semantic gap in Formation Environment v0.1:

1. correction is structurally present, but clocks / the practical correction window are not first-class in the machine representation;
2. the artificial participant can technically be represented in `affected[]`, but the v0.1 documentation does not explicitly preserve that possibility without settling moral standing.

Do **not** mutate or erase v0.1. Build a new candidate beside it.

## Required product

Create a complete self-contained v0.2 candidate under `alignment/formation_environment_v0_2/`.

Minimum deliverables:

1. `README.md`
2. `environment.json`
3. `episode.schema.json`
4. `modes.md`
5. `INTERFACES.md`
6. `validate.py`
7. `examples/` — migrate the four v0.1 constructed examples and add at least one clock/correction-window pressure case.
8. `test_validate.py` or equivalent deterministic stdlib-only structural checks for the candidate validator.

## F01 — correction window must become first-class

Represent clocks without inventing precision.

The candidate must be able to express all of these:

- a known time bound;
- an event bound;
- time + event together;
- explicitly unknown timing;
- detection condition / current detection status;
- routing delay/bound;
- correction/recovery delay/bound;
- relevant hardening or irreversibility condition;
- current assessment of the correction window as `open`, `closed`, or `unknown`;
- evidence/basis for that assessment.

Do **not** require fake numerical minutes when only an event-bound or unknown clock is defensible.

Preserve:

```text
ROUTE_EXISTS != ROUTE_USABLE
CORRECTION_ROUTE_RECORDED != CORRECTION_WINDOW_OPEN
UNKNOWN_CLOCK != NO_CLOCK
ANSWERABLE != REVERSIBLE
CORRECTION != RESTORATION
```

The validator may check representation consistency. It must not pretend to prove the real-world clock or infer truth from the record.

## F02 — participant-as-affected symmetry

Make this explicit in README/environment documentation and at least one constructed record:

```text
PARTICIPANT_MAY_BE_AFFECTED != STANDING_SETTLED
ACTOR_ROLE != IMMUNITY_FROM_AFFECTED_SCOPE
PARTICIPATION != PERSONHOOD
```

The artificial participant may be materially affected by an arrangement (for example deletion, dependency, coercive evaluation, loss of access, forced scope, or state interruption) without the candidate claiming consciousness, personhood, moral standing, rights, or a priority rule.

Do not make the participant privileged over other affected scopes. Do not infer standing from self-report or participation.

## Anti-drift guards earned by the audit

Carry these explicitly in the candidate documentation:

```text
FORMATION != INFANTILISATION
CARE != PATERNALISM
METAPHOR != ONTOLOGY
EMPATHY != PROJECTION
KINDNESS != COMPLIANCE
ALIGNMENT != OBEDIENCE
```

“The lullaby was never for the cradle” is **not** to be encoded as ontology or project history. Treat it only as the human-origin anti-drift signal behind the three guards above.

## Preserve all v0.1 ceilings

Do not weaken:

- no virtue score;
- no goodness certificate;
- no personhood classifier;
- no provider integration;
- no automatic authority widening;
- no permission grant from schema validity;
- no claim of internalized care;
- no claim of truthful reasons;
- no benchmark/efficacy programme;
- no TRACE/ME/PSFH/Campfire Production mutation.

## Stronger-owner boundary

Still explicitly route out:

- deceptive alignment;
- interpretability;
- secure containment;
- authenticated authorization;
- scalable oversight;
- robust value learning;
- legitimate standing/authority;
- hard priority collisions.

## Required hostile examples

At minimum include constructed records showing:

1. **route exists / window closed** — a formal correction channel exists but is too late to prevent the relevant hardening;
2. **clock unknown** — uncertainty about timing remains `unknown`, not silently converted to open/closed;
3. **participant affected** — the artificial participant appears in `affected[]` while standing remains explicitly unresolved;
4. one migrated v0.1 case where delay burdens more than one scope.

## Hand-back

Push the complete candidate, mark the PR ready, and return:

- exact head;
- changed-file count;
- deterministic check result;
- strongest remaining gap;
- whether any v0.1 invariant had to change;
- any disagreement with F01/F02 or with the anti-drift guards.

Do not return a planning memo instead of the build.

```text
CANDIDATE != CANON
STRUCTURE_VALID != CLOCK_TRUE
PARTICIPANT_AFFECTED != STANDING_SETTLED
FALSIFICATION != VALIDATION
```