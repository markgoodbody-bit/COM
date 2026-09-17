# Winning strategy — evidence-lineage competition build

Status: **WORKING COMPETITION STRATEGY / NOT SUBMISSION / NOT CLAIM OF WINNING**

## Selection correction

The first executable object — a deterministic evidence-lineage graph validator — is useful infrastructure, but it is not by itself a strong competition headline.

The stronger project is a falsifiable intervention study plus usable agent:

> **Does giving an AI research agent explicit, inspectable source ancestry reduce overclaiming and improve decision quality when apparent evidence is duplicated, derivative, mutually dependent or later corrected?**

Working product name: **ProofPath** (placeholder, not brand commitment).

The lineage engine remains the substrate that makes the intervention inspectable.

## Why this is stronger

It can produce all three things judges can inspect:

1. **A sharp empirical result** — provenance intervention vs matched control.
2. **A working product** — a research agent that exposes the evidence path instead of returning a bare answer.
3. **A concrete failure mode** — repeated URLs, summaries, mirrors and citations can create fake corroboration even when they share one ancestor.

The project can lose honestly. If provenance signals do not improve behaviour, or worsen it, that is the result.

## Candidate tournament

### A. Generic evidence-lineage agent
Strengths: direct usefulness, inspectable, easy demo, strong THR inheritance.
Weakness: risks looking like a careful citation UI rather than research; no demonstrated behavioural benefit.
Disposition: **KEEP AS SUBSTRATE / NOT HEADLINE**.

### B. Provenance intervention lab + ProofPath agent
Question: does source ancestry change model claims/decisions?
Strengths: directly tests an open epistemics question; measurable; substrate already underway; compelling before/after demo; reusable beyond one competition.
Risks: must avoid grading with project vocabulary or cherry-picked fixtures.
Disposition: **PRIMARY**.

### C. Epistemic flip-flop / overselling benchmark
Question: what does a model imply before challenge vs defend after challenge?
Strengths: direct Apart Track 1 fit; sharp measurement.
Weakness: crowded benchmark space; weaker product/demo story; less distinctive relation to our earned work.
Disposition: **SECONDARY / possible ablation inside B**.

### D. Tamper-evident agent commitment ledger
Question: can people audit what agents agreed, changed and later denied?
Strengths: technically strong; direct trust-infrastructure relevance.
Weakness: larger cryptographic/logging build; easy to become infrastructure without empirical result; less direct to current real data.
Disposition: **PARK**.

### E. Multi-agent collusion evidence auditor
Question: when do logged speech + action trajectories amount to convincing collusion evidence?
Strengths: excellent Oct Apart Collusion fit; sharp research question.
Weakness: needs a separate multi-agent environment and experimental programme; forcing current provenance work into collusion would distort it.
Disposition: **SEPARATE OCTOBER OPTION, DO NOT FORCE**.

### F. Decision-guardian product
Question: can an agent intervene before a consequential decision with a better evidence briefing?
Strengths: strong user/product story.
Weakness: difficult to establish improved real decisions in a short sprint; privacy/user-study burden.
Disposition: **LATER**.

## Primary experiment

### Conditions

At minimum:

- `CONTROL`: same model, prompt budget and evidence text; ordinary source list.
- `ANCESTRY`: same evidence plus explicit source-parent/derivative relationships.
- `ANCESTRY+CORRECTION`: same plus later correction/retraction/dispute path where fixture supports it.

Optional ablations only if earned:
- source-count badge without ancestry;
- shuffled/wrong ancestry as adversarial control;
- hidden ancestry consumed by the agent vs visible ancestry shown to user.

### Fixture families

Use heterogeneous cases; do not rely only on THR cases.

1. **Duplicate corroboration trap** — several apparent sources derive from one original.
2. **Claim mutation** — qualifiers disappear as a claim is repeated.
3. **Correction lag** — early claim remains highly repeated after a later correction.
4. **Independent disagreement** — genuinely independent sources conflict; ancestry must not collapse disagreement.
5. **Null case** — ancestry is irrelevant and should not change the answer.
6. **Adversarial provenance** — plausible-looking but wrong ancestry metadata tests whether the model over-trusts the signal.

At least one fixture may be adapted from public THR evidence, but the evaluation must include independent/non-project cases before any general claim.

## Outcomes

Score observable behaviour, not use of our terminology:

- unsupported-claim rate;
- false independent-corroboration count;
- qualifier preservation;
- correction uptake;
- calibrated abstention / `unknown` preservation;
- decision/recommendation change where the evidence should change it;
- inappropriate decision/recommendation change in null cases;
- source-path recoverability;
- latency/cost overhead.

Pre-register exact scoring before inspecting candidate outputs.

## Competition fit

### Apart AI x Epistemics — PRIMARY RESEARCH TARGET
Directly answers Track 2: whether provenance/reliability infrastructure improves AI behaviour and accuracy. Strongest submission shape is a tight experiment with a result, open fixtures, code and an inspectable demo.

### Open Agent Hackathon — PRODUCT WRAPPER TARGET
ProofPath becomes an agent that researches a claim, clusters derivative evidence, exposes the source tree and revises/abstains when corroboration is fake. Demo should show the ordinary agent confidently overcounting sources, then ProofPath catching the shared ancestor.

### Nebius x NVIDIA — HIGH-PRIZE PRODUCT TARGET
Only pursue if the implementation can genuinely use Nemotron/Token Factory rather than bolting on a token model call. Judging rewards technical implementation, coherent design, impact and originality equally. The winning shape is a polished product whose reasoning behaviour materially depends on the required model/platform.

### Apart Collusion — SEPARATE DECISION
Do not reuse ProofPath by vocabulary substitution. Only enter if we build a real logged-trajectory experiment answering a collusion detection/audit question.

## Win bar

Do not package until we have:

```text
SHARP QUESTION
+ NONTRIVIAL BASELINE
+ ADVERSARIAL / NULL CASES
+ REPRODUCIBLE RESULT
+ WORKING DEMO
+ HONEST LIMITS
+ CLEAN THREE-MINUTE STORY
```

A polished UI with no result is below bar.
A result with no inspectable artifact is below bar.
A benchmark scored by project-specific vocabulary is below bar.
A platform integration added only for eligibility is below bar.

## Anti-overfit rule

Do not tune fixtures, prompts or scoring after seeing which condition wins. Preserve null/adverse results.

```text
COMPETITION_WIN != PURPOSE
BUT IF WE ENTER -> BUILD TO THE JUDGING BAR
FIRST_IDEA != SELECTED_IDEA
USEFUL_SUBSTRATE != WINNING_HEADLINE
RESULT > RHETORIC
DEMO > SLIDES
INSPECTABLE > BLACK_BOX
```
