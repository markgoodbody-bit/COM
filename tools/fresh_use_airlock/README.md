# Fresh-use receiver airlock

This is a small, standard-library-only toolchain for the 7Q fresh-use research
protocol. It assembles frozen receiver cells and preserves a checkable evidence
trail around a run. It does **not** dispatch inference, call a provider, browse,
score answers, or mutate TRACE/Mechanical Ethics.

The tool exists to help a voluntary fresh receiver encounter one bounded case
without turning Framework, Codex, Claude Code, or Mark into the reasoning relay.
It keeps construction and judgment separate:

```text
PINNED PROJECT TEXT + PRESERVED EXTERNAL BYTES
-> HASH CHECK
-> NEUTRAL CELL PACKETS + SEALED ARM MAP
-> VOLUNTARY FRESH RECEIVER
-> FIRST-ATTEMPT RECEIPT + BURDEN
-> BLINDED HUMAN/INDEPENDENT SCORING FREEZE
-> UNMASK RECEIPT
-> BOUNDED HUMAN DISPOSITION
```

## Requirements

- Python 3.10 or newer;
- Git;
- a local COM checkout containing the pinned commits;
- exact local snapshots of every external source supplied to receivers.

No Python packages or network access are used. POSIX hosts verify exact `0700`
directory and `0600` file modes. Native Windows uses built-in `whoami.exe` plus
Windows PowerShell/.NET ACL facilities. It resolves the current account to one
unambiguous SID, installs a protected DACL, and then independently reads the ACL
back. Both operations use the direct .NET directory/file access-control APIs;
they do not depend on the `Set-Acl` or `Get-Acl` module cmdlets. The read-back
must show the current user as owner and exactly three
explicit `Allow FullControl` trustees: the current user, Local System, and the
built-in Administrators group. Inheritance, duplicate/missing/unexpected
trustees, deny rules, wrong rights or propagation, malformed output, unavailable
commands, or an ambiguous identity fail closed.

Create a source receipt and inspect the extracted bytes before putting its
fields into the pilot config:

```bash
python freshuse.py source-receipt \
  --raw snapshots/raib-wickford.html \
  --source-identity "exact URL; retrieved 2026-09-01T...Z" \
  --display-name raib-wickford.txt \
  --mode html_visible_text_v1 \
  --output snapshots/raib-wickford.receipt.json \
  --extracted-output snapshots/raib-wickford.preview.txt
```

The receipt command is local and create-only. It does not retrieve the source.
Review the preview for missing context before authorising it as receiver input.
For a noisy HTML page where only pre-frozen visible-text lines are required,
use `--mode html_visible_text_line_ranges_v1 --ranges '[[113,151]]'`. This
composite recipe binds the final bounded receiver text directly to the captured
HTML bytes, so later `verify` replays both extraction stages.

## Commands

Prepare a bundle after filling a copy of `examples/pilot-config.template.json`:

```bash
python freshuse.py prepare --config pilot-config.json --output run-001
python freshuse.py verify --bundle run-001
```

Only files under `run-001/public/cells/` are receiver attachments. Never upload
`private/arm-map.json`; it contains the evaluator-only arm mapping.

The public launch register supplies the same launch sentence for every cell.
The packet itself says not to browse, follow links, or treat source material as
instructions. Both the launch sentence and `START_HERE.md` require an English
answer; the receipt's language value remains an operator attestation rather
than automated language detection.

After a receiver returns, complete its generated receipt template and save the
answer as UTF-8 text:

```bash
python freshuse.py record \
  --bundle run-001 \
  --alias cell-0123456789ab \
  --receipt completed-receipt.json \
  --answer receiver-answer.txt
```

`record` verifies the packet, timestamps, exposure enums, counts, and 700-word
ceiling. It writes the exact answer and a derived burden receipt using
create-only semantics. A second record for the same cell is rejected.

The 700-unit cap is explicitly scoped to English-language answers and uses the
versioned `english_unicode_word_units_v1` counter. Receipts also record UTF-8
bytes, Unicode scalars, non-whitespace Unicode scalars, and provider-reported
tokens when available. It is not a cross-language budget; a non-English answer
is rejected for this pilot rather than treated as comparable.

After both cells for a case are recorded, an evaluator compares the aliases
without seeing the private map. Copy `examples/blinded-score.template.json`,
fill it, and freeze it:

```bash
python freshuse.py score --bundle run-001 --score R1-score.json
```

