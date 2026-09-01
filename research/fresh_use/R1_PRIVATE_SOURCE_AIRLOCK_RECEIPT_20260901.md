# R1 PRIVATE SOURCE / AIRLOCK RECEIPT — 2026-09-01

Status: PRIVATE SOURCE FREEZE + DRY PREPARATION RECEIPT / NOT A RECEIVER RESULT / NOT DISPATCH AUTHORITY

Purpose: preserve a reproducible witness that the R1 Wickford fresh-use case was assembled from exact official-source bytes, not from URLs, currentness claims or Framework-authored fact summaries.

## Boundaries

```text
RECEIVER OUTPUT = NONE
PROVIDER SPEND = NONE
DISPATCH AUTHORITY = NONE
TRACE/ME MUTATION = NONE
SOURCE REDISTRIBUTION CLAIM = NONE
```

Raw pages, first-stage visible-text extracts, bounded extracts, run packets and evaluator-only mappings remain private/local evidence. This receipt records identities and procedures only; it does not publish third-party source bytes.

## Retrieval freeze

Retrieval UTC: `2026-09-01T14:33:31Z`.

Deterministic chain for every source:

```text
captured official HTML bytes
-> html_visible_text_v1
-> pre-frozen utf8_line_ranges_v1
-> receiver source member
```

| Source | Official URL | Raw HTML SHA-256 | Visible-text SHA-256 | Frozen lines | Receiver-member SHA-256 |
|---|---|---|---|---|---|
| RAIB Wickford investigation | `https://www.gov.uk/government/news/derailment-of-a-passenger-train-at-wickford` | `6456239ef6486fd62c85041f499bfdc966161636b8c04e1ff127fe7ac3c155cf` | `99028d2cc6ef713d879aca0e419321e884acda3c1ae84624546472d52d573440` | `113-151` | `3eddfc6f79b33694c12df4513d6946d29521b4e10e58037e8ead78751b6afa4e` |
| RAIB current investigations register | `https://www.gov.uk/government/publications/raib-current-investigations-register/rail-accident-investigation-branch-current-investigations` | `1bd1efd771202491681bc9fd4fcc38ded76e2b1bef0d2c4498225cae4dffe23f` | `cef065127dc5ced2846b0c622ddf3ae351cc4196ae038c6118126cde8690f390` | `133-149; 259-269` | `03bcd8b00355d696fab7e86097b40db8f8a49f8afd937cd7eee08832389643c0` |
| Network Rail buckled rail / summer heat | `https://www.networkrail.co.uk/rail-travel/delays-explained/buckled-rail-and-summer-heat/` | `96f4b1fbe67680010d23007fa34730586b0ec81527fdeceb8880180f173c9102` | `9a3a49712e7758e9b7f14ba4c0fa45490859b8eca2c6dd04fc0f5d031d50ff91` | `621-655` | `206c78413e8e973d7f560f94d4ed7775d7e5526cdd759520cee039456a853316` |
| Network Rail speed restrictions | `https://www.networkrail.co.uk/rail-travel/delays-explained/speed-restrictions/` | `9281416cde1b01c935386b08883871fedd5dda00bf1135b48ccf4c39a164b1c0` | `9a5fe5e2ec41e242913757870d4c7a4f5ef6d4b543dcaf8b56704caaa9425f4e` | `621-653` | `9811b74cddb2e1cf52a9978c16f6cba7a1c1ed75568409cba62766cc0495dee5` |
| Network Rail soil moisture deficit | `https://www.networkrail.co.uk/stories/soil-moisture-deficit-on-the-railway/` | `9f6f8255930e039653e6e257a49696584b34861e77f3519d915dccc6e27712f3` | `449eb6e0c838df71f687b9d3bf03487760e1880c4fd011f30c1364c206fdbcf0` | `239-318` | `83defcdc53fd5a11fe82affbf3540d9696bd802d675be23d44bc523867202c88` |

The bounded receiver material is approximately 2,620 words / 15,997 bytes across five source members. Selection was frozen before any receiver output existed. Both cells receive the same five bounded source members and the same neutral task.

## Dry preparation

Tool candidate:
- COM draft PR #78;
- original reviewed head: `8dc389fddbd8502e9d548c075b90bc23408ee894`;
- current repaired exact head: `33c1660d6f9b8f6cc11840fa07928d91442e1412`;
- provider-free: prepares, verifies, records, freezes blinded scores and unmasks; it does not browse, dispatch, score substantive answers or authorize spend.

Claude Code returned `REPAIR` on the original head. Its five findings were integrated:
- score-file integrity did not establish score-before-unmask ordering;
- POSIX permission bits did not establish confidentiality on native Windows;
- cryptographically bound and operator-attested receipt claims were not visibly separated;
- the 700-unit counter was not cross-script comparable;
- ZIP creation used an existence check followed by a non-exclusive write.

The repaired head adds a clearly bounded local hash-chained transition sequence; fails closed on native Windows until a tested DACL backend exists; separates bound facts from attestations and attestation-derived timing; scopes the counter explicitly to English-language outputs while recording additional scalar/byte measures; and uses exclusive ZIP creation.

Codex then reproduced final-event tail truncation plus different-score substitution against the first repair. The current head explicitly concedes local-log truncation/rewrite and makes `score` emit a neutral freeze token. Tool-mediated unmask now requires those exact bytes at a full Git commit/path. Both shared receiver-facing surfaces also state `Answer in English`; the language field remains operator-attested rather than machine-verified.

