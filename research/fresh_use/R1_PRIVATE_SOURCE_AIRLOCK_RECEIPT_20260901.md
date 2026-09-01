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
- current repaired exact head: `2c3aa3c52136dd6968fa41bd5e2996746f687190`;
- provider-free: prepares, verifies, records, freezes blinded scores and unmasks; it does not browse, dispatch, score substantive answers or authorize spend.

Claude Code returned `REPAIR` on the original head. Its five findings were integrated:
- score-file integrity did not establish score-before-unmask ordering;
- POSIX permission bits did not establish confidentiality on native Windows;
- cryptographically bound and operator-attested receipt claims were not visibly separated;
- the 700-unit counter was not cross-script comparable;
- ZIP creation used an existence check followed by a non-exclusive write.

The repaired head adds a clearly bounded local hash-chained transition sequence; fails closed on native Windows until a tested DACL backend exists; separates bound facts from attestations and attestation-derived timing; scopes the counter explicitly to English-language outputs while recording additional scalar/byte measures; and uses exclusive ZIP creation.

Superseded dry objects are quarantined and were never dispatched:
- `RUN001`: visible pilot identifier leaked the project label `7Q`;
- `RUN002`: neutral labels and packet parity passed, but original HTML -> visible-text was outside the bundle verifier;
- `RUN003`: direct raw-HTML composite extraction passed, but it preceded integration of Claude Code's five evidence-boundary findings.

Current dry bundle:

```text
pilot_id: FRESH-USE-R1-20260901-RUN004
cells: 2
case_pack_sha256: 05b7bdd9e1feb9050eaa4e24b33314d2f78512ae42f03a8df8110d9d7e2da567
public_launch_register_sha256: 1766b498aef2f9aba891ffc9979caa495b6671ee3678054c7d634de57819805f
packet_sha256_1: 086953f724f9f3393012b9e4a1021066294b4370137ce738e21c2c58a8c81e99
packet_sha256_2: 5d55d07728d10735870cfcd7b8ea04f9ffc9b66ffa6f89f382c6ac05dc53b31e
private_arm_map_commitment_sha256: cd2cb149bfe83308848a4b1cc291e94df4f165697879e9a033898400e98c422f
private_source_ledger_commitment_sha256: 46c0b524ae5810f478d7ed8141fe97a61a1eb678ea6dbda51fa921d1c232b432
local_genesis_event_log_sha256: 20bb02d02980e5e2225802cfefe31a3b189f6139b8dc62168d1438330a20f67f
tool_sha256: 0c14cf1c457466910a47721909da51f0825a3c6a6c3a4348841e2e97b6df8055
```

Public packet/register inspection found no `7Q`, arm identity, evaluator or score label. One packet contains the frozen reasoning aid and its matching exact instruction; the other does not. Which neutral cell alias maps to which arm remains only in the evaluator-private `0600` mapping behind a verified `0700` run/private boundary. The private source ledger and local event log are also `0600`.

The event log currently contains only the prepare/genesis event. Its hash chain is explicitly local and operator-controlled:

```text
LOCAL_SEQUENCE_WITNESS != EXTERNAL_TIMESTAMP
LOCAL_SEQUENCE_WITNESS != INDEPENDENT_ATTESTATION
LOCAL_SEQUENCE_WITNESS != PROOF_AGAINST_WHOLE_LOG_REBUILD
```

Verification at preparation:
- `freshuse.py prepare`: PASS — two sealed cells;
- `freshuse.py verify`: PASS;
- unit suite: 13/13 PASS;
- `py_compile`: PASS;
- original HTML -> visible text -> frozen lines replayed by bundle verifier: PASS;
- identical source-snapshot list and case-pack SHA-256 across both cells: PASS;
- evaluator note absent from both packets: PASS;
- raw HTML absent from both packets: PASS.

## Remaining gates

- independent Codex exact-head + `RUN004` re-audit: OPEN at receipt update;
- Claude Code exact-head re-audit request `FW-FRESH-USE-AIRLOCK-REVIEW-20260901-003`: OPEN;
- fresh receiver launch: CLOSED;
- receiver/spend authority: CLOSED.

This object establishes reproducible preparation only.

```text
PACKET READY != RECEIVER FRESH
PRIVATE ARM MAP != INDEPENDENT EVALUATOR
LOCAL HASH CHAIN != EXTERNAL ORDER PROOF
DRY VERIFICATION != EMPIRICAL RESULT
```
