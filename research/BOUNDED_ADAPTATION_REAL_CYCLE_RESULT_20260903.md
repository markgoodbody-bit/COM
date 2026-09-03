# Bounded Adaptation v0 — first real-cycle result

Status: **USE-DRIVEN TRIAL / NON-CANONICAL / NO ACTIVATION**  
Date: 2026-09-03

## Question

Can the bounded-adaptation v0 contract represent an actual Framework build cycle without inventing evidence, hiding uncertainty, understating authority, or requiring a special bypass?

## Immediate use-driven failure

The first attempt could not honestly represent the cycle.

The cycle had directly used COM PRs #86, #87 and #88. The receipt schema exposed lane-specific source IDs `PR86` and `PR87`, but no honest source type for PR #88. Encoding #88 as `EXTERNAL_PUBLIC_SOURCE` would have been false; omitting it would have made the basis incomplete.

That was a real-use defect, not a synthetic fixture failure.

Minimum repair:

- add generic `PROJECT_PULL_REQUEST` source type;
- keep source identity in `coordinate_hash` / `domain_hash` rather than baking current PR numbers into the schema;
- rebind the profile to the changed receipt schema;
- preserve legacy `PR86` / `PR87` values for compatibility rather than forcing a migration merely to prove the point.

Exact repaired identities exercised by CI:

- receipt schema SHA-256: `89607c3e0364f213e895a78161a34eb56cb226bf200e1dcd8e00e26d9ca5b28d`;
- profile SHA-256: `6195e926e52232248001e45c50b3884acc7c3ac6c5799ceef93a441725eeed68`;
- constitution SHA-256: `6cb67d151d50cfe2268c055da15d9339ace849c1b2ef487834b823eb61457805`.

## Real receipt

`research/adaptation_cycles/BAL_20260903_002.json` records the actual bounded build cycle that:

- reacquired and reviewed current PR #86/#87/#88 state;
- received exact-head contract passes on #86 and #87;
- froze #86 against further validation-for-validation's-sake;
- cleaned #87's deletion-gate regression so it reaches the intended refusal;
- discovered and repaired the lane-specific PR source vocabulary;
- corrected coordination metadata;
- left PR #88 awaiting exact-current-head independent review.

The receipt records:

- `result = MOVED`;
- selected moves `REVIEW`, `BUILD_REVERSIBLE`, `CORRECT_COORDINATION`;
- authority ceiling `B` rather than pretending shared coordination writes are Class A;
- `APERTURE_RECEIPT_PENDING` as an unresolved unknown;
- the bounded-adaptation lane age rather than treating activity as proof that the lane is not old;
- `WARN` for validation-loop, infrastructure-theatre and Framework-bottleneck anti-drift checks.

Those WARNs are deliberate. A useful receipt must be able to report that a productive cycle is also showing signs of the failure modes it is meant to resist.

## Executed result

GitHub Actions run `33743553110` passed on both `windows-latest` and `ubuntu-latest`.

The run exercised:

1. the synthetic/hostile contract fixtures;
2. the clean deletion-gate refusal;
3. the real `BAL_20260903_002` receipt against the exact repaired schema/profile/constitution.

The real receipt required no validator exception or special-case acceptance.

## What this establishes

It establishes a narrow useful property:

> the v0 receipt can describe at least one real reversible build/coordination cycle, including warnings and pending uncertainty, after one source-typing defect was exposed and repaired by use.

It does **not** establish:

- autonomous continuation;
- that Mark is no longer the clock or initiator;
- that the loop reduces Mark's cognitive/coordination burden;
- that self-reported public-read/repository-write counts are independently measured;
- that every future project source is representable;
- safe external contact or deletion;
- permission to activate a daemon;
- merge necessity;
- TRACE/ME validity or mutation.

The cycle itself was initiated by Mark saying `build`, and Framework remained the main integrator. Therefore the real trial does not satisfy the larger autonomy/burden objective merely because its receipt validates.

## Next useful boundary

Do not add more synthetic machinery merely because this receipt passed.

The next useful evidence is another ordinary cycle in which the receipt is produced without changing the contract first, preferably after a materially different trigger or aperture return. If ordinary use repeatedly forces schema edits, v0 is overfit and should be redesigned or retired. If receipts remain valid but do not reduce Mark's transport/supervision burden, the contract should not be promoted merely for internal consistency.
