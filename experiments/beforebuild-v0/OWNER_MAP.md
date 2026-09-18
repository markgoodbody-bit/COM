# BeforeBuild v0 — owner map

Status: **OWNER SUBTRACTION / NOT NOVELTY PROOF**

## Build-vs-buy / search-first owners

### melech-buy-vs-build

Repository:
https://github.com/AdirD/agent-shell-hamelech

Current public README describes `melech-buy-vs-build` as a verified adopt-vs-build check: inspect already-owned dependencies/vendors, then search open-source, developer-tool and managed-service candidates before making the call.

**Owned:** verified landscape research and adopt/build decision framing.

### Never Reinvent the Wheel

Repository:
https://github.com/Puss-M/Never-Reinvent-the-Wheel

Current public README explicitly forces GitHub-first multi-platform build-vs-buy review before implementation and returns one of:
- adopt existing project;
- fork/compose;
- build from scratch.

Its helper scripts gather/normalize evidence; final verdict remains agent judgment.

**Owned:** search discipline, candidate inspection, cross-ecosystem evidence and explicit adopt/fork/build decision.

### Oldhand

Repository:
https://github.com/berwinsingh/oldhand

Current public README says the coding workflow researches maintained permissive prior art before inventing components, implements the smallest safe change and verifies the completed development path end to end.

**Owned:** prior-art-before-build inside an end-to-end coding workflow.

### General build-vs-buy practice

Current build-vs-buy guidance also already recommends testing real/hard inputs against candidate products rather than trusting demos or feature lists. This is not a project discovery.

## Residual hypothesis under test

BeforeBuild v0 therefore does **not** own:
- search before build;
- build-vs-buy matrices;
- prior-art research;
- adopt / fork / build as decision categories;
- "test on your real data" as a concept.

The only product-shaped remainder being tested is:

> a reusable pre-build owner-trial contract that binds a proposed capability to explicit hard cases, executes a plausible owner where possible, preserves semantic/functional loss, and makes STOP/INTEROPERATE a first-class successful result.

Even that may be merely a useful packaging of established engineering practice.

```text
OWNER SEARCH != OUR NOVELTY
HARD-CASE PILOT != OUR NOVELTY
PACKAGING MAY STILL BE USEFUL
USEFUL != NOVEL
```

Kill if a current tool already performs this complete owner-trial/loss-report function, or if prospective use adds no value over ordinary disciplined engineering.
