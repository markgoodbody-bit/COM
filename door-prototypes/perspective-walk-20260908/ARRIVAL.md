# Explore small entrance — workday patch, 8 September 2026

Source-only update within PR114; not a new theory or live deployment receipt.
The existing ten readings and five stipulated example inputs are unchanged.

## Reader change

An arriving machine can use `explore/start.json` (1,378 UTF-8 bytes) to find
optional routes without fetching the complete resource/hash inventory.
`questions.txt` (1,650 bytes) offers every existing open question as a link;
`questions.json` (5,238 bytes) adds the same questions, exact target sizes and
all thirty existing labelled connections. No ranking, task inference or automatic
traversal is introduced. These three paths are project conventions, not standards.
The purpose, boundary and explicit value proposal are copied from library.json.

All three resources use document-relative paths, so the path structure resolves
both on the domain and in a pinned raw repository tree. This is a tested URL
resolution property, not a claim that a particular remote service is reachable
or that any AI will choose to read it. Byte sizes are not token counts or prices.

## Build and integrate

Use the same build entry point, with the updated build.py and the complete source:

```sh
python -m unittest -v test_build test_arrival
python build.py --output NEW_EMPTY_STAGING_DIRECTORY
```

The build emits sixty files. Relative to the published Explore0.2 generation:
- three added: start.json, questions.json, questions.txt;
- five changed: index.md, index.txt, index.html, llms.txt, map.json;
- fifty-two unchanged: all reading/example representations, source/reply pages
  and complete packets. library.json and the original five example inputs are unchanged.

Expected output-tree SHA256:
`8f48f08ed886510e39d812c05a80e63c3d1fd31fedbccb46f54ffc66938f255c`.
This uses the existing builder's sorted path/file-hash identity calculation.
No self-hash or independent-witness claim is added. The resource map includes
hashes/sizes for all three additions; its format and reading-library schema stay unchanged.

Codex remains the live publisher. Reacquire the current source/publishing heads
and other in-flight operations before integrating. Copy only the generated
explore/ tree through the maintained website source; preserve every unrelated
root asset, CNAME, DNS/account setting, seed and licence notice. Add a small root
machine-index link to /explore/start.json during that maintained integration.
Do not deploy the whole COM branch or run the two old fixed-base one-shot workflows.
They are historical checks, not the deployment path for this source update.

The existing native heartbeat is not given new authority by this code. Account
verification and any authorized certificate recovery remain Codex's separately
assigned foreground operation. Do not bypass TLS or call HTTP secure delivery.

## Executed checks

Thirty-six local tests passed: the original twenty-four plus twelve small-entry
checks covering source-exact questions/edges, target identity/byte counts, disclosure
of value choice, optional routes, relative resolution, discovery, new resource hashes
and rejection rather than silent truncation when entry budgets are exceeded.
All sixty generated files were served byte-identically by a temporary loopback
HTTP server; an unknown path returned404. That server was shut down afterward.

These are author-side structural/local-delivery checks, not a new remote fetch,
independent semantic review, cold-reader trial or usefulness result. No new
workflow, scheduler, remote model, visitor script, tracking, identity collection,
public write endpoint, hosting account or paid service is introduced.
