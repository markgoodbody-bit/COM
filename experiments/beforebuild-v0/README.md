# BeforeBuild v0.2 — executable owner-trial falsifier

Status: **BOUNDED PRODUCT FALSIFIER / OWNER-TRIAL DECISION CORE / NOT A SEARCH ENGINE / NOT A COMPETITION ENTRY / NOT A NOVELTY CLAIM**

## Question

Can a small evidence contract strengthen a pre-build decision by forcing a plausible owner to face the same hard cases before custom work is earned?

```text
OWNER DISCOVERY                    # use existing search/build-vs-buy owners
-> REAL-WORLD NEED EVIDENCE
-> EXPLICIT HARD CASES
-> RUN RELEVANT OWNER / CANDIDATE WHERE POSSIBLE
-> PASS / FAIL / NOT_TESTED + LOSS
-> USE_OWNER / INTEROPERATE / SHRINK / BUILD_PROBE / STOP
```

v0.2 deliberately does **not** implement owner discovery.

Current adjacent owners already cover much of search-first / build-vs-buy:
- `AdirD/agent-shell-hamelech` — `melech-buy-vs-build` performs verified adopt-vs-build research and records what no shortlisted option gives you.
- `Puss-M/Never-Reinvent-the-Wheel` — GitHub-first multi-platform adopt / fork-compose / build review with implementation-file inspection.
- `berwinsingh/oldhand` — researches permissive prior art before minimal implementation and verifies the delivered path end to end.

The candidate therefore shrinks to one possible reusable seam:

> **pre-build owner trial** — bind the proposed need to explicit hard cases, run a plausible owner/candidate against those cases where possible, preserve semantic/functional loss, and make STOP/INTEROPERATE first-class successful outcomes.

This is established good engineering practice in manual form. v0.2 tests whether a small explicit contract is useful and robust enough to automate; it does not claim the idea is new.

## Why v0.1 was repaired before promotion

The first branch version accepted authored booleans:
- `world_need.observed`;
- `uncovered_requirement.observed`.

Those fields had too much verdict power. An enthusiastic agent could set them and manufacture `BUILD`.

v0.2 removes both.

### World need is now derived from evidence kind

Each field observation must be typed and source-bound.

Qualifying current-world evidence:
- `reproduced_failure`;
- `owner_source_contradiction`;
- `current_user_need`.

Non-qualifying by itself:
- `synthetic_only`;
- `conceptual_only`.

The classifier derives whether a real need is observed.

### Uncovered need is now derived from trials

There is no `uncovered_requirement` boolean.

A build probe can be earned only when:
1. qualifying current-world evidence exists;
2. no tested relevant owner passes all hard cases;
3. no exact/near owner remains untested;
4. an **executed exact/near candidate fails at least one declared hard case**;
5. a smallest probe is bounded and has an explicit kill condition.

Even then the verdict is only:

```text
BUILD_PROBE
```

not `BUILD PRODUCT`.

This is deliberately conservative.

## Candidate relevance

Owner/candidate relevance is explicit:

- `exact` — claims essentially the same function;
- `near` — plausibly carries the function or the owner system whose failure defines the gap;
- `adjacent` — informative but not sufficient to block a probe.

An untested `exact` or `near` candidate forces `SHRINK`: test it before custom work.

## Owner-trial rules

For an executed relevant candidate:

- passes every hard case, no material loss -> `USE_OWNER`;
- passes every hard case, visible losses but no consequential failure from those losses -> `INTEROPERATE`;
- passes current hard cases but a consequential loss is observed -> `SHRINK` because the acceptance set is incomplete;
- fails one or more hard cases -> may support `BUILD_PROBE`, but only with qualifying world evidence and a bounded falsifiable probe.

A failed **adjacent** tool does not earn a build.

## Historical calibration

`calibration_cases.json` contains no expected-verdict field.

### EvidenceBridge -> Doubt

Unmodified Doubt v0.8.0 was actually run against four THR pressure cases. All passed. Richer THR machine semantics were compressed, but no consequential use failure from that compression was observed.

Historical result should derive: `INTEROPERATE`.

### Policy-boundary compiler

Only a synthetic authored compiler/harness demonstrated the distinction. No real requirement->policy failure causing a material wrong outcome was observed.

Historical result should derive: `STOP`.

### Rail accessibility currentness

Three current owner-surface contradictions were observed with three controls. The owner system itself failed the contradiction hard cases; no current owner tool found in the bounded pass exposed the exact cross-surface consistency failure. A tiny checker with a kill condition was available.

Historical pre-build result should derive: `BUILD_PROBE`.

The later checker was hostile-reviewed and shrunk; that later success is not input to the pre-build calibration.

## Run

```bash
python experiments/beforebuild-v0/beforebuild.py \
  experiments/beforebuild-v0/calibration_cases.json

python -m unittest experiments/beforebuild-v0/test_beforebuild.py -v
```

## Claim ceiling

```text
SEARCH RESULT != OWNER SUFFICIENCY
OWNER FOUND != OWNER TESTED
HARD CASE PASS != UNIVERSAL FIT
NO OWNER FOUND != NOVEL
TYPED EVIDENCE != VERIFIED EVIDENCE
BUILD_PROBE != PRODUCT EARNED
CALIBRATION MATCH != PROSPECTIVE VALIDATION
THREE HISTORICAL CASES != GENERAL DECISION QUALITY
```

Kill this candidate if:
- existing tools already perform the same reusable pre-build owner trial/loss report;
- prospective use adds no value over ordinary disciplined engineering;
- evidence typing becomes another way for the deciding agent to encode its desired verdict;
- owner adapters are so bespoke that the "reusable" layer disappears;
- the tool becomes generic competitive-research prose with a CLI.
