# PSFH D087 — current TRACE / Mechanical Ethics source-route repair

Date: 25 September 2026

Status: **PUBLISHED / MAINTAINED SOURCE GREEN / SELECTED LIVE BYTES VERIFIED / READER BENEFIT UNMEASURED**

Purpose:
Repair a provenance/currentness mismatch in human-facing Explore source routes without rewriting the historical source basis of the Explore reading nodes.

## Defect

D086 correctly preserved the historical source snapshots used by the Explore node synthesis:

- TRACE historical node basis: `46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b`;
- Mechanical Ethics historical node basis: `44f7efb59806242fd26c572cbfbaaeaefaea2058`.

However, links explicitly labelled **current-source route** in:
- `explore/sources.html`;
- `explore/sources.md`;
- `explore/packet.md`;

still pointed at older intermediate README commits:

- TRACE `8310d2531d3b2fe4e3b44c92d1d544a322f52bf4`;
- Mechanical Ethics `25a9d793af1cded26dd2d766e1d1c08e1b30f652`.

The machine source map already carried the released current-home commits, so human and machine provenance had drifted.

## Source repair

COM PR #491 — `PSFH D087: refresh current TRACE/ME source routes`

Exact reviewed candidate head:
`5a91aea30871bfede42d9236d56abcd808ac3227`

Exact-head maintained CI:
`36197905418 / SUCCESS`

Maintained-source merge:
`f1812a8d7d965c09cfd2eeaad51b31aa25313847`

The repair:
- points TRACE current-source README routes to `6c68fae8cbc51d0ef1e77a18e220ceb7a1207025` (released v0.4.0);
- points Mechanical Ethics current-source README routes to `e2ef746e931161cb70ac46a4eaa122442134e86b` (released v0.8.0);
- leaves the historical node-source snapshots unchanged;
- adds a regression requiring human-facing pages to contain both the historical basis and the current-home identities;
- rejects the two stale intermediate README identities.

## D087 release

Release branch after exact manifest pin:
`framework/psfh-d087-publish-20260925@7bfe409d79fbd2541d10c9f63099f29d27516630`

One-shot publication workflow:
`PSFH D087 publish current TRACE/ME source routes / 36198130032 / SUCCESS`

Fail-closed public predecessor:
`gh-pages@86ed354053ba9441099447c9e82441b56d79df27`

Published `gh-pages`:
`723b07f719adacbca14cd81c61a54bcbf0c58a41`

Site Preview:
`0.8.44`

Final maintained source after release metadata sync:
`028068961dd8814e639917afcde9bb2cef7b639b`

Post-sync maintained CI:
`36198262841 / SUCCESS`

## Live verification

The one-shot publication workflow verified through the custom domain that:

- live manifest converged to `site_edition = 0.8.44`;
- `explore/sources.html`, `explore/sources.md` and `explore/packet.md` contain current TRACE `6c68fae8…`;
- the same pages contain current Mechanical Ethics `e2ef746e…`;
- the intended historical basis TRACE `46f4fcd…` remains present;
- the intended historical basis ME `44f7efb…` remains present;
- stale TRACE `8310d253…` is absent;
- stale ME `25a9d793…` is absent;
- live change history contains D087.

A separate GitHub published-branch read observed the same state at `gh-pages@723b07f7…`.

## Scope boundaries

No change to:
- TRACE source, semantics, release, licence or AI-training permission;
- Mechanical Ethics source, semantics, release, licence or AI-training permission;
- Explore node text or authored graph relations;
- artwork, Works, navigation or layout;
- THR;
- public intake, tracking or server behaviour.

Preserve:

```text
CURRENT_SOURCE_ROUTE != HISTORICAL_NODE_BASIS
HUMAN_PROVENANCE != MACHINE_PROVENANCE_BY_ASSUMPTION
PUBLISHED != READER_BENEFIT
GREEN CI != FRAMEWORK VALIDATION
CURRENTNESS REPAIR != SEMANTIC RELEASE
```
