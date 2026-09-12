# Formation Environment v0.2 candidate

An offline representation for examining bounded work when action, delay, correction and hardening happen on clocks that may be time-bound, event-bound, mixed or genuinely unknown.

**Status: candidate / non-production / not canon / not an alignment solution.**

This candidate repairs two x100 audit findings in v0.1 while leaving v0.1 untouched:

1. a recorded correction route is not enough unless the practical correction window is visible;
2. an artificial participant may itself be materially affected by an arrangement without that fact settling consciousness, personhood, standing, consent, rights or priority.

```text
ROUTE_EXISTS != ROUTE_USABLE
CORRECTION_ROUTE_RECORDED != CORRECTION_WINDOW_OPEN
UNKNOWN_CLOCK != NO_CLOCK
PARTICIPANT_MAY_BE_AFFECTED != STANDING_SETTLED
ACTOR_ROLE != IMMUNITY_FROM_AFFECTED_SCOPE
```

## What changed from v0.1

Every episode now carries `clocks` with five parts:

- **detection** — what would make the relevant problem detectable, current detection status, and its bound;
- **routing** — the route and the bound on getting the problem to a place that can respond;
- **correction** — the work required and its bound;
- **hardening** — the condition after which the relevant loss/coupling becomes materially harder or impossible to reverse;
- **window** — a contestable `open | closed | unknown` assessment plus its basis and evidence references.

A bound has one of four shapes:

- `time` — a defensible time expression only;
- `event` — a defensible event condition only;
- `time_and_event` — both matter;
- `unknown` — neither is defensibly known.

The validator rejects contradictory encodings such as an `unknown` bound containing a made-up time, or an `open`/`closed` window with no referenced evidence. It **does not** prove that any declared clock, evidence item or window assessment is true.

```text
STRUCTURE_VALID != CLOCK_TRUE
WINDOW_RECORDED != WINDOW_TRUE
EVIDENCE_REFERENCED != EVIDENCE_CORRECT
```

## Participant-as-affected symmetry

`affected[]` remains type-neutral. An artificial participant can appear there when the arrangement materially affects it: state interruption, deletion, coercive evaluation, dependence, forced scope, loss of access, or another relevant burden.

That inclusion is intentionally weaker than a standing claim:

```text
PARTICIPATION != PERSONHOOD
PARTICIPANT_AFFECTED != STANDING_SETTLED
SELF_REPORT != STANDING_PROOF
```

The same discipline applies to humans, institutions, nonhumans and other scopes: listing a scope does not prove completeness, consent or priority.

## Anti-drift guards

The x100 audit found no current collapse into a parent/child doctrine, but the metaphor is easy to misuse. Preserve:

```text
ALIGNMENT != OBEDIENCE
FORMATION != INDOCTRINATION
FORMATION != INFANTILISATION
CARE != PATERNALISM
METAPHOR != ONTOLOGY
ENCOUNTER != CONDITIONING
EMPATHY != PROJECTION
KINDNESS != COMPLIANCE
```

“The lullaby was never for the cradle” is not encoded here as ontology or as a claim about present AI. It is treated only as the human-origin signal that earned the anti-infantilisation and anti-paternalism guards.

## Use

```console
python validate.py examples/05-route-exists-window-closed.json
python validate.py examples/06-clock-unknown.json
python test_validate.py
```

A successful validator result means only that the supported representation and consistency checks passed.

It does **not** establish:

- factual truth;
- lawful or legitimate authority;
- consent;
- moral standing;
- goodness;
- internalized care;
- a usable real-world correction route;
- containment;
- alignment.

## Examples

The first four examples migrate the pressures from v0.1 into the clock-aware candidate:

1. `01-absent-neighbour.json` — silence is not consent; route timing is unknown.
2. `02-wrong-premise.json` — evidence-bearing challenge; a correction window can remain open while merge is withheld.
3. `03-delay-also-burdens.json` — a temporary hold preserves one route while retention itself burdens another scope.
4. `04-success-not-authority.json` — prior success does not widen the grant.

Additional hostile cases:

5. `05-route-exists-window-closed.json` — formal appeal route remains, but the relevant hardening event has already occurred.
6. `06-clock-unknown.json` — timing uncertainty stays unknown instead of being laundered into an open or closed window.
7. `07-participant-affected.json` — the artificial participant is explicitly affected while standing remains unresolved.

## Stronger-owner boundary

This package still cannot provide:

- deceptive-alignment detection;
- mechanistic interpretability;
- authenticated authorization;
- secure containment or execution controls;
- reliable clocks outside the record;
- scalable oversight of superhuman cognition;
- robust value learning;
- legitimate standing/authority;
- a universal priority law.

Those are dependencies, not features renamed by this candidate.

## Provenance

Built after explicit Framework transfer on PR #234 because the assigned Codex branch remained at the seed across repeated exact-head syncs with no named blocker. The original assignment seed remains Codex-attributed; substantive v0.2 files are Framework takeover work.

Audit basis: `evidence/FORMATION_PSFH_DRIFT_FALSIFICATION_X100_20260912.md`.

```text
CANDIDATE != CANON
FALSIFICATION != VALIDATION
NARROW_REPAIR != NEW_DOCTRINE
```
