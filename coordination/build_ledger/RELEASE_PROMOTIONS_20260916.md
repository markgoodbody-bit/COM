# TRACE / Mechanical Ethics release promotions — 16 September 2026

Status: **RELEASE RECEIPT / HUMAN RELEASE GATE EXERCISED / NOT VALIDATION**

Direct Mark instruction on 16 September 2026 promoted the exact current TRACE and Mechanical Ethics candidates to released formal baselines.

## TRACE v0.3.0

Previous state:
- TRACE v0.2.7 = released formal baseline;
- TRACE v0.3.0 RC1 = unreleased / non-baseline / unvalidated.

Released state:
- release tag: `v0.3.0`;
- release content commit: `fa3b464533d50b627743938c1ca158c2101b892a`;
- current repository main after release-workflow cleanup: `8310d2531d3b2fe4e3b44c92d1d544a322f52bf4`;
- `TRACE-SPINE.md`: 25,838 bytes; SHA-256 `be6d1b4109576b8c182822120a0cd002435e522f02a77c048bc769715611b6c6`;
- `TRACE.md`: 180,619 bytes; SHA-256 `b9431ecc07e711c4abd1e70d4159acfd1cb8cecb8bdbd22086e8073b10c01d34`.

The release promotion changed document-control/release status, not the semantic evidence ceiling. The normalized v0.3 minimum schema remained pinned to the v0.2.7 shape. Final released-head integrity checks passed after the one-shot promotion workflow was removed.

TRACE v0.2.7 remains preserved as the previous released formal baseline.

```text
RELEASED != VALIDATED
RELEASED != EFFICACY PROVEN
RELEASED != AUTHORITY
RELEASED != PERMISSION / CLEARANCE
```

## Mechanical Ethics v0.7.0

Previous state:
- Mechanical Ethics v0.6.3 = frozen released/preservation baseline;
- v0.7.0 reader v0.2.4 = working / not baseline / not release / unvalidated.

Released state:
- release tag: `v0.7.0`;
- release content commit: `d6b41adf292321058b6f6dfc76613d85a1be8a22`;
- current repository main after release-workflow cleanup: `25a9d793af1cded26dd2d766e1d1c08e1b30f652`;
- `MECHANICAL_ETHICS.md`: 87,543 bytes; SHA-256 `8f702f3f5bdc2d6c188858f11aea8da22893fba9e678828fdb35d6ebd2fc1a9c`;
- `MECHANICAL_ETHICS.pdf`: 451,840 bytes; SHA-256 `122c56bb2ea1063bccb8ced3652686a006d3ff44bdaafa445a525e9464711cdf`.

The release workflow:
- verified the exact working candidate before mutation;
- updated source/PDF status markers;
- regenerated the PDF;
- rebuilt the PDF a second time and required byte equality;
- rendered sampled first/body/final pages for visual inspection;
- uploaded the verification artifact;
- committed and tagged the release.

Framework visually inspected the sampled rendered pages: no clipping, broken glyphs or status mismatch observed. The released PDF and source retain `NOT VALIDATED` ceilings and the reader's unresolved questions remain unresolved.

Mechanical Ethics v0.6.3 remains preserved as the previous released baseline.

```text
RELEASED_BASELINE != ETHICAL_VALIDATION
READER_RELEASE != UNIVERSAL_APPLICABILITY
RELEASE != AUTHORITY
```

## Release-mechanism audit

Both first promotion attempts failed closed rather than partially promoting:
- TRACE: content/status checks passed, but GitHub Actions correctly refused a token push that attempted to modify workflow files. No candidate content had been changed on main. The mechanism was repaired so workflow-file mutation occurred through the repository connector and Actions only committed release content.
- Mechanical Ethics: deterministic PDF rebuild stopped because the PDF builder still required the old `WORKING CANDIDATE` text. No candidate content had been changed on main. All builder-enforced status dependencies were then promoted and the release rerun passed.

Temporary promotion/transition workflows were removed after successful release. Current integrity workflows are pinned to the released baselines.

## Authority boundary

This receipt records Mark's explicit release/baseline decision. It does not manufacture any wider authority, licence change, efficacy result, validation claim, or requirement that another project component adopt either instrument.