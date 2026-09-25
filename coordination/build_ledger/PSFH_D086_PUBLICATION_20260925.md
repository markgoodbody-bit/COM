# PSFH D086 — map-first Explore publication

Date: 25 September 2026

Status: **PUBLISHED / MAINTAINED SOURCE GREEN / FRESH DESKTOP+MOBILE QA / SELECTED LIVE BYTES VERIFIED / READER BENEFIT UNMEASURED**

Purpose:
Let a visitor reach the existing ten-question Explore map before six sections of project orientation, while preserving the complete artwork entrance, the orientation itself, graph/source structure and reader autonomy.

## Source / review

Superseded candidate:
- COM PR #467 — D084-based map-first Explore — closed unmerged as stale after D085.

Current source change:
- COM PR #490 — `PSFH: re-port map-first Explore onto D085`;
- reviewed exact candidate head: `067911c7658bf9f9dfcbd23345ff8cfba2c77e0c`;
- exact-head maintained CI: `36195803895 / SUCCESS`;
- maintained-source merge: `3f462ded684b1790c0df272569c29847831acccd`.

Fresh rendered QA used the exact built candidate output from hosted CI:
- desktop viewport: 1440px; complete Atkins artwork remains dominant; ten-question map scans as two columns;
- mobile viewport: 390px; map becomes one column; no observed horizontal overflow or clipped content;
- all `From here` branches remain collapsed/optional;
- `Other routes` and `About this reading space` remain available after the question map;
- visual QA found no defect worth another source edit.

The temporary QA artifact step was removed before the reviewed candidate head above was integrated.

## D086 release

Release branch after exact manifest pin:
`framework/psfh-d086-publish-20260925@d8cb6e1c7ab424121ffd714dd400c203940a1eab`

One-shot publication workflow:
`PSFH D086 publish map-first Explore / 36196077132 / SUCCESS`

Fail-closed public predecessor:
`gh-pages@e78c04f9668ad46f10c20909fffb9f6def2dda9e`

Published `gh-pages`:
`86ed354053ba9441099447c9e82441b56d79df27`

Site Preview:
`0.8.43`

Final maintained source after release metadata sync:
`c071b1e570851b275565ca364f4a788178da9bac`

Post-sync maintained CI:
`36196201700 / SUCCESS`

## What changed

After the existing complete Anna Atkins artwork entrance, Explore now:
1. asks what the reader is trying to understand, change or keep possible;
2. presents the existing ten-question map immediately;
3. keeps all thirty authored `From here` relations optional;
4. preserves the original six orientation sections verbatim under `About this reading space`;
5. preserves all other routes and machine/source representations.

Current-state regression requires:
- exactly ten graph nodes;
- exactly thirty authored relations;
- verbatim preservation of the six source orientation sections;
- map before orientation;
- preservation of all source routes;
- rejection of silently changed orientation or graph identity.

## Selected live verification in the publication run

The one-shot publisher observed:
- live manifest converged to `site_edition = 0.8.43`;
- live Explore contains the Atkins contextual-art entrance;
- live question prompt and `Ten questions` map;
- live `About this reading space` disclosure;
- exactly 10 `data-reading-node` entries;
- exactly 30 `data-relation` entries;
- reading map occurs before the orientation disclosure;
- artwork entrance occurs before the reading;
- live change history contains D086 and its map-first title.

## Scope boundaries

No change to:
- TRACE source, release or semantics;
- Mechanical Ethics source, release or semantics;
- Human Record source/schema/records;
- artwork bytes, provenance or selected works;
- Explore node Markdown/JSON text;
- authored graph relations;
- machine payload semantics;
- permissions/licensing/training grants;
- crawler policy;
- public intake/tracking;
- server behaviour or hosting topology.

Preserve:
```text
PUBLISHED != READER BENEFIT
VISUAL QA != USABILITY STUDY
MAP FIRST != ORIENTATION REMOVED
ORIENTATION DISCLOSED != ORIENTATION DEMOTED TO FALSE
GREEN CI != FRAMEWORK VALIDATION
REVERSIBLE PRESENTATION CHANGE != SEMANTIC RELEASE
```

D086 was earned by the held candidate's explicit review condition: current-source re-port, exact-head CI and fresh desktop/mobile visual inspection. It was not published merely because an old PR remained open.
