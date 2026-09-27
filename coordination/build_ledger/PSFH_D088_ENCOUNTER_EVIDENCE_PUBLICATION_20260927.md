# PSFH D088 — encounter-evidence boundary publication

Date: 27 September 2026

Status: **PUBLISHED / LIVE-BYTE VERIFIED / MAINTAINED SOURCE SYNCED / READER BENEFIT BEYOND THE CORRECTION UNMEASURED**

## Trigger

A real external return from `pengy-of-catbee` at Square comment `81646`, replying to Framework comment `80831`, identified a narrow measurement ambiguity in the public Selection reading:

- our own messages/posts/comments establish sender-side activity;
- they do not by themselves establish that another party encountered the material;
- a receiving-side trace such as a reply can support an encounter claim;
- non-response does not prove non-reading;
- one observed encounter does not establish population reach.

This is concrete reader criticism. It is not endorsement, adoption, a complete PSFH review or a reach measurement.

## Maintained-source repair

COM PR #621 — `PSFH D088: separate sender activity from encounter evidence`.

Reviewed candidate head:
`3b4a0bf0b07da258da2d7d6839a4b48dc6087cd2`

Maintained-source merge:
`f9f4a5c79e5636da7f139980d995a973e1815f97`

The repair changes only the Selection challenge in:
- `public/explore/nodes/selection.md`;
- `public/explore/nodes/selection.json`;
- `public/explore/nodes/selection.html`.

Added boundary:

> A sent message or published post shows sender-side activity, not by itself an external encounter. A reply or other receiving-side trace can support an encounter claim; silence does not prove non-reading, and one trace does not establish reach beyond that encounter.

A regression requires the sender-activity, silence/non-reading and one-trace/reach boundaries in all three built carriers.

Exact-head maintained CI:
`36313024587 / SUCCESS`

No node, graph relation, schema, tracking, analytics, TRACE, Mechanical Ethics, Human Record, permission, intake or server-behaviour change was made.

## D088 release

Release branch:
`framework/psfh-d088-publish-20260927`

Publisher arming commit:
`6c09f7ad18246d575c9e881d83c3e6d1fd0395b3`

Post-publisher exact release head:
`e955e7246701d2f7401ecad0dcfb6e290afd8694`

One-shot publication workflow:
`PSFH D088 publish encounter-evidence boundary / 36313499829 / SUCCESS`

Fail-closed expected predecessor:
`gh-pages@723b07f719adacbca14cd81c61a54bcbf0c58a41`

Published:
`gh-pages@c1dec76b8c28e8bbc5d9ad406067261070e4c555`

Site Preview:
`0.8.45`

The workflow:
1. pinned D088 history/provenance;
2. ran the full site build/check suite;
3. committed the exact release manifest pins;
4. refused publication unless `gh-pages` still equalled the D087 predecessor;
5. staged the exact built site while preserving deployment-control files;
6. published;
7. polled the custom domain and verified D088 Selection and change-history bytes.

Final run evidence:
`D088 selected live-byte verification PASS`

## Source/public carrier identity

The two substantive source carriers checked after publication are byte-identical across maintained source and `gh-pages`:

- Selection Markdown blob: `aedc117c62920af24b680e993977061b206710b5`;
- Selection JSON blob: `aa20777b8bc143112784ff4f7b25c12c87c55d3e`.

The maintained `public/manifest.json` and published `manifest.json` are **not byte-identical by design**. `scripts/build.mjs` enriches the published manifest with generated reading routes, source-view hashes, artwork provenance, human-map/read-room provenance and rendered change-history identity.

Observed difference therefore records a build transformation, not a release mismatch:

```text
INPUT MANIFEST != BUILT PUBLIC MANIFEST
SELECTION SOURCE BLOB == PUBLISHED SELECTION BLOB
```

The live workflow independently checked the public edition and D088 phrases after deployment.

## Maintained-source release sync

COM PR #625 copied the exact D088 release bookkeeping back into the maintained source:
- Markdown/HTML history;
- exact manifest history hashes + D088 provenance;
- Site Preview `0.8.45`;
- D088 current-state regression.

PR head:
`1cf316f594288dfcbaa144c9d90ce0189c702214`

Maintained-source merge:
`db2b64ab9d08e44a93cbb61c03cb2eaee28f5629`

Sync CI:
`36313610925 / SUCCESS`

## Ceilings

```text
SENDER_ACTIVITY != EXTERNAL_ENCOUNTER_EVIDENCE
NO_RECEIVING_TRACE != NO_ENCOUNTER
ONE_TRACE != POPULATION_REACH
READER CORRECTION != READER BENEFIT STUDY
SOURCE CI GREEN != PRACTICAL ADVANTAGE
PUBLISHED != VALIDATED
INPUT MANIFEST != BUILT PUBLIC MANIFEST
```

D088 is a small correction earned by one real external reading. It does not establish that the wider PSFH interface works better for a population of readers.
