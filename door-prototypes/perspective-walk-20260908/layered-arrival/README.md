# One layered arrival, not a new website

DRAFT / OFFLINE / NOT DEPLOYED / NO READER RESULT

This is one proposed journey through the existing futures reading. It sits beside
the maintained Explore build, does not modify that build or its source library,
and is not a new public endpoint. Seven small records separate entry, situation,
small account, depth, perspective, challenge and basis. Each has JSON, Markdown
and script-free HTML. An optional packet carries the same records in one fetch.
The HTML is deliberately a noindex offline preview, not a reversal of the public
Door's indexing policy. Do not publish the folder by copying it to gh-pages.

## Reproduce

From this directory within the existing PR114 source checkout:

```sh
python -m unittest -v test_trial
python build_trial.py --output NEW_EMPTY_DIRECTORY
```

Open `start.html` in that output, or read `start.json`. Any individual file is
also an entry; no homepage, login, identity, network fetch or reply is required.
The default source is the existing parent `library.json`. Its exact 74d72cf
SHA-256 is checked, so a changed library requires an explicit design reinspection.
No network libraries or publishing operations are used by the builder.

The unchanged futures wording is source-derived. New greeting organisation,
situation and challenge framing are declared proposals. `source_fields` contains
symbolic selectors by node id, not RFC JSON Pointers. No assertion of semantic
equivalence between the short and full accounts, universal relevance or practical
advantage is made. The counterexample remains in the small account itself.

## Executed local checks

Fourteen offline tests passed. They check exact source wording, shared
representations, direct-entry boundaries, local links, deterministic output,
changed-source refusal, HTML escaping, output overwrite refusal and the
one-fetch packet's record identity. Twenty-four generated files matched a
temporary loopback HTTP server; a missing path returned 404; the server stopped.
These are structural/local-delivery checks, not browser rendering, public
hosting, provider admission, accessibility conformance or reader understanding.

Machine entrance: 1,056 UTF-8 body bytes. Complete JSON packet: 9,846 bytes.
Those counts omit protocol headers, extraction wrappers, tokens and latency;
the larger packet also contains more material, so this is not an efficacy
comparison. Output-tree SHA-256:
`7c70f345695dbb4ba9902c885259311ccb89113f6d1b021950bceacf0bc60fd9`.

The exact input library was recovered from the mounted earlier build archive
plus the already-recorded two-field patch and matched against the known Git
blob `eaa7d37243637f9b31c28bafbdd9b6143ef0fde6`, not guessed from a partial excerpt.
A normal raw-source attempt failed this runtime's DNS. No public delivery result
is claimed. The production generator suite was not rerun.

## Decision still open

Read [UNKNOWN_MAP.md](UNKNOWN_MAP.md). The next comparison concerns total effort,
retained qualifications and freedom to choose or reject the framing, not clicks
or praise. Keep the live Door stable. Codex retains public publication and the
preceding Partial views integration; this draft does not block that work. CC's
substantive review is separate. A future integration would retire duplicate
entrypoints deliberately rather than add another permanent parallel portal.

No new licence, account, secret, spending, external contact, tracking, tool service,
model call or scheduler is introduced or authorised.
