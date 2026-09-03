# Local Continuity Capsule v1 — exact-current-head review target

Review the PR #86 current head, not any earlier head.

Required checks:

1. Reproduce exact UTF-8/LF SHA-256 for schema and profile.
2. Confirm `profile.capsule_schema_sha256` equals the exact schema digest.
3. Confirm profile and schema material-delta vocabularies/cardinalities agree.
4. Confirm profile and schema active-condition vocabularies/cardinalities agree.
5. Run `python research/validate_local_continuity_capsule_v1_contract.py` and independently try to defeat its stale-binding negative fixture.
6. Treat the older candidate prose as historical where the 2026-09-03 binding-repair receipt explicitly supersedes stale exact hashes/code counts.
7. Look for any remaining semantic contradiction that a schema-valid capsule can exploit.

Return only `PASS | REPAIR_CONTRACT | DELETE` with reproducible evidence. No merge, outbox retarget, publisher activation, credential use, spend or authority expansion follows from review.
