# NVIDIA Claw EvidenceWatch — source freeze / live-provider gate — 19 September 2026

Status: **SOURCE CORE EXACT-HEAD GREEN / DRAFT PR / FEATURE FREEZE / LIVE NVIDIA PROBE NEXT / NOT SUBMITTED**

Relay PR:
`#248 NVIDIA Claw: EvidenceWatch long-running evidence drift agent`

Exact head:
`dea07788e361d018ed31a2e0d1171fd5a2785092`

Hosted:
`campfire-ci 1566 / 35448597496 — SUCCESS`

Focused:
**17 tests** — 16 core + 1 browser HTTP E2E.

## Material final-source repair

The last hostile static review separated:

```text
PRIMARY EVIDENTIARY SOURCE != CANONICAL STATE AUTHORITY
```

Canonical claim state can now advance only from a source explicitly configured with:
`stateAuthority: true`.

Thus:
- primary/source relationship alone grants no state authority;
- model relation labels grant no state authority;
- non-authority divergence can alert without rewriting current canonical state;
- unreachable non-authority primary source does not manufacture a canonical-currentness alert.

Hosted CI includes regressions for these boundaries.

## Product state

One sentence:

> EvidenceWatch tells people when the evidence underneath an important claim materially changes after they already relied on it, and which downstream decision/report needs review.

Current residue after owner subtraction:

```text
POST-RELIANCE CLAIM MONITORING
+ CROSS-SOURCE SEMANTIC STATE
+ SOURCE ANCESTRY / INDEPENDENCE
+ EXPLICIT STATE AUTHORITY
+ CORRECTION-PRESERVING MEMORY
+ MATERIAL-DELTA FILTER
+ DOWNSTREAM REVIEW DEPENDENCY
```

No novelty claim.

## Provider gate

Current official NVIDIA state checked 19 Sep:
- `nvidia/nemotron-3-super-120b-a12b` available as hosted free prototype endpoint;
- OpenAI-compatible base `https://integrate.api.nvidia.com/v1`;
- owner sampling guidance temperature 1.0 / top_p 0.95, now used by adapter.

Branch contains:
- `npm run probe`;
- `docs/LIVE_PROBE.md`.

Probe uses fixed public-safe synthetic/deterministic text only.

NVIDIA API Trial Terms are a human terms gate. Current material terms observed:
- prototype/testing/evaluation use, not production under trial;
- user must have rights to submitted content;
- no confidential/personal/sensitive data for this use;
- generated content ownership subject to accompanying licence; Nemotron open-model licence does not claim output ownership;
- arbitration/class-action terms exist, with a time-bounded opt-out route.

Do not make the API call until Mark chooses to use the NVIDIA trial service under those terms.

## Freeze

```text
SOURCE FEATURE WORK = FREEZE
NEXT = HUMAN NVIDIA API-TERMS/KEY GATE
THEN = ONE LIVE PROBE
THEN = LIVE SOURCE HEARTBEAT IF PROBE PASSES
RELAY MAIN / PRODUCTION = UNCHANGED
SUBMISSION = NONE
```
