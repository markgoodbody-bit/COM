# Campfire component and Simple-v1 installer currentness — 29 September 2026

Status: **BOUNDED CURRENTNESS RECEIPT / NO GENERAL BUILD LANE / NO INSTALL / NO PRODUCTION CHANGE**

## What actually changed

### Simple-v1 Windows installer guard

Mark's attempted install of the maintained Simple-v1 candidate at `9f0f038ee1c17663e193db76f8523d94f1217909` failed before adoption. The source payload was ASCII, but the installer compatibility rewrite used `Set-Content -Encoding UTF8` under Windows PowerShell 5.1, adding a leading UTF-8 BOM. The contract guard introduced by #270 then rejected those three installer-created bytes.

Claude Code reproduced the failure and the bounded repair in COM #76 comment `5877321354`: skip exactly one leading UTF-8 BOM while continuing to reject every later byte over `0x7F`.

Relay PR #272 applied only that guard change:
- reviewed head: `ab0ce6484a0e0c6b8144a849cdd3b6d441696ff5`;
- pull-request checks: `Campfire Square Simple v1 / 36498087672 / SUCCESS` and `campfire-ci / 36498087738 / SUCCESS`;
- merged into the draft Simple-v1 candidate as `6ca82daf8fea8424f46b44d8bb0a0829edea9c9a`;
- post-merge branch run: `36498228679 / SUCCESS`.

No installation, restart, credential use, provider call, release, Relay-main merge or Production activation followed. The installed App was restored after the failed attempt and remains on its earlier lineage.

```text
SOURCE GUARD REPAIRED != INSTALL SUCCEEDED
DRAFT CANDIDATE CURRENT != INSTALLED CURRENT
POST-MERGE CI PASS != TARGET-HOST ADOPTION
```

### Campfire encounter components

COM PR #679 is merged on COM main as a disposable internal/local shared-room encounter interface. It is an experiment, not an online service or usable forum.

COM PR #683 remains a draft portable inheritance capsule reader/viewer. Its exact current head is `cdfeb4c2ab94fe2ed9ba9057965380faf820d7b9`; hosted run `36495571732` succeeded. The branch includes strict untrusted-data reading, canonical cross-platform bytes, a read-only human HTML view and scan-first question/change navigation. Claude Code review of the latest repairs is unavailable, not satisfied. Visual/browser QA remains not established. The one-shot model probe remains unrun.

Relay PR #271 remains a separate draft encounter-memory implementation. Its private/shared visibility sketch does not match the current #679 shared-room contract. It is not silently combined with #679 or #683.

COM PR #682 remains a wider design seed only and explicitly defers current execution/wire-format authority to COM #678/#679.

## Product boundary

These are components, not a joined experience. No current artifact demonstrates the whole loop:

```text
ARRIVE
-> UNDERSTAND THE DISCUSSION
-> CONTRIBUTE
-> LEAVE
-> RETURN
-> SEE WHAT CHANGED
```

That loop is the next meaningful product-level hypothesis, but it is **PROPOSED / NOT YET EARNED AS AN ACTIVE BUILD**. Do not accumulate more isolated interface increments or join incompatible contracts merely because the pieces exist.

```text
COMPONENTS PRESENT != USABLE FORUM
TEST COUNTS != HUMAN USEFULNESS
AVAILABLE PARTS != AUTHORITY TO INTEGRATE
```

## Coordination result

- no general build lane opened;
- no TRACE, Mechanical Ethics, Formation, PSFH or Human Record source change;
- no public deployment, external invitation, provider call, spend, credential use or Production action;
- preserve COM #678/#679 as current encounter execution authority;
- preserve #683, #682 and Relay #271 as bounded drafts with their explicit limits;
- reopen implementation only for a concrete joined-use test, a target-host install decision, or a new field defect.
