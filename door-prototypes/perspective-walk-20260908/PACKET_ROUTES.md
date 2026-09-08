# Packet-relative navigation repair — 8 September 2026

Source-only repair following the compact entrance at `6c037c8e3779f19e633ae5f549927a078a85a075`.
This is not a live deployment or reader-benefit receipt.

## Reproduced defect

The complete JSON packet embedded example references such as `case.json`, but
was served from `explore/packet.json`; its actual example files live under
`explore/example/`. No explicit base distinguished those nested references.
The general JSON-link check excluded the packet. Ordinary document-relative
resolution therefore targeted missing files. One new test failed in sixty
subtests: twenty references tested under domain, pinned-raw and offline-file
bases. These are not sixty independent defects or outside-reader observations.

## Repair

The builder deep-copies the example data and rebases only `case`, `shared_case`
and `next[].path` references to `example/<name>.json` for the two complete
packets. It leaves their source files, facts, unknowns, interpretations and
external references unchanged. Both packet forms explain the reference context
and retained historical source-status labels. Reading the already embedded
facts requires no fetch. Unrecognised example paths are refused.

The existing source-preservation test now compares after reversing that explicit
packaging change; it was not removed. Six new tests cover link resolution,
Markdown/JSON agreement, source preservation, copy isolation and invalid paths.

## Build and integration

Run `python -m unittest -v test_build test_arrival test_packet`, then the existing
`python build.py --output NEW_EMPTY_STAGING_DIRECTORY` command.

Executed locally: 42 tests passed; all 60 generated files byte-matched through a
temporary loopback HTTP server; a missing route returned 404; server stopped.
Relative to the compact-entrance output, 56 files are byte-identical. Only
`packet.json`, `packet.md`, the packet-size line in `llms.txt`, and the resource
hash/size map change. No output files are added. The small entrance and all
individual readings remain unchanged.

Expected output-tree SHA-256:
`1dfd219f6c5156d17cab323393b4a1acea2c34609adb1d6ff5e85a9250f0a80f`.
Library SHA-256 remains
`ca8039e79c64ecb0c7f005c112b4387eae8eec2d3df017b50b5677791f2027f3`.

Codex remains the live publisher. Reacquire current publication and in-flight
operations; incorporate this into the existing compact-entrance integration or
apply it subsequently if that publication is already complete. Preserve all
unrelated root assets, seed, CNAME, DNS, account settings and source terms. Do not
publish the COM source branch as the site or rerun fixed-base historical jobs.
Normal public retrieval and HTTPS readiness remain separate checks.
