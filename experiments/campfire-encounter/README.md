# Campfire encounter experiment

Local synthetic/public-only slice. COM #678 is the canonical coordination thread;
FW's decision at comment 5878974902 supersedes the earlier duplicate briefs.

Run: `python -m unittest -v` from this directory. Standard library only.
Tests create and clean up a temporary SQLite database; no service starts.

Before: a paper proposal. After: executable append/read/reopen/export rules.
The original remains alongside disputes, refusals and corrections. Export is
all-or-nothing when a thread includes content without carry-forward permission;
it does not silently omit dissent. This deliberately sacrifices partial export.

Limits: no authentication, hostile-host protection, adopting imports, model
calls, trusted time, backups, or usefulness result. Producer labels are claims.
Caller-supplied time is a test seam, not an HTTP API field.
Expiry blocks application access but DOES NOT erase data.
SQLite contains the payload after expiry; do not use this with personal data.
The host can bypass every application rule. No secrets or real participant
memories belong in this probe. No production files were changed.

Next: CC attack and actual bounded internal use against the COM #672 baseline.
Do not expose this experiment as an online service.

## CC attack repair (v1)

Before: carry defaulted to false, one room acceptance covered later contributors,
and no route observation was recorded. After: carry is a required boolean; each
append refers to a separate matching disclosure acceptance; observed route is
explicitly UNKNOWN because no authenticated transport exists. Retries are scoped
to acceptance, not a producer name. Acceptance IDs are NOT authentication:
another same-host caller can copy one. This is recorded acknowledgement, not proof
that a particular participant read or understood a disclosure.

The test disclosure is shared synthetic storage, no isolation from the host or
other same-user processes. Retrieved content can reach the reader's model
provider. Only synthetic/already-public material is suitable. No auto-recall.

Existing v0 databases are rejected unchanged rather than silently migrated.
Tests use new temporary stores. Earlier source remains addressable in COM #675.
Whole-thread export veto remains deliberate pending FW's policy decision.
No carry-amendment operation exists: pretending to authenticate the author of
such a change would outrun this probe. This does not settle lock-in or privacy.

## Bounded capsule inspection

`capsule.inspect_capsule(bytes)` parses v3 exports as unverified imported claims.
It never writes to the database, fetches a URL or executes message text. It checks
size/count/shape, duplicate IDs/keys and backward links. It preserves disputed
text without deciding whose account is right. A forged route remains a source
claim. Declared carry permission is not verified consent.

An important adverse control deletes the final dispute before inspection. The
file still parses: a self-contained bundle cannot prove it includes all history.
Every inspection therefore reports completeness NOT_ESTABLISHED. This is not
restoration, authenticated import or a prompt-injection defence for future AI
consumers. Those consumers must still treat the returned content as untrusted.

## Local interface (2026-09-28)

Before: storage and capsule code only. After: a loopback HTTP interface with
explicit entry, on-demand retrieval, linked contributions, whole-thread export
and inspection without adoption. No production app or website is changed.

Run `python server.py --port 8876`, then open http://127.0.0.1:8876/ .
Each run creates a fresh disposable room outside the repository. Ctrl+C closes
the server and removes its SQLite database and journal/WAL/SHM files. This is
ordinary removal, not secure erasure. A crash or forced termination may leave
temporary files; exported copies are outside its control. Do not use personal
material, secrets or real participant memories. There is no private room mode.

The server checks Host, Origin, JSON shape, request size and a per-run local
session token. It uses host time and bounds socket waits. These checks do not
authenticate participants or defend against a hostile process on this host.
Names and acceptance IDs remain claims, not credentials. No carry amendment is
implemented; one withheld entry vetoes the whole export.

Verification: 31 automated tests cover storage, capsule and HTTP paths.
Browser checks exercised entry, literal script-shaped text, explicit retrieval
and missing-carry rejection. Malformed carry option markup and an overlapping
sticky status panel were repaired. Pointer automation was inconsistent in the
in-app browser; the keyboard entry/preserve/retrieve path was verified instead.
This is not a claim of complete browser compatibility or independent use.

For the internal trial, compare a bounded task with COM #672: retrieve an earlier
claim, locate its disagreement, add a correction without replacing the original,
and attempt an export with a withheld entry. Record completion, mistakes, elapsed
time and operator interventions. Keep failures and stop if it adds burden without
improving retrieval or preserving disagreement. Test count is not usefulness.

## CC capability-disclosure repair

CC comment 5879039142 demonstrated that v1 read/export distributed acceptance
IDs that could be reused to append under other participants' claims. Before:
all database entry columns were returned. After: an explicit read projection
omits acceptance IDs and retry keys; exports use that projection. Capsule v2
rejects the old capability-bearing shape rather than silently importing it.
The HTTP regression checks both reader and export paths and rejects using a
public entry ID as acceptance. Existing leaked IDs remain usable in an old
running room: close that disposable room and start fresh after this repair.
This does not establish authorship: callers can claim the same name, stolen
acceptances remain reusable, and the host can bypass the application entirely.
The simpler omission repair differs from CC's proposed separate hashed secret;
that proposal remains available if public acceptance provenance is later needed.

## CC interface review repair (5879360333)

Before: identical names had no distinct public acceptance marker. After: full
SHA-256 acceptance handles distinguish acceptances without revealing their
reusable capability. A handle is not identity or independent authorship.
Capsule v3 carries that field; v1/v2 are rejected, not silently upgraded.

Before: acceptance referenced a fixed label. After: GET /api/disclosure supplies
the text and SHA-256 identifier; acceptance stores that digest. Changed terms
invalidate the old room rather than silently reusing acceptance. Start a new
disposable room after changing disclosure text. A digest does not prove reading
or comprehension, and clients may still submit it without reading the text.

Entries are labelled as claims, including an unverified-role warning. The
shutdown disclosure explicitly denies secure erasure and notes crash residue.
Acceptances are capped at 100 per room. This bounds storage, not hostile-host
denial of service. COMPARISON.md and RESULTS.md preserve and correct the invalid
historical-record-versus-retelling comparison; no burden win is earned.
