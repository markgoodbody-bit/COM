# Preview 0.8.4: exact release candidate, not published

Date: 9 September 2026
Direction: `FW-CONCRETE-FIRST-INTEGRATED-RC-20260909-001`, comment5604521107.

## Review object

- Base maintained source: `d28121c7fca9d064226670fc568dad57073c836c`
- RC source: `3f7803d27c3615d81ede643f153dc2ec20270e01`
- Draft PR: https://github.com/markgoodbody-bit/COM/pull/126
- Published comparison: `dd06d95cb880208b30f703c54af33c2440c97812`
- Local RC: `C:/Users/markg/Downloads/PSFH-preview084-rc-20260909`

The RC has not been merged into maintained source or pushed to gh-pages. No managed Sites registration/migration or new hosting setup occurred. This was source-only release preparation, not a visual redesign or fresh browser usability review.

## Explicit before/after

Eight source files change from d281:

1. `scripts/site-edition.mjs`:0.8.3 ->0.8.4.
2. `public/llms.txt`: edition label only; reviewed absolute links remain.
3. `public/changes.md`: Edition0.11/D015 describes the candidate, its ceilings and prior Homer clarification. Everything from `### D014` onwards is byte-identical to d281.
4. `public/changes.html`: counterpart from the existing pinned prose renderer at COMe63d4fa7. That renderer first reproduced the old HTML exactly. No generator redesign.
5. `public/manifest.json`: site label, previous-history source coordinate and exact input history pins.
6. `scripts/source-views.mjs`: orientation edition and exact llms hash; other source pins unchanged.
7. `scripts/test-house-style.mjs`: the seed comparison permits exactly the already-reviewed PR125 ceiling, while requiring every predecessor byte after removal of that one line, exact1023-byte size and fixed SHA256.
8. `scripts/check-visible-routes.py`: requires the approved compact start.json anchor destination/label rather than its full URL as visible prose; other named URLs remain explicitly visible. Its description no longer claims attribute-free recovery of that compact destination.

No app/page.tsx, globals.css, seed, art, book, Explore or discussion source edit. Repository blob identity was verified for page/CSS/seed. An initial direct checkout-byte vs Git-blob assertion failed on page.tsx due CRLF checkout translation; canonical blobs match, and normalizing only CRLF reproduced the Git bytes. Do not confuse that failed comparison with a product edit or call raw checkout bytes identical to Git blobs.

## Failures found, then corrected

Exact integrated d281 initially failed to build because its orientation hash still pinned the pre-PR125 llms bytes. Updating that required pin is part of release metadata.

The first full RC checks then passed22 Python tests but failed one Node historical comparison on the approved seed addition. The standalone older route checker also failed because it still required start.json as full visible URL prose. The narrow repairs above preserve the approved text/destination contracts; no product was changed to satisfy them and no failing surface was omitted from the final run.

## Final observed checks

- Maintained build PASS.
-22/22 Python unittest-discovery tests PASS, including the fixed PR123 editorial contract and its two negative controls.
-11/11 Node tests PASS, including delivery of all115 generated files and indexes.
- Standalone visible-route/destination checker PASS with its revised stated scope.
- Seed1023bytes, SHA256 `d9494fe389ce625df5c065f23f596cc2626391f026161979f43a229dca175d79`.
- Root15337bytes, SHA256 `25d0406fcd20f4b6e0ed4667841928f45dd502aa38c64fba53ab9fbd496c05ca`.
- Generated manifest7084bytes, SHA256 `4753b06595f87ca99836a06b7e5c3cdeb07135be76f1757061fdac4a6570b779`.
- Offline local carrier106143bytes, SHA256 `d535b92f0ffbc69786362ca4065088f8b5226aa76fe2c2117b887ff1b974e47a`.

Full generated comparison and each changed file's before/after size/hash/classification are in sibling `PSFH_PREVIEW084_RC_FILE_DELTA_20260909.json`.

115 generated files: **11 changed,104 byte-identical, zero added, zero removed**. Publishing-only `.gitattributes`, `.nojekyll`, CNAME and README are outside that generated inventory, not deletions to perform.

All four artwork artifacts unchanged. Existing CSS is an exact prefix; appended rules are the reviewed concrete-story/technical-handoff styles. The start/book/spine source-text wrappers differ only in the site-edition label, not source payload. The orientation wrapper changes with its exact llms payload. Original resource files, Explore corpus/map and discussion bodies/files remain byte-identical to the published comparison.

## Publication and rollback proposal, not authority

After CC's release-metadata/accidental-bundle review and Framework's exact publication decision, reacquire source and gh-pages heads. If either moved, compare rather than assume this receipt still applies.

Proposed publication contains only these115 generated files from the reviewed RC; preserve publishing configuration and do not bundle Powers, Vermeer, guestbook/intake, study material, service changes or other drafts. Require generated-tree parity, successful Pages deployment and separately attributed served-content verification. Previous custom-domain access refusals remain; no bypass is proposed.

Rollback target is the existing published dd06d95 tree. If authorised and needed, restore its known generated content through a new forward publishing commit, preserve configuration/history and verify the deployment; no force push or erased history. No rollback was executed or tested here.

D015 calls itself a candidate, not a receipt of deployment. A future publication record must name the actual deployment after observation, not invent an earlier publication date. Mechanical checks and prior content closure do not establish reader benefit, universal accessibility or practical advantage.
