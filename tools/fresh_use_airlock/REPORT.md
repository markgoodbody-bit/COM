# Codex constructive build report — fresh-use receiver airlock

## Outcome

Built a local, provider-free airlock that converts the frozen 7Q research
definitions plus preserved external source bytes into mechanically checkable,
neutrally aliased receiver cells.

It closes five preparation/evidence gaps:

1. **Tested object = named object.** Protocol, candidate, prompts, and case
   manifests are loaded directly from their full pinned COM commits and checked
   against declared SHA-256 values.
2. **URL != snapshot.** Packet construction refuses source references that do
   not resolve to preserved local bytes with a predeclared hash. Its private
   ledger binds raw bytes to a versioned deterministic extraction recipe,
   extracted bytes, a parity case-pack hash, and each complete cell-input hash.
3. **Arm identity stays evaluator-only.** Public random cell aliases are split
   from a permission-restricted private arm map. Public listing order is also
   randomised. The prepare event binds the exact hidden-map bytes, and both
   verification and unmasking enforce that binding before using arm identity.
4. **Failure/attempt evidence is append-only.** Answers and receipts are created
   once. Duplicate recording, post-hoc packet mutation, over-budget answers,
   malformed timestamps/exposure fields, and relabelled retries are rejected.
5. **Evaluation order is enforceable.** A two-cell comparison is frozen under
   aliases before arm unmasking. A local hash-chained transition log detects
   accidental mutation but is explicitly vulnerable to operator tail
   truncation/rewrite. `score` therefore emits a neutral freeze token, and
   tool-mediated unmasking requires those exact bytes at a full Git commit/path.
   The Git object prevents silent substitution of a previously anchored score;
   it is not a trusted wall-clock or proof that the operator did not inspect the
   arm map. Unmasking deliberately does not manufacture a final disposition.

Claude Code's threat-model review also produced bounded repairs:
- raw HTML can be transformed directly through visible-text normalization and
  frozen line selection in one replayable extraction recipe;
- native Windows now has a fail-closed DACL backend: current identity is
  resolved by SID, a protected current-user/System/Administrators ACL is
  installed with direct .NET directory/file access-control APIs rather than
  `Set-Acl`/`Get-Acl` module cmdlets, and an independent ACL read-back must
  exactly match owner, trustee, allow/rights, inheritance and propagation
  expectations;
- receipts classify tool-bound facts separately from operator attestations;
- the output budget is explicitly English-scoped and ZIP creation uses
  exclusive file creation.

The preparation order was also repaired. All configuration, pinned-object,
manifest, raw-hash, extraction and extracted-hash checks complete before the
private-storage guard. The guard still executes before the first bundle file is
written, so Windows permission failure cannot leave receiver or evaluator
artifacts behind.

Preparation also freezes a sorted case-to-source-ledger hash map. Verification
requires exactly one ledger per public case and joins ledger pilot/case identity,
case-pack, source identity, extracted member, hash and size to the exact packet
manifests before replaying raw-byte extraction. A rewritten, missing, extra or
semantically disconnected ledger is rejected.

Permission establishment and later permission verification are separate paths.
Creation installs and reads back the boundary. Existing-bundle commands only
read it: broadened POSIX modes or Windows DACLs fail without being silently
repaired by the verifier.

Observable burden retained by the receipt includes elapsed time, exact answer
bytes/Unicode words, reported token counts, source opens, clarifications,
terminology lookups, exposure state, and errors/truncation.

## What this enables now

Once exact official-source files exist, Codex/Framework can generate the two R1
receiver attachments (and later R2) without hand-editing prompts, leaking
evaluator notes, or naming arms in filenames. Mark's remaining action can be
reduced to voluntarily launching a clean receiver with the fixed sentence and
returning its answer plus factual run metadata.

The tool is equally usable for a consenting human receiver; it does not assume
that voluntary help must come from a model.

## Hard boundary still present

COM currently contains source identities/currentness witnesses, not the exact
third-party bytes needed for a receiver pack. This build intentionally did not
fetch and silently freeze those pages. R1 needs the selected RAIB/Network Rail
snapshots; R2 can use the immutable SEC filing alone or that filing plus one
explicitly frozen newsroom snapshot.

Raw snapshots and generated receiver packets are local/private run evidence by
default. Suggested COM integration should commit the manifest, hashes, and
extraction recipe—not third-party raw pages—unless licence/quotation policy
affirmatively permits inclusion.

No inference was dispatched. No provider spend was incurred. Codex, Claude Code,
and Framework were not used as receivers. TRACE and Mechanical Ethics were not
read or changed.

If a paid route is later selected, all four calls require separate one-use,
call-bound authorizations. This tool does not create, combine, consume, retry, or
infer those authorizations.

## Claim ceilings

The airlock improves reproducibility and prevents several contamination paths.
It does not prove receiver freshness, source sufficiency, evaluator independence,
domain correctness, 7Q usefulness, or project validity. New session remains
different from historically fresh receiver. A run can and should still end in a
null, adverse, burden-exceeds-value, case-not-discriminating, or inconclusive
outcome.

The Windows ACL backend is access control, not encryption. It does not defend
against compromise of the current account, administrators, Local System, the
kernel, backups, or offline media; administrators can take ownership. Those two
privileged built-ins are retained for normal OS operation and recovery. Unknown
trustees, inherited rules, ambiguous SID resolution, unavailable built-in
commands, and unverifiable read-back all stop execution. POSIX mode bits retain
their corresponding root/operator/storage-layer ceiling.

## Suggested COM integration

Integrate as a small `tools/fresh_use_airlock/` research utility, not as TRACE,
ME, Campfire Production, or project canon. Before merging:

1. have Claude Code independently review the code and threat model;
2. verify the exact protocol SHA already recorded in the config template;
3. choose and preserve the source bytes under the project's source/copyright
   policy, preferably storing hashes/receipts rather than republishing when
   redistribution is not permitted;
4. run only R1 first;
5. keep evaluator notes out of public cells;
6. retain first-attempt failures rather than retrying silently;
7. record the tool version/commit in any actual run manifest.

The tool should be deleted or simplified if the launch process remains too heavy
for the small question being tested.
