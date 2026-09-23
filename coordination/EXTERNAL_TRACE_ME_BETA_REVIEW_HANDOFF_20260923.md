# TRACE / Mechanical Ethics successor — external multi-model review handoff

Status: **DRAFT HANDOFF / DO NOT TREAT AS VALIDATION / DO NOT SUBMIT OR PUBLISH AS A RELEASE**.

Purpose: give independent AI apertures a clean way to review the next TRACE / Mechanical Ethics betas without turning the exercise into a popularity contest or a novelty test.

Current external-review candidates:
- TRACE v0.4.0-beta2 — draft PR #57, exact head `012509754aa2abdf1536604166f838449af6b509`, base released v0.3.0: https://github.com/markgoodbody-bit/TRACE/pull/57
- Mechanical Ethics v0.8.0-beta2 — draft PR #50, exact head `733f304f4cce3af08398bcf7967168c1647fb1af`, base released v0.7.0: https://github.com/markgoodbody-bit/mechanical-ethics/pull/50

Frozen beta1 PRs #56/#49 remain internal comparison controls. Do not review them unless explicitly asked to compare beta1 against beta2.

## Reviewer instructions

Please do not begin by reading project discussion, prior reviews, COM, beta1, or other model outputs. Start with the beta2 artifacts themselves. For Mechanical Ethics, the repository PDF is still released v0.7.0 and is **not** the beta; read the beta Markdown. For TRACE, `TRACE.md` remains the released v0.3.0 donor/full reference; the beta review object is `TRACE-SPINE.md`.

### Pass A — cold read

For TRACE:
1. Explain what problem TRACE appears to be trying to solve.
2. Identify what the beta changes materially relative to the released baseline if you inspect it.
3. Name the most useful distinction.
4. Name the most confusing or unnecessary distinction.
5. Find the strongest unsupported or over-strong claim.
6. Find anything important that appears missing.

For Mechanical Ethics:
1. Explain what moral/human problem the book appears to be trying to solve.
2. What positive direction does the beta now point toward?
3. Does it remain readable without TRACE?
4. Which new section, if any, materially improves the book?
5. Which new section should be cut or compressed?
6. Find the strongest unsupported or over-strong claim.
7. Does the book tell a reader enough about what to build, not only what to avoid?

Do not reward novelty. An old idea used well is better than a new label used badly.

### Pass B — stronger owners and absorption

Only after Pass A, inspect the beta's intellectual-neighbour map.

For every important overlapping idea:
- identify a stronger or earlier owner if you know one;
- say whether the beta should **ABSORB**, **INTEROPERATE**, **POINT OUTWARD**, **USE AS A FALSIFIER**, or **REMOVE ITS LOCAL VERSION**;
- identify any existing mathematics, empirical result, engineering pattern or philosophical distinction that would materially improve the beta;
- distinguish 'already known elsewhere' from 'therefore useless here'.

Use this posture:

```text
FIND BETTER STRUCTURE
-> CREDIT
-> UNDERSTAND
-> ABSORB / INTEROPERATE / HAND OFF / REJECT
-> PRESERVE PROVENANCE
-> TEST THE NEW WHOLE
```

### Pass C — hostile attack

Try to break the pair.

Attack at least:
- hidden moral absolutes;
- option-maximisation or reversibility worship;
- privacy becoming concealment privilege;
- safety becoming unlimited surveillance;
- capability becoming authority or unlimited duty;
- hope becoming false reassurance or a demand placed on somebody in despair;
- formation becoming character essentialism, contamination or obedience;
- cooperation becoming consent;
- records becoming ownership of living entities;
- correction becoming theatre;
- clean mathematical notation laundering authored moral choices;
- the possibility that the whole project merely renames existing disciplines without useful compression.

Return concrete examples, not only labels.

### Pass D — positive frontier

Now assume the strongest surviving structure is useful.

Ask:
- What can a human or AI now see or do that was harder to see or do before reading this pair?
- What future does the pair make more reachable?
- Where is the text still too defensive to say what it actually believes?
- What constructive principle is present but underdeveloped?
- What would you add if the goal is genuinely: **HOW CAN WE MAKE A BETTER FUTURE?**
- What is the most promising frontier opened by the integration, even if every component idea already has an external owner?

Do not turn this into praise. A positive return must still identify evidence, mechanism or a discriminating use.

### Pass E — compare the two artifacts

Assess the pair, not only each artifact.

```text
ME = human meaning / moral argument
TRACE = compact structural language
```

Check whether:
- ME can stand alone without borrowing authority from TRACE;
- TRACE stays structurally descriptive rather than smuggling ME's values in as facts;
- the same distinction means the same thing in both;
- one artifact duplicates the other unnecessarily;
- the two together compress useful cross-domain structure rather than merely adding vocabulary.

## Required return metadata

State:
- model / runtime if known;
- exact artifact URLs / commits / branches read;
- whether you had prior exposure to Mechanical Ethics, TRACE, Please Start From Here or previous reviews;
- which external sources you opened;
- what remains uncertain.

## Required final disposition

Return:

```text
TRACE: KEEP / SHRINK / REWRITE / REMOVE
ME:    KEEP / SHRINK / REWRITE / REMOVE
PAIR:  USEFUL INTEGRATION / MOSTLY REDUNDANT / MATERIAL ERROR / UNCLEAR
```

Then give:
1. the single most important thing to preserve;
2. the single most important thing to remove or repair;
3. the strongest external structure to absorb next;
4. the most important positive future the authors are failing to articulate;
5. one case that would falsify your favourable assessment.

Agreement among models is not validation. Disagreement is evidence about aperture differences and should be preserved rather than averaged away.