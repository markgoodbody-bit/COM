# NVIDIA Claw public-stack preflight and candidate seam — 19 September 2026

Status: **PUBLIC COMPATIBILITY PREFLIGHT / OWNER-SUBTRACTED CANDIDATE SEAM / NO SUBMISSION BUILD YET**

Direct Mark direction:
`go for it / COMSYNC and proceed`.

## Event gate

From the live NVIDIA/Luma page supplied by Mark:
- Claw Agent Challenge: London;
- fully remote;
- open to anyone living in the UK;
- no team requirement;
- registration closes 3 Oct 2026 07:59 BST;
- full challenge/submission details appear only after registration.

```text
REGISTER -> GET FULL BRIEF -> RULES/OWNER CHECK -> CHOOSE AGENT -> BUILD
```

Do not infer hidden judging criteria.

## Public NVIDIA stack reconnaissance

Current public NVIDIA material establishes:

### NemoClaw / OpenShell
NemoClaw is an open-source reference stack for running supported agents (including OpenClaw, Hermes and LangChain Deep Agents) inside OpenShell sandboxes with:
- managed inference;
- network policy;
- lifecycle operations;
- persistent workspace state;
- snapshot / restore;
- recovery;
- credential custody;
- operator-controlled egress.

### Windows path
NVIDIA documents Windows x86-64 via **WSL2**, not native Windows execution.

Current documented baseline:
- Windows 10 build 19041+ or Windows 11;
- WSL2;
- Docker Desktop WSL backend or qualified rootless Podman path;
- generic minimum about 4 vCPU, 8 GB RAM, 20 GB disk;
- local GPU inference is optional because onboarding supports provider/model selection.

Therefore no public hardware blocker is established for an ordinary Windows development machine, subject to actual host preflight.

## Strong-owner subtraction

Do not pitch these as project inventions:

### Persistent memory / maintained state
NVIDIA community already has a memory-driven Chief-of-Staff example with:
- versioned schema;
- maintained indexes;
- decay / stale-data handling;
- append-only correction log;
- scheduled repair and re-judgment;
- replay-idempotent ingestion.

### Monitoring / scheduled work
NVIDIA community already has scheduled cited monitoring, persistent deduplication and long-running worker examples.

### Runtime retries / reconciliation
Current NemoClaw work explicitly includes:
- durable pending journal before external side effects;
- reconciliation required after timeout/crash/ambiguous mutation;
- retry distinctions;
- exact identity-bound cleanup;
- lifecycle recovery;
- exact-candidate evidence checks.

### Snapshot / rebuild / restore
NemoClaw already owns manifest-defined state preservation, rebuild and snapshot/restore semantics.

```text
GENERIC MEMORY != OUR GAP
GENERIC RETRY != OUR GAP
GENERIC SNAPSHOT/RECOVERY != OUR GAP
GENERIC LONG-RUNNING AGENT != OUR GAP
```

## Candidate application seam that survives public subtraction

Not observed as an exact public NVIDIA example:

> a long-running **continuity steward** for a real multi-repository human/AI project where each model/runtime session is episodic and must reacquire current state without pretending continuous identity.

Candidate functions:

1. **Live-source reacquisition**
   - fetch current repository / issue / build / external owner state;
   - reject known-stale pointers.

2. **Role continuity without runtime-identity fiction**
   - distinguish role, aperture/session, human authority, repository source, and current task;
   - no claim that a successor agent "remembers" the predecessor.

3. **Gate / authority continuity**
   - preserve what remains human-gated;
   - capability does not silently become authority.

4. **Currentness / stale-state detection**
   - mark pointers as fresh / stale / unobserved;
   - later source beats cached summary.

5. **Correction-preserving ledger**
   - do not overwrite prior state as if it never existed;
   - retain why current routing changed.

6. **Compact handoff**
   - maintain a bounded hot state;
   - detail/history remains externally recoverable;
   - prevent the continuity layer itself from growing into replay burden.

7. **Optional bounded actions only if the registered challenge permits**
   - use NVIDIA/OpenShell policy and runtime controls rather than reimplementing sandbox/egress/security;
   - application-level action receipts only where product semantics require them.

Possible working name:
`Continuity Steward` / `Project Steward`.

This is a product/use-case hypothesis, **not a novelty claim**.

## Why useful even without prize

The current project has repeatedly experienced the target problem:
- short chat/runtime windows;
- successor apertures;
- stale mutable pointers;
- duplicate work risk;
- human gates;
- continuity surface bloat;
- need to reacquire before acting.

A NemoClaw implementation could be useful as a local/project-side steward if the challenge rules allow it.

## Kill / route conditions after registration

Kill or substantially revise this candidate if the hidden brief:
- specifies a domain where this is irrelevant;
- requires a different stack/product class;
- judges primarily on a user outcome this candidate does not serve;
- forbids existing-project inheritance or requires all code during challenge;
- requires a specific OpenClaw/NemoClaw architecture incompatible with the design;
- reveals an NVIDIA reference example already solving the same project-continuity seam;
- imposes licensing/public-repository requirements we do not want to accept.

## Build gate

```text
PUBLIC FIT = STRONG
PUBLIC STACK COMPATIBILITY = PLAUSIBLE
CANDIDATE PRODUCT SEAM = SURVIVES BOUNDED OWNER SUBTRACTION
NOVELTY = NOT CLAIMED
REGISTRATION = STILL HUMAN/UI GATE
FULL BRIEF = REQUIRED BEFORE CODE BUILD
```

Next after registration:
1. preserve exact challenge text / rules / deadline / judging;
2. map requirements against this candidate;
3. OWNER FOUND / NO DELTA / PIVOT / BUILD;
4. if BUILD, create the smallest end-to-end NemoClaw-compatible vertical slice first.
