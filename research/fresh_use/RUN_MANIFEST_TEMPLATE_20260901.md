# 7Q FRESH USE — RUN MANIFEST TEMPLATE — 2026-09-01

Status: PRE-DISPATCH RESEARCH OBJECT / NOT RESULT / NOT AUTHORITY

One manifest is completed for every receiver cell before arm identity is unmasked for evaluation.

```text
pilot_id: 7Q-FRESH-USE-20260901
case_id: R1 | R2
cell_alias:
underlying_arm: O | Q                 # evaluator-only until scoring freeze

source_manifest_path:
source_snapshot_identifiers:
source_snapshot_sha256:
source_retrieval_utc:
source_live_browsing_for_receiver: false
neutral_task_sha256:
receiver_prompt_sha256:
seven_q_sha256:                       # null for O

receiver_model_provider:
receiver_model_version:
receiver_settings:
receiver_session_id_or_local_alias:
receiver_prior_project_exposure: NONE_KNOWN | KNOWN | UNKNOWN
receiver_prior_case_exposure: NONE_KNOWN | KNOWN | UNKNOWN
freshness_note:

receiver_start_utc:
receiver_end_utc:
reported_input_tokens:
reported_output_tokens:
answer_unicode_words:
answer_sha256:
errors_or_truncation:

source_open_count:
clarification_count:
terminology_lookup_count:

scorer_1_identity:
scorer_1_project_exposure:
scorer_2_identity:                    # optional / preferred for interpretive disputes
scorer_2_project_exposure:
arm_unmasked_after_scoring: true | false

material_action_delta:
material_evidence_delta:
material_owner_handoff_delta:
material_scope_burden_delta:
material_time_correction_delta:
unique_material_error:
burden_note:

disposition:
  7Q_FRESH_USE_SIGNAL |
  ORDINARY_SUFFICIENT |
  NO_MATERIAL_DIFFERENCE |
  7Q_BURDEN_EXCEEDS_VALUE |
  7Q_UNIQUE_ERROR |
  CASE_NOT_DISCRIMINATING |
  EVALUATION_INCONCLUSIVE
```

## Identity / hashing rule

- Hash exact UTF-8 bytes with LF line endings for experiment-owned text objects.
- For external source snapshots, record the exact preserved artifact identity/hash used in the receiver run.
- Do not claim a live webpage URL alone identifies immutable bytes.

## Burden rule

Do not collapse burden into output length.

Where observable preserve:
- source-reading effort/time;
- input/output tokens;
- response time;
- clarification/terminology lookup;
- evaluator effort;
- any extra source handling required only by one arm.

## Freshness ceiling

`NEW SESSION != HISTORICALLY FRESH RECEIVER`.

If prior project/case exposure is unknown, preserve UNKNOWN. Do not upgrade it to NONE.

## Evaluation ceiling

A disposition applies only to the named cell/case under the frozen source/task/model condition. Do not aggregate R1 + R2 into a universal winner.
