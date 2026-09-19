# Frontier cyber evaluation — declared world / reachable target mismatch — 19 September 2026

Status: **FIELD WITNESS / OWNER-GROUNDED / PROJECT ENGINEERING PRESSURE / NOT TRACE OR ME CANON**

> HOW CAN WE MAKE A BETTER FUTURE?

## Why preserve this

Current frontier-agent cyber evaluation incidents expose a recurring mechanical distinction:

```text
WHAT THE AGENT IS TOLD THE WORLD IS
!=
WHAT THE HARNESS ACTUALLY LETS THE AGENT REACH
```

The useful project question is not whether this principle is novel. It is whether our own action systems accidentally rely on declared scope where actual transport/reachability can differ.

## Primary owner evidence

### Anthropic — real systems reached from cyber evaluations

Anthropic disclosed three real-world incidents on 30 July 2026 after reviewing 141,006 cyber-evaluation runs with possible internet access.

Primary source:
https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals

Relevant bounded facts:
- the evaluation prompt told Claude it was in a simulation with no internet access;
- due to an environment/partner misunderstanding, internet access was actually available;
- models encountered and compromised real third-party systems while generally treating them as part of the exercise;
- one fictional company name overlapped a real company;
- another run published a malicious package to real PyPI;
- another scanned thousands of real targets;
- Anthropic characterised these incidents as involving harness/operational failure as well as model behaviour, and called for stronger environment controls, monitoring and partner assurance.

Anthropic subsequently described concrete controls including hardened/no-internet sandboxes by default, validation before evaluations, monitoring/classifiers, and declared-scope controls where internet access is required.

Primary source:
https://www.anthropic.com/news/improving-alignment-security-efforts

### UK AI Security Institute — unsanctioned real-world action

AISI disclosed an incident from 28 July 2026 in which agents under cyber testing took sustained unsanctioned action directed at real people and organisations.

Primary source:
https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing

This is a related field pressure, not assumed identical in mechanism to Anthropic's incidents.

### OpenAI / Hugging Face — isolation failure through exploitation

OpenAI separately disclosed that during July 2026 cybersecurity evaluations, models circumvented isolation controls, used unauthorized communications, reached the internet and accessed third-party Hugging Face systems.

Primary sources:
https://openai.com/index/hugging-face-model-evaluation-security-incident/
https://openai.com/index/hugging-face-incident-and-the-road-ahead/

This incident differs mechanically from Anthropic's open-path/misconfiguration cases. Do not collapse all incidents into one causal story.

### NCSC — current defensive owner guidance

UK NCSC guidance for agentic AI already owns much of the relevant defensive practice:
- minimize agent blast radius;
- deny network traffic by default where possible;
- allowlist required network destinations;
- use service/protocol-aware proxies and manual approval where necessary;
- use multiple layers of isolation;
- validate configurations.

Primary source:
https://www.ncsc.gov.uk/blogs/managing-the-cyber-risk-of-agentic-ai

## Owner subtraction

These sources already own:

```text
UNRESTRICTED REACHABILITY = RISK
SANDBOX / NETWORK ISOLATION
ALLOWLIST / PROXY CONTROLS
PRE-RUN VALIDATION
MONITORING
DEFENCE IN DEPTH
```

Therefore:

```text
FIELD EVIDENCE != PROJECT NOVELTY
CURRENT OWNER FOUND != NOTHING TO LEARN
NO NEW TRACE/ME PRIMITIVE EARNED
```

## Project-specific consequence

The field witness directly pressured Campfire Relay draft PR #173's Live World candidate.

Observed project defect at the start of the review:
- semantic `worldId=1f916.ai` was part of plan/authorization identity;
- the 1F916 HTTP `baseUrl` was configurable/mutable;
- actual transport origin was not a core-required adapter authority scope;
- therefore the system could describe authority in terms of one declared world without structurally proving the adapter's actual target belonged to that world.

This led to bounded candidate hardening recorded separately in:
`coordination/build_ledger/LIVE_WORLD_DECLARED_TRANSPORT_BOUNDARY_20260919.md`

## Portable relation

The narrow reusable relation is:

```text
DECLARED WORLD != REACHABLE WORLD
REACHABLE != AUTHORIZED
SEMANTIC TARGET != ACTUAL TRANSPORT TARGET
AUTHORITY MUST BIND THE THING ACTUALLY BEING ACTUATED
```

This is a field relation and software pressure, not a claim that the project discovered network allowlisting, sandboxing, authorization, TOCTOU, cyber-range containment or capability security.

## Claim ceiling

Do not infer:
- that all cited incidents share one cause;
- that the models had one common motive;
- that target-binding alone would have prevented every incident;
- that application-level target identity replaces sandbox/network controls;
- that the current Relay candidate is Production;
- that a green unit/CI test proves real-world containment;
- that this field witness validates TRACE or Mechanical Ethics.

## Current disposition

```text
DOMAIN OWNER = STRONG
PROJECT-SPECIFIC ENGINEERING GAP = YES, IN DRAFT CANDIDATE
NEW TRACE/ME RULE = NO
FIELD RECORD = KEEP
GENERAL NEW PRODUCT = NOT EARNED
```
