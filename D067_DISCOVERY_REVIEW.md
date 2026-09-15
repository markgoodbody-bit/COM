# D067 discoverability candidate

Basis: maintained D066 `404de6f0` plus FW draft `3188fefd`, COM #336 / PR #337.

Before: THR had machine routes in the draft but no visible PSFH root route; the static root lacked canonical/OpenGraph metadata. After: one bounded separate-project paragraph, first-party metadata, Site Preview 0.8.26 and paired D067 history with renewed exact history hashes. No crawler-policy, licence, stewardship or framework-source change.

## Verification

- Maintained build passes with history, resource and source-view pins enforced.
- Four D067 checks pass: visible route/standing, metadata, edition/history, local homepage destinations.
- Four existing Python source-view roundtrip checks pass.
- Chrome 1440×900 and 390×844: exactly one visible THR link, expected separate-project wording, no page errors or horizontal overflow. Mobile screenshot visually inspected.
- Built unchanged D066 in a separate worktree for comparison. Both versions show the same 21 failing Node cases (29 passing of 50) and five failing Python cases (17 passing of 22). Historical objects are unavailable in this shallow checkout and several tests assert superseded wording/editions. This comparison is not a passing full suite; no old assertions were weakened.
- Only ten generated files differ: index.html, llms.txt, packet.md, manifest.json, changes.md, changes.html, and four read/*.html wrappers. Artwork, Explore output, framework resources, CSS, seed, robots and sitemap are byte-identical to the D066 build.

The first output-comparison helper incorrectly matched Windows paths and returned an empty delta. Corrected to use relative paths; the ten-file result above is the corrected comparison.

## Not established

Candidate not yet published. No indexing, reach, adoption or usefulness result. Public D066 remains unchanged. Hosting identity/readback must be recorded only after deployment. The inherited test-suite failures remain visible for the integration decision.
