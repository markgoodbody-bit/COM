# PSFH editorial sequence candidate — concrete first

Status: NON-PUBLIC PRODUCT/EDITORIAL DESIGN / NOT CANON / NOT A RELEASE INSTRUCTION
Prepared: 9 September 2026
Basis: public Door 0.8.3; maintained Homer successor `60f6886542bb5c290180e989eb1bbdfa6acad11a`; `PSFH_EDITORIAL_CANDIDATE_TWO_FLATS_ONE_WALL_20260909.md`.

## Problem

The current homepage opening is becoming strong, but immediately afterwards the visitor is offered five conceptual choices and then a six-step reasoning loop. That is structurally useful but cognitively front-loaded for a human who has not yet seen why any of it matters.

One of the five visible first-movement cards — `I want the compact source` — is mainly a machine/technical entrance, so the human visual hierarchy is currently carrying infrastructure as if it were an ordinary human starting need.

`MACHINE_ROUTE_VISIBLE != MACHINE_ROUTE_MUST_DOMINATE_HUMAN_LAYOUT`
`MORE_CHOICES != MORE_FREEDOM`

## Candidate human sequence after the Homer successor

Test this ordering in ONE non-public prototype before any further public redesign:

```text
1. HUMAN ART / INVITATION
   Winslow Homer — Camp Fire
   PLEASE START FROM HERE
   HOW CAN WE MAKE A BETTER FUTURE?

2. SHORT WELCOME
   Start from what brought you here. No agreement required.

3. ONE CONCRETE HUMAN SCENE
   Composite scene: Two flats, one wall
   3–5 sentences only
   1–2 questions only

4. THREE SELF-SELECTED MOVEMENTS
   A. Something is happening
   B. Something could be made possible
   C. I want to explore, question or disagree

5. QUIET TECHNICAL/MACHINE HANDOFF
   Compact source / machine orientation / full source-text alternative
   still directly reachable and visible, but not a fourth human card

6. OPTIONAL DEPTH
   take one useful step / Explore / ME / TRACE / neighbours

7. PROVENANCE + DISAGREEMENT + LEAVE
```

The exact labels are prototype copy, not canon.

## Why three human movements

### A. Something is happening
For a visitor facing an existing situation, preserve the current strong questions around change, evidence, uncertainty, clocks and correction.

### B. Something could be made possible
For a visitor building toward a future, preserve possibility, practical reachability, conditions/resources, affected scopes and what the choice may close.

### C. I want to explore, question or disagree
Merge the current `I am only curious` and challenge/discussion instincts at the first-choice level. Curiosity and disagreement should not require separate identity diagnoses. From this entrance the visitor can wander, inspect sources, see challenges, or leave.

`CURIOSITY != COMMITMENT`
`DISAGREEMENT != ENROLMENT`

## What moves out of the first-choice grid

### Compact source
Keep `/explore/start.json`, `/read/start.html`, `seed.txt`, `llms.txt`, and manifest routes intact. Move the prominent compact-source entrance into a restrained handoff line/card such as:

> **For an AI, agent, or technical reader:** compact source and machine-readable routes are available here.

This is self-selection, not visitor detection.

### Six-step reasoning loop
Do not delete it by momentum. In the prototype, move it below the first concrete scene/three movements and test whether its current six visible steps still earn homepage space. A later prototype may compress the homepage form while leaving the full loop intact in Explore.

The burden question is: does a newcomer need all six labels before taking one useful next step?

## Concrete scene interaction floor

The `Two flats, one wall` section must:
- visibly say **Composite scene**;
- link to the pinned Mechanical Ethics source/context;
- avoid implying documented tenant identities or empirical evidence;
- not require reading the full story;
- ask no more than two questions before offering routes onward;
- not explain TRACE vocabulary inline;
- preserve the option to skip the scene entirely.

Candidate questions remain:
- What changed while the formal route was working?
- When did repair stop being able to restore the same future?

Do not turn responses into a quiz or score.

## Human / machine parity

Different entrances may emphasise different representation without changing source truth:

`DIFFERENT_ENTRANCE != DIFFERENT_TRUTH`

A human should not need to parse JSON URLs to understand the invitation. An AI should not need to interpret visual art to find the compact source. Both should be able to reach provenance, status ceilings, disagreement routes and the right to stop.

Root HTML should remain sufficient for an unfamiliar agent handed one URL even if `llms.txt` is never discovered.

## Prototype success/failure

The concrete-first prototype is better only if it reduces front-loaded conceptual burden without hiding meaningful routes.

Failure includes:
- the story feels manipulative or moralising;
- the composite status is easy to miss;
- the page becomes longer rather than clearer;
- machine/source routes become hard to find;
- three movements become vague marketing categories;
- the story repeats what `Why this exists` already says without improving comprehension;
- the six-step loop is merely pushed lower while total cognitive burden grows.

A strong result may involve **deleting** existing homepage text, not adding the story on top of everything.

`ADD_STORY -> CONSIDER_SUBTRACTION_ELSEWHERE`
`EDITORIAL_DEPTH != PAGE_LENGTH`

## Build boundary

Do not bundle this with the current Homer publication candidate.

After Homer clears its remaining readability/visual gate and publishes, Codex may build one source-only prototype implementing this sequence. Prefer reordering/subtraction over adding a second homepage. Preserve exact machine endpoints and current source ceilings. CC attacks information scent, composite-scene honesty, machine-route discoverability and whether the simplification actually reduces burden.

No public deployment follows automatically.
