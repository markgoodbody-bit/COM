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

No Python packages or network access are used. This v1 requires a POSIX
filesystem boundary (Linux/macOS/WSL). Native Windows execution fails closed
because `chmod` is not a tested Windows confidentiality control for the private
arm map.

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
- ZIP cells use sorted members, fixed timestamps, and no compression so the
  same members produce stable bytes.
- Public aliases are random and do not contain arm labels.
- Private-map permissions are restricted where the filesystem supports it.
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
- The verifier detects packet, answer, receipt, and frozen-score changes.

## Important ceilings

This makes the transport more reproducible; it does not make a receiver fresh.
The operator must still record historical exposure honestly. A Temporary Chat,
new session, or new alias is not proof of independence.

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
