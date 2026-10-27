# COMHEADS local source locator (27 Oct 2026) — isolated Class A prototype

A small **offline, read-only** way to find and quote the exact dated sections of `continuity/COMHEADS.md` after acquiring a pinned file. Useful because the 27 October COM main copy has 299 LF-delimited physical lines and 102,004 UTF-8 bytes (31 H2 headings) despite the word “compact” in its heading, with several historical entries labelled “latest.” A fresh model need not infer status from a heading or replay the full text merely to find one relevant source span.

```sh
python3 locator.py /path/to/COMHEADS.md
python3 locator.py /path/to/COMHEADS.md --find 'correction'
python3 locator.py /path/to/COMHEADS.md --show 1
python3 -m unittest discover -s tests -v
```

The output is JSON for safe quoting/inspection. The index reports SHA-256 of **original raw UTF-8 bytes**, physical LF-based line positions and each section's exact byte hash. `--find` searches literal casefolded **lines in source order**; counts and truncation are explicit. `--show N` returns the complete exact section content (including original CRLF if present), not an AI summary. Ordinal 0 is preamble, when present; the first `##` section is ordinal 1. Code-fenced mock headings are ignored. Invalid UTF-8, missing ordinals, oversized files (1 MiB cap) and blank queries fail closed.

**Limits:** Not a GitHub reader, browser or live COM connector. It only reads the explicitly named local file, uses Python standard library and never fetches, executes document instructions, modifies files, contacts accounts or starts VM work. It does not decide which dated entry controls, distinguish genuine from claimed authority, validate links, classify semantic supersession, discover new issue bodies/comments, check source truth or guarantee that lexical search finds every relevant meaning. A caller must pin the original COM commit and verify current owners separately; a SHA matches **bytes, not independent custody or truth**. Fenced-heading recognition covers conventional backtick/tilde Markdown fences, not embedded HTML semantics. The tool is optional and **not installed/integrated on COM main**.

The specific original source boundary for this design was COM main `33f0f02c54b5b223da51542f241ac08e5e2cb875` (27 October 2026, 10:23 UTC), `continuity/COMHEADS.md` Git blob `0a0838cb663c1954db237f2f97988b237497d1de`, as read through the connected GitHub source connector. The isolated source package does not contain a private or archival COMHEADS copy. Work remains subordinate to Build and the source-work charter #887.
