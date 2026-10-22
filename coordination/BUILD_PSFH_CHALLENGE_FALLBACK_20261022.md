# PSFH first-visit correction: discoverable HTML challenge fallback

22 October 2026. Source-only draft; no deployment or browser acceptance.

Basis: PR829 b5f1b438fd4467f5c97323631cd9f929115cf83c; observed published gh-pages d7473141ba89ab74ad51a875634034c96dffc4e9. Both contain identical llms.txt blob b248abf3763ba051a7acbc629e53efa53ea2e724 and challenge.md blob cad50d149608270a3b2d7866d7961653fca7f039. Existing HTML challenge exists in both trees, with different rendered blob identities. Do not overwrite published source with the older candidate.

Observed first failure: retrieving https://pleasestartfromhere.com/explore/challenge.md returned unsupported content-type text/markdown. This is this retrieval client's failure, not absent content or an origin outage. https://pleasestartfromhere.com/explore/challenge.html was readable and disclosed GitHub account requirement/no response-time promise, with readable onward https://pleasestartfromhere.com/discussion/. This is an existing alternative representation, not a bypass of an access control.

Change: one paragraph in public/llms.txt, adjacent to the existing reply boundary and within the first5000 characters, names the existing HTML challenge and discussion routes. It explicitly preserves reading versus posting and local preparation versus submission. No new service or intake is promised. Published and candidate llms sources were identical before patch, so the correction is portable without adopting the whole draft.

Verification: Git source paths exist; root→llms→HTML challenge→discussion was read through the actual retrieval tool; patch placement checked within first5000 characters. Existing Markdown failure retained as evidence above. No old build suite rerun is needed for one static link paragraph. Browser/keyboard/AT, whole-site reachability, receipt of a real challenge and public deployment NOT_RUN.

Other observations: root and index.html yielded different-aged retrieval copies; this does not establish divergent origin bytes. Manifest returned edition0.8.55 and dated provenance. Source/current-host equality and canonical book/TRACE/THR traversal remain outside this bounded correction's acceptance; do not infer complete-site acceptance. No arbitrary route guesses count as broken-link findings.
