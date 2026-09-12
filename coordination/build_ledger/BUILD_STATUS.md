# Build status

Recorded snapshot: 2026-09-12T10:29:10Z.

These are observed states, not live permission or automatic monitoring. Re-read mutable heads before acting.

| Work | Owner | State | Current disposition |
| --- | --- | --- | --- |
| PSFH-D049 | FRAMEWORK SOURCE / CODEX PUBLISH | closed | Any-reader visible root is public at Preview 0.8.8. |
| PSFH-D050 | FRAMEWORK SOURCE / CODEX PUBLISH | closed | Existing Works shelf is now discoverable from machine/text entry surfaces at Preview 0.8.9. |

## PSFH D049

Maintained source: `946fcdcf5f184b21c61ef6ef6113956e3f398f7b`  
Public: `738bd4798e7b8d8d9031e4cae8a2a0475128b6cb`

Visible root and machine/text welcome are aligned around an any-reader invitation without requiring an identity category.

## PSFH D050

Framework source PR #232 merge: `6dbf756fa7c4c2d3e189c967a5d728429b1a31ce`  
Final maintained source after publisher history/integrity: `67a6dfb716825c80ad0efea413fd65f90a76b551`  
Public `gh-pages`: `9b32209738e4b7b8de4bc8db7c498d3e314897bd`  
Pages run `34688546966`: success on exact public head.

D049 -> D050 public comparison: 12 modified outputs, zero added/deleted routes. No Works shelf/page or artwork path changed.

Substantive effect:
- `llms.txt` now links to `/works/`;
- `explore/start.json` now exposes a `works` route;
- `explore/index.md` now exposes the existing Works shelf;
- `manifest.json` now includes `works: /works/`;
- Preview 0.8.9.

The underlying art encounter is unchanged: five selected works, no ranking or required order, individual pages and museum records, and the works are not endorsements of the project.

No artwork/image bytes, Works content/layout/order, new interpretation, root story/journey, Explore node content, TRACE/ME, Answerable Construction, Formation, forms/backend/analytics changed.

`ART_ENCOUNTER != CURRICULUM`  
`DISCOVERABILITY != INTERPRETATION`  
`PROVENANCE != ENDORSEMENT`

All current PSFH build lanes are closed. Historical lanes remain in Git history and source PRs/commits. No later edition follows automatically.