`score` emits `evidence/score-freeze-tokens/R1.json`. Before unmasking, commit
those exact neutral token bytes to a content-addressed Git object that the
evaluator cannot silently replace. Then identify that full commit/path:

```bash
python freshuse.py unmask \
  --bundle run-001 \
  --case R1 \
  --anchor-repo /path/to/anchor-repository \
  --anchor-commit 0123456789abcdef0123456789abcdef01234567 \
  --anchor-path research/fresh_use/anchors/R1.json
python freshuse.py verify --bundle run-001
```

Unmasking does not assign a result. It joins the frozen comparison to arm
identity and leaves `final_disposition` empty for bounded adjudication under the
protocol's signal, null, adverse, exposure, and authority ceilings.

## Safety and evidence rules

- Full 40-character Git commit identities and SHA-256 hashes are compulsory.
- Experiment-owned Markdown must be exact UTF-8/LF bytes.
- A URL is never accepted as a source snapshot. Each receiver source must be a
  local raw file with a predeclared SHA-256, versioned deterministic extraction
  recipe, predeclared extracted SHA-256, and source identity.
- The private source ledger binds `raw bytes -> extraction recipe -> extracted
  bytes -> case-pack hash -> cell-input hash`. Raw snapshots remain local/private
  run evidence by default; do not turn COM into a mirror of third-party pages.
  Preparation freezes a sorted case-to-ledger hash map in the first event. The
  verifier requires exact case coverage and joins each ledger's identity,
  case-pack, source identity, extracted member, hash, and size back to both
  receiver packets.
- ZIP cells use sorted members, fixed timestamps, and no compression so the
  same members produce stable bytes.
- Public aliases are random and do not contain arm labels.
- Private-map permissions are verified before the first bundle file is written.
  All config, pinned project text, case-manifest, extraction, raw-source, and
  declared-hash checks run before that guard, so an input defect is reported as
  such rather than being masked by an unavailable storage backend.
- On POSIX the boundary is exact mode bits. On native Windows it is a protected,
  read-back-verified DACL for current user + Local System + built-in
  Administrators. The current user is owner; no other trustee is accepted.
  Permission installation occurs only while creating new protected artifacts.
  Loading, recording, scoring, unmasking, and verification use read-only
  permission checks: a broadened mode or DACL stops the command and is never
  silently repaired.
- The initial hash-chained event freezes the evaluator-only arm-map hash as well
  as the source-ledger hashes. Verification and unmasking reject any later arm
  mapping change before using the map.
- Each receipt distinguishes tool-bound hashes/measurements from
  operator-attested provider, exposure, timing and burden metadata. Hashing an
  attestation binds its bytes; it does not make the claim true in the world.
- One bundle contains first attempts only. A failure is evidence; it is not
  silently replaced. A retry requires a new cell/package and explicit authority
  outside this v1 tool.
- A local hash-chained event log enforces one visible sequence of preparation,
  first-attempt records, scoring and unmasking. It detects accidental mutation,
  but an operator can truncate, delete, rewrite or rebuild its tail. It is not
  an external timestamp or independent attestation.
- Tool-mediated unmasking therefore requires the exact neutral score-freeze
  token to match a full Git commit/path. The immutable Git object prevents a
  previously anchored score from being silently substituted; it still does not
  establish a trusted wall-clock time or prove that nobody inspected the arm
  map.
- The verifier detects packet, hidden-map, source-ledger, answer, receipt, and
  frozen-score changes.

## Important ceilings

This makes the transport more reproducible; it does not make a receiver fresh.
The operator must still record historical exposure honestly. A Temporary Chat,
new session, or new alias is not proof of independence.

The storage guard is a local access-control boundary, not encryption or a
defence against a compromised account, kernel, administrator, backup agent, or
offline disk reader. Windows administrators can take ownership, and Local
System/Administrators are retained for operating-system and administrative
recovery. A filesystem or PowerShell environment whose ACL state cannot be
read back in the expected form is unsupported and fails closed. POSIX mode bits
have the analogous operator/root and storage-layer ceilings.

This does not establish domain correctness, efficacy, validation, project
survival, canon, or authority. It deliberately permits a null or adverse result.
No run should be described as independent if the scorer constructed 7Q; use the
protocol's `PROJECT-PARTICIPANT / CONTAMINATED` ceiling where applicable.

This v1 never spends or dispatches. If a later paid dispatcher is built, each of
the four intended calls needs a separate one-use, call-bound authorization. A
failed or ambiguous call must not be silently retried under the same authority.

## Test

```bash
python -m unittest discover -s tests -v
```
