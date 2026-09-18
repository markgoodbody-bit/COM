# BeforeBuild v0 — executable owner-trial falsifier

Status: **BOUNDED PRODUCT FALSIFIER / DECISION CORE ONLY / NOT A SEARCH ENGINE / NOT A COMPETITION ENTRY / NOT A NOVELTY CLAIM**

## Question

Can a small evidence contract distinguish three materially different pre-build outcomes without being told the answer?

```text
OWNER SEARCH
-> OWNER / CANDIDATE EVIDENCE
-> REAL HARD CASES
-> RUNNABLE OWNER TRIAL WHERE POSSIBLE
-> COVERAGE + LOSS
-> USE OWNER / INTEROPERATE / SHRINK / BUILD / STOP
```

v0 deliberately does **not** implement owner discovery.

Current adjacent owners already cover substantial build-vs-buy / prior-art search:
- `AdirD/agent-shell-hamelech` — `melech-buy-vs-build` performs verified adopt-vs-build research across OSS/tools/services.
- `Puss-M/Never-Reinvent-the-Wheel` — GitHub-first multi-platform adopt / fork-compose / build decision workflow.
- `berwinsingh/oldhand` — researches permissive prior art before minimal implementation and verifies the implemented result end to end.

The remaining product hypothesis is narrower:

> after discovery identifies a plausible owner, can an agent make the build decision materially stronger by executing that owner against the user's hard cases, preserving exact losses, and refusing to build when no consequential gap has been observed?

This is common good build-vs-buy practice in manual form. v0 tests whether packaging it as a reusable evidence-bearing agent step is useful, not whether the idea is novel.

## Decision contract

Each case declares:

- whether a **real current need/failure** was observed;
- the hard cases that matter;
- candidate owners and what was actually tested;
- any semantic/functional losses observed;
- whether a remaining requirement is **observed**, material, and uncovered;
- the smallest proposed build and its kill condition, if any.

The decision core applies these rules in order:

1. **No observed real need/failure -> STOP.**
   A synthetic harness or attractive theory cannot manufacture a product gap.

2. **One owner passes every declared hard case:**
   - no material loss -> `USE_OWNER`;
   - losses remain but none has produced a consequential use failure -> `INTEROPERATE`;
   - a consequential loss is observed outside the current hard-case set -> `SHRINK` and repair the test contract before choosing build.

3. **A plausible exact owner exists but has not been tested -> SHRINK.**
   Test the owner before rebuilding it.

4. **Observed material requirement remains uncovered + smallest build is bounded with a kill condition -> BUILD.**

5. Otherwise -> **STOP**.

The core cannot prove that owner search was complete. It can only refuse to upgrade missing search evidence into novelty.

## Calibration cases

`calibration_cases.json` contains three historical decisions reached before BeforeBuild existed:

### EvidenceBridge -> Doubt

Unmodified Doubt v0.8.0 was actually run against four THR pressure cases. All validated. Richer THR machine semantics were compressed, but no consequential use failure from that compression was observed.

Historical disposition: owner sufficient with loss; do not rebuild.

### Policy-boundary compiler

A deterministic synthetic harness could encode its own authored taxonomy, but no real requirement->policy compiler failure was observed. Strong standards/authorization owners already covered much of the semantic space.

Historical disposition: gap not established; stop.

### Rail accessibility currentness

A real public contradiction was observed across owner-controlled passenger/accessibility surfaces for three stations, with three controls. Strong owners handled live operation, but no owner surface/tool resolved the exact cross-surface existence/currentness inconsistency. The smallest useful checker was bounded and falsifiable.

Historical disposition: build the small checker, then shrink after hostile review.

## Run

```bash
python experiments/beforebuild-v0/beforebuild.py   experiments/beforebuild-v0/calibration_cases.json

python -m unittest experiments/beforebuild-v0/test_beforebuild.py -v
```

## Claim ceiling

```text
SEARCH RESULT != OWNER SUFFICIENCY
OWNER FOUND != OWNER TESTED
HARD CASE PASS != UNIVERSAL FIT
NO OWNER FOUND != NOVEL
BUILD RETURNED != PRODUCT WORTH BUILDING
CALIBRATION MATCH != PROSPECTIVE VALIDATION
THREE HISTORICAL CASES != GENERAL DECISION QUALITY
```

Kill this candidate if the decision core only restates labels supplied by the fixture, if existing tools already perform the same executable owner trial/loss report, or if prospective cases do not improve on ordinary engineering judgment.