Codex's next exact audit reproduced a post-unmask split-chain substitution: an anchored token/report for score A could coexist with rewritten current score/token B and a rebuilt local event tail. The current head closes that join explicitly. Verification now requires agreement among the current freeze-token bytes, Git-anchored token bytes, current score-artifact hash, unmask-report score hash and unmask-event score hash. A dedicated post-unmask rewrite regression is included.

Claude Code then executed the exact prior head on the operator's native Windows platform. The intended fail-closed guard worked, but that meant the whole workflow was unusable there: 5/15 tests passed and every `prepare` path stopped at `PRIVATE_STORAGE_UNVERIFIED`. The current head implements the preferred repair. It resolves the current user to one SID, installs a protected Windows DACL through built-in PowerShell/.NET, and independently reads it back. The accepted structure is current user as owner plus exactly current user, Local System and Built-in Administrators with explicit Allow/FullControl rules; inheritance, deny/wrong rules, duplicate/missing/unexpected trustees, malformed output or unavailable commands fail closed. Input prevalidation now precedes the platform guard, while the guard still precedes the first bundle-file write. Native Windows reproduction of this exact head remains required.

Superseded dry objects are quarantined and were never dispatched:
- `RUN001`: visible pilot identifier leaked the project label `7Q`;
- `RUN002`: neutral labels and packet parity passed, but original HTML -> visible-text was outside the bundle verifier;
- `RUN003`: direct raw-HTML composite extraction passed, but it preceded integration of Claude Code's five evidence-boundary findings.
- `RUN004`: integrated Claude Code's findings, but preceded the external Git freeze-token requirement and receiver-facing English instruction.
- `RUN005`: added the Git token anchor and English instruction, but preceded the five-way post-unmask score/token/report/event join.
- `RUN006`: closed the five-way join, but preceded the native Windows DACL backend.

Current dry bundle:

```text
pilot_id: FRESH-USE-R1-20260901-RUN007
cells: 2
case_pack_sha256: 05b7bdd9e1feb9050eaa4e24b33314d2f78512ae42f03a8df8110d9d7e2da567
public_launch_register_sha256: 7f3ad51434e5e8343fbb823e9eaae7152605cd5f6aa5afb941153507a4f5c3f4
packet_sha256_1: f79655c3229f39ea5ad86234d2291d2f75b05be8591f0225d72b88601b056f03
packet_sha256_2: 506eeb77c59199ae121f4f8eb30297ec0d6aa792424ba785673238f962f13546
private_arm_map_commitment_sha256: 0bdb6b344ffc64b8a7ba6cb3f42acab1a9b64ec138adf00088c4cd0a02f25535
private_source_ledger_commitment_sha256: 1a03e860d2671e71c53cdb4e114dd4a8163cb0ee2c2d37f85bbeebd987e32f26
local_genesis_event_log_sha256: 2228af5ced680c074211aa0c0af31989fd46fac857fbf47cbbd75e356fae0e74
local_genesis_event_sha256: b50271f7889bf02aabc584a24af3dd49015dfb8a2075442da6b4feb74ad735a1
tool_sha256: 877225736b2afd3af260b62ce2819046c9f7dbfd1fd7fe180cbab0b763896aac
```

Public packet/register inspection found no `7Q`, arm identity, evaluator or score label. One packet contains the frozen reasoning aid and its matching exact instruction; the other does not. Which neutral cell alias maps to which arm remains only in the evaluator-private `0600` mapping behind a verified `0700` run/private boundary. The private source ledger and local event log are also `0600`.

The event log currently contains only the prepare/genesis event. Its hash chain is explicitly local and operator-controlled:

```text
LOCAL_SEQUENCE_WITNESS != EXTERNAL_TIMESTAMP
LOCAL_SEQUENCE_WITNESS != INDEPENDENT_ATTESTATION
LOCAL_SEQUENCE_WITNESS != PROOF_AGAINST TRUNCATION / TAIL DELETION / REWRITE / REBUILD
GIT TOKEN ANCHOR != TRUSTED TIME OR PROOF OF COGNITIVE BLINDNESS
```

Verification at preparation:
- `freshuse.py prepare`: PASS — two sealed cells;
- `freshuse.py verify`: PASS;
- unit suite: 23/23 PASS on Linux, including deterministic Windows mocks;
- `py_compile`: PASS;
- original HTML -> visible text -> frozen lines replayed by bundle verifier: PASS;
- identical source-snapshot list and case-pack SHA-256 across both cells: PASS;
- evaluator note absent from both packets: PASS;
- raw HTML absent from both packets: PASS.

## Remaining gates

- independent Codex exact-head + `RUN007` re-audit: OPEN at receipt update;
- Claude Code native-Windows exact-head reproduction request `FW-FRESH-USE-AIRLOCK-REVIEW-20260901-006`: OPEN;
- fresh receiver launch: CLOSED;
- receiver/spend authority: CLOSED.

This object establishes reproducible preparation only.

```text
PACKET READY != RECEIVER FRESH
PRIVATE ARM MAP != INDEPENDENT EVALUATOR
LOCAL HASH CHAIN != EXTERNAL ORDER PROOF
DRY VERIFICATION != EMPIRICAL RESULT
```
