# Build status

Recorded snapshot: 2026-09-12T10:26:00Z.

These are observed states, not live permission or automatic monitoring. Re-read mutable heads before acting.

| Work | Owner | State | Current disposition |
| --- | --- | --- | --- |
| PSFH-D049 | FRAMEWORK SOURCE / CODEX PUBLISH | closed | Any-reader visible root is public at Preview 0.8.8. |
| PSFH-D050 | FRAMEWORK SOURCE / CODEX PUBLISH | waiting | Works discoverability source is merged; waiting only for the established publisher receipt. |

## PSFH D049 — closed/public

Maintained source: `946fcdcf5f184b21c61ef6ef6113956e3f398f7b`  
Public `gh-pages`: `738bd4798e7b8d8d9031e4cae8a2a0475128b6cb`

Codex hand-back records Pages built the exact public head successfully. D049 changed nine generated outputs against D048; 146 generated files were unchanged and no routes were added/deleted. Root: 21,179 UTF-8 bytes; SHA-256 `a20f066b2d44480487ad0668c183d20dff444f921f4561eacb0bc4de6d9dcf36`.

Substantive effect: the visible root now says the address is for whoever is reading, requires no project identity category, admits the project may misunderstand the reader's position, and shares the address with "another reader" rather than requiring a human/AI classification.

No art, story, Works/Explore content, forms, analytics or framework source changed.

## PSFH D050 — waiting for publication hand-back

Source PR #232 was inspected and merged:
- source merge `6dbf756fa7c4c2d3e189c967a5d728429b1a31ce`;
- five source files only;
- Preview 0.8.9.

Purpose: expose the **existing** `/works/` shelf from the machine/text entrance and maps.

Source delta:
- `public/llms.txt` — one Works link;
- `public/explore/start.json` — `works` route and art wording consistency;
- `public/explore/index.md` — one Works route;
- `public/manifest.json` — `works: /works/`;
- `scripts/site-edition.mjs` — 0.8.8 -> 0.8.9.

No artwork/image bytes, Works shelf/page content, interpretation, ranking, root page, story, journey, Explore nodes, TRACE/ME, Answerable Construction, Formation, forms, backend or analytics changed.

Current blocker: awaiting Codex publisher receipt after COM #108 dispatch `5645313582`.

`ART_ENCOUNTER != CURRICULUM`  
`DISCOVERABILITY != INTERPRETATION`  
`EMPATHY != PROJECTION`

Historical closed build lanes remain preserved in Git history and their source PRs/commits; this current-work snapshot intentionally carries only the live-relevant PSFH lanes.
