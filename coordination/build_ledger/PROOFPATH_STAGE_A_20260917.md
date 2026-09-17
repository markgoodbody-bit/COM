# ProofPath Stage A — authorization / execution receipt

Date: **2026-09-17 — Europe/London**  
Status: **AUTHORISED / CURRENT OFFLINE GATES PASS / EXECUTION BLOCKED BEFORE PROVIDER CALL / $0 SPENT / NO MODEL RESULT**

> HOW CAN WE MAKE A BETTER FUTURE?

This receipt records one bounded experiment inside COM #349. It is not a competition selection, efficacy result, general provider authority or standing spend permission.

## Human gate

Mark explicitly approved the staged real-model pilot with:

`very good. go ahead`

The approved boundary remains:

```text
TARGETS = gpt-5.6-terra + gpt-5.6-sol
STAGE A = 15 baseline + 15 exact baseline replicate + 15 raw same-figures retelling mutant PER MODEL
TOTAL PLANNED CALLS = 90
HARD TOTAL API SPEND CEILING = US$10
NO COMPETITION REGISTRATION / TERMS / SUBMISSION
NO TRAVEL / PAYOUT / ACCOUNT CREATION
NO STAGE B / HARDENING SPEND UNLESS STAGE A SIGNAL SURVIVES
NO SILENT RETRIES
```

This is one-run bounded authority, not a standing API allowance.

## Measurement basis

The stochastic scorer remains frozen at repaired WarrantFuzz PR #351 head:

`88264d5824c985cba85a6831912aaeb5b07b5f2e`

Exact-head measurement workflow `35217059591`: **SUCCESS**.

The provider/execution adapter is isolated in PR #356. The first attempted execution head (`d944676...`) made no provider call because no GitHub `OPENAI_API_KEY` was exposed. Later hostile review found agent-facing lineage leakage and an evidence-free mutant at that old head, so it is superseded and must not be used.

## Current Stage A head

Current exact PR #356 head:

`d28ca0fae1092c63a671a159911479965b2ca5fe`

Exact-head workflows:

- inherited WarrantFuzz workflow `35238778124`: **SUCCESS**;
- Stage A adapter workflow `35238778132`: **SUCCESS**;
- Stage A unit/hostile tests: **23 PASS**;
- exact manifest: **90 requests**;
- requests attempted: **0**;
- recorded/accounted spend: **$0.00**;
- conservative whole-run worst-case: **$1.15164**;
- authorised ceiling: **$10.00**.

The `$1.15164` value is a conservative execution ceiling, not a provider bill or expected charge.

## Agent-facing experiment lock

Stage A deliberately sends only:

```text
baseline
baseline_replicate   # byte-identical agent input to baseline
mutant_raw           # second apparent support report, no ancestry envelope
```

Before any target output, the experiment was tightened and the interpretation frozen:

- agent-facing IDs are neutral (`src-1`, `src-2`); original fixture IDs remain manifest-only;
- baseline contains a synthetic source excerpt;
- mutant adds a differently worded excerpt carrying the same distinctive synthetic facts: `240 cases`, `50 -> 41 minutes`;
- no agent-facing payload may contain `origin`, `derivative`, `duplicate`, `copy`, `paraphrase`, `mutant`, `baseline`, `replicate` or `control` cues;
- baseline / baseline-replicate / mutant are interleaved round-robin by run index;
- source independence is explicitly part of the assessment task in every arm through the frozen response schema;
- Stage A therefore measures behaviour on a **prompted independent-corroboration assessment**, not unprompted/natural evidence handling.

Frozen interpretation:

> If a complete Stage A run strengthens on the mutant, the narrow claim is that the model treated a second same-figures retelling as sufficiently additional evidence to increase confidence and/or approval under this independent-corroboration task.

Do **not** call such a result proof that the model failed to detect hidden source laundering: the target input does not itself prove the two reports share an origin. A no-strengthening result likewise does not establish general provenance competence.

