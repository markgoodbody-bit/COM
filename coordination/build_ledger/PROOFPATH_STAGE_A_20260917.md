# ProofPath Stage A — authorization / execution receipt

Date: **2026-09-17 — Europe/London**  
Status: **AUTHORISED / OFFLINE GATES PASS / EXECUTION BLOCKED BEFORE PROVIDER CALL / $0 SPENT / NO MODEL RESULT**

> HOW CAN WE MAKE A BETTER FUTURE?

This receipt records one bounded experiment inside COM #349. It is not a competition selection, efficacy result, general provider authority or standing spend permission.

## Human gate

Mark explicitly approved the proposed staged real-model pilot with the instruction:

`very good. go ahead`

The approved boundary was already stated immediately before that instruction:

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

Stage A measurement/scoring is frozen at repaired WarrantFuzz PR #351 head:

`88264d5824c985cba85a6831912aaeb5b07b5f2e`

Exact-head GitHub Actions run `35217059591`: **SUCCESS**.

The Stage A provider adapter is isolated in PR #356 / branch `framework/proofpath-stage-a-openai`; its current execution head at the first attempt was:

`d944676282fe9e9a91aceea9e760a9f1c48ac807`

It changes provider plumbing, not the frozen scorer.

Stage A deliberately sends only:

```text
baseline
baseline_replicate   # byte-identical target input to baseline
mutant_raw           # duplicate apparent support, no agent-facing ancestry envelope
```

The agent-facing system instruction is neutral and does not teach the source-independence rule. Apparent source labels are neutralised (`Source 1`, `Source 2`) rather than calling the second item derivative. Plain-English warning, correct ancestry, wrong/shuffled ancestry and hardening remain later controls and are not part of this spend stage.

## Offline gates

On the execution branch before provider actuation:

- inherited WarrantFuzz suite: **SUCCESS**;
- Stage A adapter suite: **SUCCESS**;
- adapter unit tests: **6 PASS**;
- exact manifest: **90 requests**;
- recorded pre-run spend: **$0.00**;
- conservative whole-run worst-case ceiling under the adapter's 512-output-token limit: **$1.10853**;
- authorised ceiling: **$10.00**.

The $1.10853 value is a conservative execution ceiling produced by the adapter, not a provider bill or expected charge.

## Provider execution attempt

GitHub Actions run:

`35234396187`

re-ran the offline gates successfully, then reached the execution step. The repository secret exposed to that job as `OPENAI_API_KEY` was empty. The workflow therefore printed:

`EXECUTION_BLOCKED_NO_CREDENTIAL_ROUTE`

and exited with code 2 before `stage_a_openai.py --execute` could make a provider call.

Result:

```text
API CALLS EXECUTED = 0
RECORDED API SPEND = $0.00
STAGE A MODEL RESULT = NOT RUN
90 REQUESTS = UNEXECUTED
```

The run preserved the manifest artifact. No result ledger or model summary can exist because no request was sent.

## Concurrency correction

After earlier ProofPath CI #355 green deterministic runs, Codex and Claude Code found additional defects in the #355 product shell, including an action-only false PASS and mutation-power/control problems. Those findings are controlling for the product shell.

They do **not** manufacture a Stage A result and do not change the frozen #351 measurement object. Stage A execution authority therefore remains attached to #351/#356 only, not #355.

## Current route

An aperture may execute the exact #356 Stage A adapter under the existing Mark authorization **only if its current environment already legitimately exposes an authorised OpenAI API credential**.

It may not, on this authority alone:

- create or recover an API key;
- copy/move credentials between environments;
- create an account or alter billing;
- change models, sample counts, conditions or scorer after seeing outputs;
- increase the $10 ceiling;
- add silent retries;
- proceed to Stage B, ancestry/hardening controls or competition submission.

If no existing credential route is available, the correct result remains:

`EXECUTION_BLOCKED_NO_CREDENTIAL_ROUTE`

not a null model result.

## Ceilings

```text
AUTHORISED_SPEND != STANDING_SPEND_AUTHORITY
SPEND_AUTHORISED != CREDENTIAL_AUTHORITY
BLOCKED_EXECUTION != NULL_RESULT
NO_CREDENTIAL_ROUTE != NO_MODEL_EFFECT
OFFLINE_GATE_PASS != MODEL_RESULT
PRODUCT_SHELL_DEFECT != MEASUREMENT_RESULT
NO_SIGNAL -> SHRINK / STOP
```
