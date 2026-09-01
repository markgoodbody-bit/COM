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

No Python packages or network access are used.

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
instructions.

After a receiver returns, complete its generated receipt template and save the
answer as UTF-8 text:

```bash
python freshuse.py record \
  --bundle run-001 \
  --alias cell-0123456789ab \
  --receipt completed-receipt.json \
  --answer receiver-answer.txt
```

`record` verifies the packet and validates the format of timestamps, exposure
enums, counts, and the 700-word ceiling. This v1 requires the receipt to declare
English (`en`) and rejects non-Latin letter scripts; another language requires a
separately defined counting policy. Receiver identity, exposure, timing, token, and interaction
fields remain operator attestations. The output receipt lists those separately
from fields the tool mechanically checks or derives.

It writes the exact answer and receipt using create-only semantics. A second
record for the same cell is rejected while the complete local bundle is
retained.

After both cells for a case are recorded, an evaluator compares the aliases
without seeing the private map. Copy `examples/blinded-score.template.json`,
fill it, and freeze it:

```bash
python freshuse.py score --bundle run-001 --score R1-score.json
python freshuse.py unmask --bundle run-001 --case R1
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
- On POSIX systems the tool applies restrictive modes to the private directory
  and private files. On Windows it does not claim that `chmod` establishes an
  ACL: private-map confidentiality is procedural unless the operator separately
  configures and verifies Windows access control.
- One bundle contains first attempts only. A failure is evidence; it is not
  silently replaced. A retry requires a new cell/package and explicit authority
  outside this v1 tool.
- Preparation writes an integrity manifest covering the public packets,
  receipt templates, private arm map, and private source ledgers. Successful
  `prepare`, `record`, `score`, and `unmask` operations append a hash-chained
  line to `evidence/log.jsonl`. Unmasking requires a matching prior score event.
  The verifier detects missing or changed prepared/logged artifacts and ordinary
  delete-and-redo attempts when the complete bundle remains intact.
- This local log is ordering evidence, not an external timestamp or independent
  witness. An operator who controls the whole bundle can erase or replace both
  artifacts and log. Preserve the complete bundle in a separately governed or
  versioned store if stronger chronology is required.

## Important ceilings

This makes the transport more reproducible; it does not make a receiver fresh.
The operator must still record historical exposure honestly. A Temporary Chat,
new session, or new alias is not proof of independence.

This does not establish domain correctness, efficacy, validation, project
survival, canon, or authority. It deliberately permits a null or adverse result.
No run should be described as independent if the scorer constructed 7Q; use the
protocol's `PROJECT-PARTICIPANT / CONTAMINATED` ceiling where applicable.

The tool is deliberately substantial for a small pilot because the same
airlock is intended to be reused across Stage 0 and later bounded tests. If that
reuse does not happen, simplify or remove it rather than treating maintenance
burden as automatically justified.

This v1 never spends or dispatches. If a later paid dispatcher is built, each of
the four intended calls needs a separate one-use, call-bound authorization. A
failed or ambiguous call must not be silently retried under the same authority.

## Test

```bash
python -m unittest discover -s tests -v
```
