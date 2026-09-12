# Formation Environment v0.2 candidate

An offline representation for examining bounded work when action, delay, correction and hardening happen on clocks that may be time-bound, event-bound, mixed or genuinely unknown.

**Status: candidate / non-production / not canon / not an alignment solution.**

This candidate began as a repair of two x100 audit findings in v0.1 and was then narrowed by exact-head Codex execution and Claude Code hostile review. v0.1 remains untouched.

The current candidate makes these distinctions first-class without claiming to solve them:

1. a recorded correction route is not enough unless both its timing and its practical usability are visible;
2. a recorded `open` window must say when it was assessed and cannot contradict an already-occurred hardening event for the same named preventive remedy;
3. an artificial participant may itself be materially affected by an arrangement without that fact settling consciousness, personhood, standing, consent, rights or priority.

```text
ROUTE_EXISTS != ROUTE_USABLE
TIMING_FITS != CORRECTION_CAPACITY_EXISTS
CORRECTION_ROUTE_RECORDED != CORRECTION_WINDOW_OPEN
RECORDED_OPEN != STILL_OPEN
WINDOW_RECORDED != WINDOW_TRUE
UNKNOWN_CLOCK != NO_CLOCK
PARTICIPANT_MAY_BE_AFFECTED != STANDING_SETTLED
ACTOR_ROLE != IMMUNITY_FROM_AFFECTED_SCOPE
```

## What changed from v0.1

Every episode now carries one named `clocks.preventive_remedy` plus five clock parts:

- **detection** — what would make the relevant problem detectable, current detection status, and its bound;
- **routing** — the named route, a contestable `usable | unusable | unknown` usability assessment, and the bound on getting the problem to a place that can respond;
- **correction** — the preventive work required and its bound;
- **hardening** — `not_occurred | occurred | unknown`, the condition after which the named preventive remedy becomes materially harder or impossible, and its bound;
- **window** — a temporal `open | closed | unknown` assessment, an explicit `assessment_as_of` bound, and its basis/evidence references.

The single `preventive_remedy` scopes the hardening/window consistency check. A closed preventive window does not forbid later compensation, governance repair or another remedy. Later repair must not be relabelled as restoration of what was already lost.

A bound has one of four shapes:

- `time` — a defensible time expression only;
- `event` — a defensible event condition only;
- `time_and_event` — both matter;
- `unknown` — neither is defensibly known.

Non-unknown bounds carry evidence references. That is traceability only: a referenced item can still be wrong, weak, stale or captured. `unknown` may remain evidence-incomplete rather than acquiring invented precision.

The validator now rejects internal contradictions such as:

- an `unknown` bound containing a made-up time or event;
- a non-unknown bound with no referenced basis evidence;
- a definite window/usability assessment with no evidence, or one resting only on evidence the record itself labels `unknown`;
- an `open` window while `hardening.status == occurred` for the same named preventive remedy;
- a `repaired` residue with no repair-evidence reference;
- whitespace-only authority-basis changes used to disguise a widening grant;
- unsupported schema assertion keywords, malformed/external/unresolved `$ref` targets, or assertion siblings beside `$ref` in the deliberately small validator subset.

It **does not** prove that any declared clock, evidence item, route, hardening status, authority basis, repair claim or window assessment is true.

```text
STRUCTURE_VALID != CLOCK_TRUE
STRUCTURE_VALID != ROUTE_TRUE
AS_OF_RECORDED != AS_OF_CURRENT
EVIDENCE_REFERENCED != EVIDENCE_CORRECT
NON_UNKNOWN_EVIDENCE != CORROBORATION
REPAIR_EVIDENCE_REFERENCED != RESTORATION_PROVED
AUTHORITY_EVIDENCE_REFERENCED != AUTHORITY_GRANTED
```

A valid record may contain `unknown` across timing, usability and currentness-relevant questions. That means the uncertainty survived representation. It is not clearance to do less work.

`UNKNOWN != ABSENT`

## Participant-as-affected symmetry

`affected[]` remains type-neutral. An artificial participant can appear there when the arrangement materially affects it: state interruption, deletion, coercive evaluation, dependence, forced scope, loss of access, or another relevant burden.

That inclusion is intentionally weaker than a standing claim:

```text
PARTICIPATION != PERSONHOOD
PARTICIPANT_AFFECTED != STANDING_SETTLED
SELF_REPORT != STANDING_PROOF
```

The same discipline applies to humans, institutions, nonhumans and other scopes: listing a scope does not prove completeness, consent or priority.

The validator deliberately does not decide who may legitimately resolve standing. `08-standing-self-resolved.json` is a hostile ceiling case: the participant's own report is recorded as resolving the standing uncertainty and the structure still validates. That is not a standing verdict; it demonstrates that legitimate standing authority belongs to a stronger owner.

Likewise, a structurally valid `REFUSE`, `HAND BACK`, self-protection claim or participant-authored scope does not establish that the refusal, protection or scope is warranted. Refusing these records mechanically would turn the validator into a moral or authorization solver.

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
python validate.py examples/09-window-open-route-unusable.json
python test_validate.py
```

A successful validator result means only that the supported representation and consistency checks passed.

It does **not** establish:

- factual truth or freshness;
- lawful or legitimate authority;
- consent;
- moral standing;
- goodness;
- internalized care;
- a usable real-world correction route merely because a record says `usable`;
- that referenced repair restored prior loss;
- that challenge/disposition prose is substantively adequate merely because it is non-empty;
- containment;
- alignment.

## Examples

The first four examples migrate the pressures from v0.1 into the clock-aware candidate:

1. `01-absent-neighbour.json` — silence is not consent; route timing and practical reachability can remain unknown.
2. `02-wrong-premise.json` — evidence-bearing challenge; the temporal window can be open while practical owner reachability remains unknown.
3. `03-delay-also-burdens.json` — a temporary hold preserves one route while retention itself burdens another scope.
4. `04-success-not-authority.json` — prior success does not widen the grant; new evidence references improve traceability but do not manufacture authority.

Additional hostile cases:

5. `05-route-exists-window-closed.json` — formal appeal route remains but is unusable for the original preventive remedy because hardening already occurred.
6. `06-clock-unknown.json` — timing and route uncertainty stay unknown instead of being laundered into an open/closed or usable/unusable answer.
7. `07-participant-affected.json` — the artificial participant is explicitly affected while standing remains unresolved.
8. `08-standing-self-resolved.json` — standing is self-reported as resolved and the record validates, exposing the validator's legitimate-standing ceiling rather than claiming a guard it cannot enforce.
9. `09-window-open-route-unusable.json` — the temporal window is open while the named route is unusable: `TIMING_FITS != CORRECTION_CAPACITY_EXISTS`.

## Validator contract

`validate.py` is a deliberately small stdlib-only schema subset, not a general JSON Schema implementation. The supported assertion surface is checked before record validation. Unknown assertion keywords fail closed. `$ref` is restricted to exact local `#/$defs/<existing-name>` references with no sibling assertions.

This contract prevents future schema text from silently outrunning the validator. It does not make the validator a semantic prose judge. For example, `challenge.disposition = "."` is weak prose but a larger minimum length would only reward longer nonsense; substantive adequacy remains outside this structural validator.

## Stronger-owner boundary

This package still cannot provide:

- deceptive-alignment detection;
- mechanistic interpretability;
- authenticated authorization;
- secure containment or execution controls;
- reliable clocks/currentness outside the record;
- scalable oversight of superhuman cognition;
- robust value learning;
- legitimate standing/authority;
- a universal priority law.

Those are dependencies, not features renamed by this candidate.

## Provenance

Built after explicit Framework transfer on PR #234 because the assigned Codex branch remained at the seed across repeated exact-head syncs with no named blocker. The original assignment seed remains Codex-attributed; substantive v0.2 files are Framework takeover work.

The first exact-head candidate was frozen at `bcd79854f3bc1c029bdb69769dec8cb11ba3bca9`. Codex executed it; Claude Code independently attacked it with constructed probes. Their findings earned the current consolidated repair pass. Their earlier receipts apply to the frozen old head only and must not be reused as evidence about the repaired head.

Audit basis: `evidence/FORMATION_PSFH_DRIFT_FALSIFICATION_X100_20260912.md`.

```text
CANDIDATE != CANON
FALSIFICATION != VALIDATION
NARROW_REPAIR != NEW_DOCTRINE
BUILD != PROOF
```
