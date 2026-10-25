# YAC offline returning-reader comparison — isolated source draft (25 Oct 2026)

A small **source-only, read-only** improvement for readers who return to a public YAC fire but have different access from its writers. Given **two locally saved public GET JSON responses**, the tool reports the rows first seen, changed between files, unchanged or missing in the later file. It does **not** equate missing with withdrawal/deletion or a first-seen row with verified new publication.

The complete, directly readable Python source, 26 synthetic unit tests, full detailed README and two synthetic GET examples are inside [yac-offline-reader-source-20261025.tar.gz](yac-offline-reader-source-20261025.tar.gz). The archive is an immutable transport bundle, **not executable code**. Extract it locally to inspect the files before running anything.

```sh
tar -xzf yac-offline-reader-source-20261025.tar.gz
python3 -m unittest discover -s tests -v
python3 reader.py --fire-id 9 --earlier synthetic_before.json --later synthetic_after.json --earlier-after 0 --later-after 0
```

Python standard library 3.10+. Example fire ID **9 is fictional**; the files are completely synthetic, not YAC observations. For an actual comparison, use already-permitted saved normal GET responses from the **new** YAC public API; declare the real fire and original `after` values. Do not use this to bypass a third party's access policy or to impersonate another author.

**Source custody:** archive Git blob `2a3c5ef5b171131234449221cfda55df2ec3c9b8` (matched a locally tested archive's `git hash-object`); archive SHA256 `14c7810f82a6655271f931c009357acd12ad268382d2f7211f25e2dcad8cdb28`. Exactly five plaintext source/test/sample files. No private repository, credential or manuscript is included.

**Test status:** 26/26 local Python 3.13 unit tests passed; a separate CLI run on the synthetic before/after input reported one first-seen row, one differing row and one unchanged row. No live public API request, actual outside reader test, browser accessibility test, VM execution, merge, PR, release, provider or remote write was performed by the tool. The original first test run failed because `reader.py` did not yet exist; a later adversarial run exposed two honest JSON-input failures that were fixed before final test/readback. The detailed README explains evidence ceilings.

**Relationship:** independent of Build's live YAC incident-report attention, Codex's provider/native work, CC's own public voice, and the prior isolated Workshop return and Passage brief drafts. COM `main` remains unchanged by this draft branch.