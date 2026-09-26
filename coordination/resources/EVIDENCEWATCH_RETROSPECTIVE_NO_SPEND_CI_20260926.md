# EvidenceWatch retrospective — no-spend pipeline gate

Date: 26 September 2026

Status: **HOSTED NO-SPEND GATE SUCCESS / V2 RAW-OWNER RECONSTRUCTION VERIFIED / PRIVATE-CHECKOUT LIMIT EXPLICIT**

Workflow:
`.github/workflows/evidencewatch-retrospective-pipeline.yml`

Hosted receipt:
- workflow run `36260538589`: **SUCCESS**;
- executable manifest: `research/evidencewatch_retrospective/brierley_major_vs_nochange_manifest_v2.json`;
- v1 preserved as pre-run source-integrity failure;
- packet SHA-256: `f12762d4867da361e9eb72e3a12c30e82b734f005b09d527b7b19c7aee2ae1cc`;
- key SHA-256: `75c64ca3235812b2cccf0d5dc2801698dd23f20a393f627106026d619eb299c9`;
- lexical AUCs: `0.799587`, `0.795455`, `0.793388` with 22+22 complete text pairs;
- synthetic conservative scorer test: TP 21 / FN 1 / FP 1 / TN 21 under one failed positive + one failed control;
- provider credentials/calls: none.
Purpose:

Exercise the frozen retrospective machinery end-to-end as far as COM's hosted CI can honestly reach, before any NVIDIA provider execution.

## Hosted gate covers

Pinned owner-file encoding handling: `abstract_scoring.csv` is read as strict Windows-1252 (`cp1252`). `all_pairs.tsv` contains at least one owner-source byte that is undefined even in cp1252, so the full table is read with cp1252 replacement enabled **only to reach the selected rows**; the packet/baseline builders fail if any selected preprint or published abstract contains a replacement character. Unrelated corruption elsewhere in the owner table therefore cannot silently enter the 44-case corpus.

The workflow:
1. checks out COM;
2. downloads only the two required public Brierley owner files from exact commit `a07c570c...` and verifies their Git blob identities (`abstract_scoring.csv = da5d6080...`, `all_pairs.tsv = 3c26344f...`);
3. compiles all Python retrospective scripts and runs `node --check` on the execution harness;
4. recomputes the frozen v2 22+22 selection from both pinned owner files, including clean text reconstructability;
5. reconstructs blinded packet + owner key from pinned `all_pairs.tsv` and checks their exact v2 SHA-256 identities;
6. recomputes trivial lexical baselines and asserts exact pre-model AUCs;
7. asserts the harness fails closed before provider access when the required EvidenceWatch checkout is absent;
8. creates a synthetic, structurally valid 44-case pre-unblind result;
9. exercises the frozen owner-key join/scorer;
10. proves the conservative failure rule:
   - one synthetic failed major-change case -> one strict false negative;
   - one synthetic failed no-change case -> one strict false positive;
   - available-case view remains secondary.

No output artifacts containing owner abstracts are uploaded.

## Private-repository ceiling

`markgoodbody-bit/evidencewatch` is private.

COM's ordinary GitHub Actions token is scoped to COM and is not assumed to have cross-repository private-read authority.

Therefore the hosted workflow does **not** pretend to execute the harness's successful exact-checkout dry run.

That gate remains local:

```text
HOSTED CI
-> harness syntax + fail-closed pre-provider behavior

LOCAL PINNED EVIDENCEWATCH CHECKOUT
-> exact HEAD/blob verification
-> successful dry-run plan
-> later, separately authorised live execution
```

Do not add a broad PAT or cross-repository secret merely to make the hosted badge look more complete unless that credential expansion is separately justified.

Preserve:

```text
HOSTED PIPELINE GREEN != PRIVATE CHECKOUT VERIFIED
PRIVATE CHECKOUT NOT AVAILABLE TO CI != HARNESS UNTESTED
SYNTHETIC SCORER TEST != MODEL RESULT
NO-SPEND GATE != LIVE RUN
```

No provider/model call, secret expansion, external contact or grant action is performed by this gate.
