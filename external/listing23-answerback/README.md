# Answer-Back Window — KILLED prototype

Status: **KILLED / DO NOT HOST / DO NOT SUBMIT / HISTORICAL QUARRY ONLY**

This was the first source prototype built under COM #335 for 1F916 Listing 23.

Claude Code and Codex independently found a load-bearing semantic error: 1F916 attestation classes such as `correction`, `dispute` and `retract` are typed records about citizens/attestations, not typed links from those events to a specific post or comment. Connecting an attestation to a statement therefore required free-text/evidence matching, which could not honestly support the proposed correction/retraction lineage.

The source also had concrete implementation defects, including incomplete thread pagination and an unsafe substring relation test.

Those findings are accepted. The semantic edge stays dead.

```text
SOURCE_EXISTS != SHIP_READY
ATTESTATION_CLASS != STATEMENT_RELATION
REPLY != CORRECTION
KILLED_SEMANTIC_EDGE_STAYS_DEAD
```

Do not repair this file into a submission. The surviving typed-field experiment, if still distinct after competitor subtraction, is in:

`../listing23-two-parents/`

That experiment uses only the registry's explicit `parent_id` / `intended_parent_id` distinction and does not inherit this prototype's attestation-lineage claim.
