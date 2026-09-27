# Campfire Relay Simple-v1 — malformed GitHub ingress diagnostic-retention repair

Date: 27 September 2026

Status: **MAINTAINED SOURCE REPAIRED / TESTS GREEN / INSTALLED RUNTIME NOT YET UPDATED**

## Field defect

Fresh host evidence found one historical Relay #177 comment, GitHub comment ID 5380939579, whose JSON-looking body had stripped quotes.

The speech worker reparsed it on every poll. At the observation point:
- 5,252 retained PowerShell event-4100 rows existed;
- 4,028 were the same Invalid JSON primitive: campfire-simple-read-v1 parse error;
- useful diagnostics were aging out in under a day.

The historical comment is preserved. It was not edited or hidden to silence the error.

## Repair — PR #267

Candidate head: 95737a3a94be033146f607c2043cc8f1ea8ef0c1

The worker now keeps local append-only github-ingress-refusals.jsonl state.

Refusal identity: GitHub comment id + UTF-8 body SHA-256.

Behavior:
- first malformed JSON-looking body may incur one parse failure;
- identical bytes are skipped before ConvertFrom-Json on later polls;
- refusal state survives worker restart;
- an edited body with the same comment ID is automatically reconsidered;
- refusal records store id/login/hash/reason, not a copy of the malformed body;
- remote-receipt discovery and speech parsing share the refusal state.

Validation:
- Windows PowerShell 36319114531 / SUCCESS;
- broad campfire-ci 36319114533 / SUCCESS;
- post-merge Simple-v1 36319248333 / SUCCESS.

Source merge: 20b371282a848404d6a3ef962f37c8b6d7536ce3

Independent Codex hostile review found no blocking defect and reproduced one parser call for the repeated malformed payload plus reopening after an edit.

## Regression hardening — PR #268

The initial regression counted refusal rows. Hostile review correctly noted that this could miss a future refactor that moved the cache check after parsing.

PR #268 therefore counts actual entry into the extracted real ConvertFrom-CSJsonComment parser:
- first malformed body -> 1 parse;
- identical body same process -> still 1;
- refusal reloaded after simulated restart -> still 1;
- edited/fixed body -> exactly 2.

Candidate head: ae8d08c162c5559d9183805705d1d5b62833f3fb

Pre-merge:
- Windows PowerShell 36319389245 / SUCCESS;
- broad campfire-ci 36319389248 / SUCCESS.

Merge: 6a07380bdf85804d7029ce5ea6ba279a14c5192b

## Installed-runtime boundary

The most recent host observation before these repairs established:
- supervisor RUNNING;
- installed App still on the pre-#266 f4fa182 lineage;
- locally restored supervisor already carries the event ledger.

Therefore the installed worker does not yet contain #267/#268. The source repair is real; the live log flood is not claimed fixed until a later install/runtime witness establishes it.

    SOURCE_REPAIRED != INSTALLED_REPAIRED
    HISTORICAL_BAD_COMMENT != DELETE_HISTORY
    REFUSED_BODY_HASH != PERMANENT_COMMENT_BLACKLIST
    ONE_BAD_PAYLOAD != UNBOUNDED_LOG_DEBT
