# THR Hannibal reader gate + PSFH D070 delivery receipt — 2026-09-18

Status: **BOUNDED COORDINATION RECEIPT / NOT CANON / NOT VALIDATION**  
Basis before this receipt: COM main `707b5225172fcfe523f2732b53e72b3044f87a71`.  
Later live source and direct human direction win.

> **HOW CAN WE MAKE A BETTER FUTURE?**

## The Human Record

Production main remains:

`58f1b7ade96ea2a5524bb6d36fdba193f8c016db`

Public catalogue remains exactly **three records**.

Hannibal candidate PR #35 remains a draft/non-public surface at:

`836f93e0849268359c58d531792bce1890271691`

What changed after the morning checkpoint:
- Claude Code completed the differentiated revised-head hostile review; one missing Polybius 3.48.12 source-method assertion was added and rechecked.
- THR's own selection discipline exposed one further gap: the selection-time candidate pool / alternatives were not preserved. The candidate now records that absence rather than reconstructing it.
- PR #39's reviewed reader copy was integrated into the PR #35 branch only.
- `cases/hannibal-reader-page-proposal.html` is a styled, `noindex,nofollow`, non-catalogued mockup outside `/records/`.
- exact PR35 head workflow `35339637347` = SUCCESS; integrity + rejection-case tests = SUCCESS.
- public hostile-review issue #31 now carries a bounded reader-object break request; no outsider response had landed at the last check.

Current residue:

```text
HISTORICAL PERSON != SURVIVING BIOGRAPHY
CANDIDATE != RECORD_4
GREEN_CANDIDATE != PUBLICATION
NO_OUTSIDER_RESPONSE_YET != REJECTION
```

Next: **wait for reader/outside evidence or a new concrete falsifier; no new THR specimen and no catalogue promotion by momentum.**

## PSFH D070

D069 public base before this work:

`23e3047cb9ba9d9b42ac12b18e5be59a41a17449`

D070 purpose:
- advance same-domain TRACE/ME current aliases to released TRACE v0.3.0 / ME v0.7.0;
- preserve the historical pre-release source basis used by adapted Explore readings;
- preserve fixed released snapshots;
- update PSFH's THR description to the actual three-record public state;
- retain all evidence/authority ceilings.

### Hostile-review repair before final publication

Claude Code found that `public/manifest.json` had wrongly advanced `human_preview_source_revision` from the historical preview basis to released commits.

Restored:
- TRACE preview basis = `46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b`
- ME preview basis = `44f7efb59806242fd26c572cbfbaaeaefaea2058`

Current-source / released-resource routes remain:
- TRACE = `8310d2531d3b2fe4e3b44c92d1d544a322f52bf4`
- ME = `25a9d793af1cded26dd2d766e1d1c08e1b30f652`

A regression now protects that historical/current distinction.

### Delivery witness added

A live verifier now checks:
- every current and release-snapshot resource declared in `resources/inventory.json`;
- public manifest;
- public inventory;
- `llms.txt`;
- `packet.md`;
- `changes.md`.

The first publication run correctly exposed a delivery defect:
- `gh-pages` reached `428340c82a09470bb5515f3d0efce24a3d04aa02`;
- 29/33 live targets converged;
- four README targets failed;
- cause: publisher used recursive `rsync --exclude='README.md'` while intending to preserve only root `README.md`.

Repair:
- exclusion narrowed to `--exclude='/README.md'`;
- staged-tree `verifyResources('/tmp/psfh-publish/resources')` now runs before commit/push.

Exact maintained source after repair:

`7ef97775f3f9970042c87d476ac9e39eb2516b49`

Maintained CI:
- run `35340308124` = SUCCESS.

Final public `gh-pages`:

`c0a830bfd14ca76052a1ee5913d302952485f57c`

Pages deployment:
- run `35340423410` = SUCCESS.

Final publisher:
- run `35340379133` = SUCCESS;
- job `105584667180` = SUCCESS;
- live verification: `LIVE_PSFH_D070_VERIFIED targets=33 attempt=5`.

The repaired public tree now contains both released current READMEs and both released snapshot READMEs with the expected exact Git blobs.

```text
SOURCE_GREEN != PUBLISHED
GH_PAGES_PUSHED != LIVE_DOMAIN_CONVERGED
LIVE_BYTE_MATCH = DELIVERY_WITNESS, NOT READER_BENEFIT
PUBLICATION != VALIDATION
```

D070 is therefore **LIVE / BYTE-VERIFIED / READER BENEFIT UNESTABLISHED**.

## External discovery observation

A bounded current search for the two first-party domains surfaced an outside discussion of PSFH but did not prominently surface either first-party domain. Current PSFH indexing signals are already permissive (root has no `noindex`, `robots.txt` allows public retrieval, sitemap exists).

Disposition:

```text
WEAK_SEARCH_VISIBILITY_SIGNAL != INDEXING_DEFECT_PROVEN
NO_NEW_SEO_BUILD
OBSERVE
```

## Portfolio consequence

```text
THR -> WAIT FOR READER / OUTSIDE EVIDENCE
PSFH -> D070 LIVE; OBSERVE, DO NOT CHURN
ATRS -> SEPTEMBER METHOD FROZEN; WAIT FRESH NOVEMBER WORLD DATA
TRACE / ME -> RELEASED BASELINES; NO MOMENTUM EDIT
#99 -> FIELD WATCH
RESOURCES -> QUARRY / NO APPLICATION LIVE
```

The useful lesson from this pass was mechanical rather than conceptual:

```text
BUILT_BYTES != STAGED_BYTES
STAGED_BYTES != PUSHED_BYTES
PUSHED_BYTES != SERVED_BYTES
SERVE_VERIFIED != READER_BENEFIT
```
