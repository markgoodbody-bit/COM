# Local reading copy

The first human reading surface for inheritance capsules. Experimental; not a live forum, an importer, or an identity system.

Before: validated records were available as JSON or terminal text.
After: a separately generated HTML copy offers linked originals, disputes and corrections, source claims and an input hash. Entry bodies are preserved as text, never interpreted as HTML. This adds presentation, not new evidence or schema.

From this directory:

```text
python human_view.py examples/benign.json new-reading-copy.html
python -m unittest test_human_view -v
```

The output must not already exist. Open the resulting HTML yourself in a browser. It has no JavaScript, forms, remote fonts/assets or external source links. The responsive CSS uses a single column below 700px; print styling retains entries.

Export is refused for `carry_forward=false`. A true flag still does not verify ownership, source permission or consent. Use only synthetic or already-public material in this experiment. Generated files persist until their holder removes them; sharing one shares its contents. No sanitisation or confidentiality guarantee is made.

## Verification, 28 September 2026

Five focused tests PASS: relation links resolve; HTML injection stays text; source URLs are not clickable; withheld/duplicate input rejected; existing output not overwritten; empty record displayed. Some checks share a test method.

Base: PR #683 commit `248f02f0361764e0d018c77cea01053ff2232eec`.
The initial combined 23-test run on Windows had one inherited failure: probe packet golden hash length 2117 instead of 2116 from CRLF checkout of PROBE_TASK.txt. Actual CLI stdout also translated LF to CRLF on Windows. The separately reviewed carrier repair PR #685 pins LF task checkout and binary UTF-8 stdout, with an actual subprocess golden-byte test. With that repair included and the existing task file refreshed to LF, the combined Windows suite passes **24/24**. No model dispatch. Older checkouts can retain CRLF until refreshed; the hash test catches this rather than silently normalising the input at dispatch.

Visual/browser QA is not established: browser policy blocked the local file URL; no alternate route was used. Automated HTML structure checks are not a substitute for visual inspection.

No changes to the live 8876/8877 rooms, their code, the parser, source fixtures or probe instructions. No network calls, publication, provider calls or schema additions.
