# EvidenceWatch retrospective — no-spend pipeline gate

Date: 26 September 2026

Status: **HOSTED NO-SPEND GATE PREPARED / PRIVATE-CHECKOUT LIMIT EXPLICIT**

Workflow:
`.github/workflows/evidencewatch-retrospective-pipeline.yml`

Purpose:

Exercise the frozen retrospective machinery end-to-end as far as COM's hosted CI can honestly reach, before any NVIDIA provider execution.

## Hosted gate covers

The workflow:
1. checks out COM;
2. downloads only the two required public Brierley owner files from exact commit `a07c570c...` and verifies their Git blob identities (`abstract_scoring.csv = da5d6080...`, `all_pairs.tsv = 3c26344f...`);
3. compiles all Python retrospective scripts and runs `node --check` on the execution harness;
4. recomputes the frozen 22+22 selection from owner `abstract_scoring.csv`;
5. reconstructs blinded packet + owner key from pinned `all_pairs.tsv`;
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
