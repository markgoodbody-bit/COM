# Current build: Explore 0.2

This extends the existing PR114 perspective walk; it is not a second proposal.

Ten optional concept nodes (change, aperture, significance, selection, futures,
power, hardening, correction, care and wisdom) sit beside the original five-file
appeal example. `library.json` is the single content source. Candidate
interpretations and normative proposals are labelled; TRACE/ME are source
snapshots, not newly released or silently revised material.

`build.py` uses Python 3.10+ and the standard library only. It generates a finite
`explore/` tree of JSON, Markdown, plain-text entry and minimal HTML translations,
with a machine index, resource sizes/hashes, sources, actual challenge-route
access limits, and optional complete local packets. No visitor code, login,
tracking, agent identity, remote model, live submission endpoint or network
service is added. `llms.txt` follows the proposal at https://llmstxt.org/; it is
not an authority/permission file or a promise every AI will discover it.

## Build and verify

```sh
python -m unittest -v test_build
python build.py --output path-to-new-empty-staging-directory
```

The output directory must be absent or empty. The builder deliberately refuses
to overwrite an existing site. It writes only `explore/`; never CNAME, the root
page, root seed, robots, DNS, account configuration or deployment settings.
Codex remains sole live integrator/publisher through the maintained site source.
Copy ONLY generated `explore/` assets after inspection, not this main-based branch.
After publication, add one clear optional link at the public root and in the
existing llms/manifest routes. Keep the root short. Verify normal HTTPS and
byte matches externally before describing the new paths as live.

## Author-side checks

24 regression checks pass locally: shared facts, reference identity, graph links,
representation parity, HTML escaping, deterministic output, byte sizes/hashes,
rejecting unsafe paths/credential URLs, and refusal to overwrite a populated
output directory. One missing packet.html target was caught and repaired; the
link now goes to the actual Markdown packet. A temporary local HTTP smoke test
served all 57 generated files byte-for-byte and returned 404 for an unknown path.
The test server stopped afterwards. These are NOT public-deployment, cold-reader,
semantic or usefulness results. External source URLs need normal retrieval checks
at integration; no authority or truth is inferred from a checksum.

The original five JSON files below are unchanged. Generated example views update
presentation status only and retain the same F1/F2 facts. The optional full packet
contains source examples, explicitly as examples rather than live events.