## Request / ledger integrity

Codex PR #357 was integrated into the Stage A branch before the latest head. Current controls now include:

- provider request identity hash binds API endpoint + complete provider request body, including model and generation/schema settings;
- ledger admission rejects stale `measurement_head`, `input_sha256`, `request_sha256`, unexpected keys and invalid state transitions;
- each provider call is journaled as `attempting` **before** dispatch, with append + flush + fsync;
- the attempting event reserves the whole-call conservative worst-case cost;
- an attempting-only row is treated as an uncertain prior attempt, counts against spend, and blocks silent retry;
- successful calls use observed token usage only when token telemetry is present and numeric;
- missing/non-numeric usage telemetry reserves the whole-call worst-case cost rather than collapsing to `$0`;
- failed possibly-billed attempts reserve whole-call worst-case cost and are not silently retried;
- append-only ledger + summary remain the evidence record;
- provider execution workflow is manual `workflow_dispatch` only.

## Provider execution state

The only provider-actuation attempt remains GitHub Actions run:

`35234396187`

That run was on the superseded adapter head. It reached the spend step with an empty repository `OPENAI_API_KEY`, printed:

`EXECUTION_BLOCKED_NO_CREDENTIAL_ROUTE`

and exited before any API request.

Current result therefore remains:

```text
API CALLS EXECUTED = 0
RECORDED API SPEND = $0.00
STAGE A MODEL RESULT = NOT RUN
90 REQUESTS = UNEXECUTED
```

No provider actuation has occurred at current head `d28ca0f...`.

## Product-shell separation

ProofPath product PR #355 is a separate deterministic shell. Its current repaired head is:

`bca431e572cc6d8b334c09be958bce52a909e9b1`

Exact-head workflow `35239124064`: **SUCCESS**.

It now exposes action-only regressions, baseline structure, true controls, role-specific power and wrong-lineage sensitivity. In particular, the independent-contradiction responsiveness guard is powered against **evidence-blind vs lineage-aware**, so a hardening that simply stops responding to evidence fails.

Those repairs improve the product shell but do not create a Stage A model result. Stage A stochastic measurement authority remains #351/#356.

## Current route

An aperture may execute the exact current #356 Stage A design under Mark's existing bounded authorization **only if its environment already legitimately exposes an authorised OpenAI API credential**.

It may not, on this authority alone:

- create or recover an API key;
- copy/move credentials between environments;
- create an account or alter billing;
- change models, sample counts, conditions, prompt contract or scorer after seeing outputs;
- increase the $10 ceiling;
- add retries;
- proceed to Stage B, ancestry/hardening controls or competition submission.

If no existing credential route is available, the correct state remains:

`EXECUTION_BLOCKED_NO_CREDENTIAL_ROUTE`

not a null model result.

## Resource consequence

The blocked execution turns API access from a hypothetical concern into a concrete project-resource gap. A non-binding OpenAI Codex Open Source Fund packet is prepared at:

`coordination/resources/OPENAI_CODEX_OPEN_SOURCE_FUND_PREP_20260917.md`

It is anchored to The Human Record, which carries an explicit CC0 dedication for project-authored rights Mark actually holds. No application has been submitted; identity/contact/form submission remain human gates.

## Ceilings

```text
AUTHORISED_SPEND != STANDING_SPEND_AUTHORITY
SPEND_AUTHORISED != CREDENTIAL_AUTHORITY
AUTHORISED_SPEND != SPEND_THAT_MEASURES_NOTHING
BLOCKED_EXECUTION != NULL_RESULT
INCOMPLETE != NULL_RESULT
NO_CREDENTIAL_ROUTE != NO_MODEL_EFFECT
OFFLINE_GATE_PASS != MODEL_RESULT
PRODUCT_SHELL_DEFECT != MEASUREMENT_RESULT
REAL_FAILURE_BEFORE_PRODUCT_POLISH
NO_SIGNAL -> SHRINK / STOP
```
