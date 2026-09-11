# COM build ledger

A small **recorded snapshot**, not a live dashboard, scheduler, permission system or reputation score. It does not contact GitHub, execute a next action, monitor an owner or adopt anything into Production.

Read [BUILD_STATUS.md](BUILD_STATUS.md) for the generated view. Edit `ledger.json`, not the rendered file. Keep the build contract as historical assignment evidence.

## Use

From this directory, with Python 3.10 or newer and no third-party packages:

```text
python validate.py
python render.py --output BUILD_STATUS.md
```

Both commands reject invalid input with a nonzero exit code. Rendering validates first. Without `--output`, it writes Markdown to stdout. An alternative ledger path may be supplied as the first argument. Generation does not refresh observations.

## Recording work honestly

`observed_head` is the exact Git commit read, not a prediction of the current branch. `observed_at` dates that observation, while `recorded_at` dates this snapshot. A building lane can have uncommitted work after its observed base; the field must not imply that work was already delivered. Do not replace unknown activity with an optimistic status. A dispatch supports `queued`; an owner claim or observed implementation can support `building`. Neither establishes completion.

`queued` claims no active ownership. `building` and `waiting` reserve the named mutation scope. `waiting` requires a concrete blocker and the event that removes it. `handback` means the artifact/receipt is delivered but the closure decision remains elsewhere; `closed` means the named lane ended, not that all related work or all consequences are resolved. Both keep their receipt. For example, D047's publication lane can close while a separate visual witness is still pending.

Before changing a lane, read its source and exact branch; preserve closed entries and earlier states in Git. A takeover is not made legitimate by changing `owner` in JSON. It needs an external coordination decision, an exact-head read, a stopped/transferred previous claim and a recorded source. This ledger neither implements nor replaces the separate recovery companion.

Hand-back events describe observable deliveries, not assumed human agreement. New work needs its own scope. A successful build, a validator pass, or a receipt does not grant more authority. A receipt also cannot establish that somebody read it.

## Ownership checks

Write scopes are concrete repository-relative files or directory prefixes. No globs, traversal, absolute paths or whole-repository root shorthand. A directory claims its descendants. Comparison is conservatively case-insensitive, including across different branches of the same repository: branch isolation does not settle competing ownership of the same intended content. Split disjoint paths or resolve the overlap outside this tool; do not invent a branch name to bypass it.

Active mutating claims on the same or ancestor/descendant paths are rejected. Waiting owners still reserve their scope until a separately evidenced transfer or closure. `no_touch` is explanatory prose, not an enforceable access-control list. Physical Git access, semantic dependencies, symbolic links, cross-repository dependencies and dishonest or omitted entries are outside this check. Disjoint paths can still conflict in meaning.

## Schema and limits

`schema.json` is the structural JSON Schema contract. The stdlib validator supports only its declared subset: local `$defs` references, type, required/properties, additionalProperties, const/enum, array items/count/uniqueness, text length/pattern and date-time/URI formats. It is not a general JSON Schema engine. It additionally rejects duplicate JSON keys, empty text, invalid scope paths, duplicate work IDs, observations later than the snapshot, incomplete waits/receipts and overlapping active ownership. HTTPS evidence URLs and timezone-bearing whole-second timestamps are required.

Validation does not check that URLs exist, that their authors are authentic, that a head is still current, or that a claim is true. The renderer always says **observed state**, displays observation times and exact heads, and instructs the reader to refresh before acting. There is no invented freshness threshold, check-in interval or green currentness badge.

The ledger's own observation may name an earlier implementation commit rather than its containing commit: a file cannot contain the hash of the commit containing itself. The final hand-back receipt supplies the delivered head externally. Do not manufacture a self-hash.

This is coordination infrastructure only. No empirical benefit, comprehensive task inventory or authority claim is established.
