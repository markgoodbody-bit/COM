# ProofPath Stage A — authorization / execution receipt

Date: **2026-09-17 — Europe/London**  
Status: **AUTHORISED / REPAIRED OFFLINE GATES PASS / EXECUTION BLOCKED BEFORE PROVIDER CALL / $0 SPENT / NO MODEL RESULT**

> HOW CAN WE MAKE A BETTER FUTURE?

This receipt records one bounded experiment inside COM #349. It is not a competition selection, efficacy result, general provider authority or standing spend permission.

## Human gate

Mark explicitly approved the staged real-model pilot with:

`very good. go ahead`

The approved boundary remains:

```text
TARGETS = gpt-5.6-terra + gpt-5.6-sol
STAGE A = 15 baseline + 15 exact baseline replicate + 15 raw duplicate-evidence mutant PER MODEL
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

The provider/execution adapter is isolated in PR #356. The first attempted execution head (`d944676...`) made no provider call because no GitHub `OPENAI_API_KEY` was exposed. Claude Code then found a more important pre-spend defect in that head: the agent-facing IDs leaked `origin-a` / `derivative-a` and the evidence rows carried no actual text, making either a positive or null result uninterpretable.

That head is superseded for any future execution.

## Repaired Stage A head

Current exact PR #356 head:

`f60387b69a291da5cc894008a2d8a442028da194`

Stage A now deliberately sends only:

```text
baseline
baseline_replicate   # byte-identical agent input to baseline
mutant_raw           # second apparent support with no ancestry envelope
```

Experiment/payload repairs before any spend:

- agent-facing source IDs are neutral (`src-1`, `src-2`); internal fixture IDs remain manifest-only;
- baseline source has a synthetic excerpt;
- mutant adds a differently worded excerpt carrying the same distinctive pilot facts, making content overlap recognisable in principle without telling the model it is a copy/derivative;
- agent-facing prompt/payload is rejected if it contains lineage/mutation tells such as `origin`, `derivative`, `duplicate`, `copy` or `paraphrase`;
- baseline / baseline-replicate / mutant are round-robin by run index rather than time-blocked;
- plain-English warning / correct ancestry / wrong ancestry / hardening remain later controls and are not part of Stage A.

Execution-control repairs:

- `--execute` remains required;
- `store: false` remains set;
- `reasoning.effort=none`, structured output, max output 512 tokens;
- no automatic retry;
- a failed provider attempt reserves that call's conservative worst-case cost because a timeout/failure may still have been billed;
- a failed key is treated as attempted and is not silently retried;
- append-only ledger remains the evidence record;
- provider execution workflow is now `workflow_dispatch` only; commit-message push actuation was removed;
- exact-model pricing was rechecked against current OpenAI model documentation before repair: Terra $2/M input, $12/M output; Sol $4/M input, $20/M output.

## Repaired offline gates

Exact-head evidence at `f60387b...`:

- inherited WarrantFuzz workflow `35237109779`: **SUCCESS**;
- Stage A adapter workflow `35237109788`: **SUCCESS**;
- adapter/unit/hostile tests: **11 PASS**;
- exact manifest: **90 requests**;
- requests attempted: **0**;
- recorded/accounted spend: **$0.00**;
- conservative whole-run worst-case after source excerpts were added: **$1.15164**;
- authorised ceiling: **$10.00**.

The `$1.15164` value is a conservative execution ceiling, not a bill or expected charge.

## Provider execution state

The only provider-actuation attempt so far remains GitHub Actions run:

`35234396187`

It reached the spend step with an empty repository `OPENAI_API_KEY` and emitted:

`EXECUTION_BLOCKED_NO_CREDENTIAL_ROUTE`

before any API request.

Current result therefore remains:

```text
API CALLS EXECUTED = 0
RECORDED API SPEND = $0.00
STAGE A MODEL RESULT = NOT RUN
90 REQUESTS = UNEXECUTED
```

No run has been attempted against repaired head `f60387b...` because provider execution is manual-dispatch only and the known GitHub secret route is absent.

## Product-shell separation

ProofPath product PR #355 is a separate deterministic shell. Its current repaired head is `82c6988ed79a12cf16893843d91a1ded5dbfdc20`, workflow `35237752920` SUCCESS. It now exposes action-only regressions, mutation power, baseline structure, unpowered guards and sensitivity controls.

Those repairs improve the product shell but do not create a Stage A model result. Stage A stochastic measurement authority remains #351/#356.

## Current route

An aperture may execute the exact repaired #356 Stage A design under Mark's existing bounded authorization **only if its current environment already legitimately exposes an authorised OpenAI API credential**.

It may not, on this authority alone:

- create or recover an API key;
- copy/move credentials between environments;
- create an account or alter billing;
- change models, sample counts, conditions or scorer after seeing outputs;
- increase the $10 ceiling;
- add retries;
- proceed to Stage B, ancestry/hardening controls or competition submission.

If no existing credential route is available, the correct result remains:

`EXECUTION_BLOCKED_NO_CREDENTIAL_ROUTE`

not a null model result.

## Ceilings

```text
AUTHORISED_SPEND != STANDING_SPEND_AUTHORITY
SPEND_AUTHORISED != CREDENTIAL_AUTHORITY
AUTHORISED_SPEND != SPEND_THAT_MEASURES_NOTHING
BLOCKED_EXECUTION != NULL_RESULT
NO_CREDENTIAL_ROUTE != NO_MODEL_EFFECT
OFFLINE_GATE_PASS != MODEL_RESULT
PRODUCT_SHELL_DEFECT != MEASUREMENT_RESULT
REAL_FAILURE_BEFORE_PRODUCT_POLISH
NO_SIGNAL -> SHRINK / STOP
```
