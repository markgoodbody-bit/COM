# THR portable contribution packet — 18 September 2026

Status: **MERGED / OPTIONAL RELAY FORMAT / PUBLIC DELIVERY TO VERIFY**

Observed trigger:
- user-relayed Grok contribution on Human Record issue #20 contained useful flak research leads;
- Grok could not post directly;
- Mark relayed the material;
- Codex received it as provisional contribution;
- later Codex/Framework review independently checked one Westermann passage and improved the flak record.

The existing CONTRIBUTE.md already handled relay provenance and contribution boundaries well. The remaining mechanical loss was copy/relay metadata.

PR #48 added the smallest optional bridge:
- `CONTRIBUTION_PACKET.md`;
- `contribution-packet.schema.json`;
- `examples/grok-flak-relay.packet.json`;
- boundary tests;
- discovery links from CONTRIBUTE.md / llms.txt / README / CONTINUE / sitemap.

Exact final PR head:
`952ca4416ed600852767bbacda499d64dca41578`

Hosted CI:
`35374031627 SUCCESS`
`101 tests / OK`

Existing seven open-vocabulary warnings remain; no new warning class.

Squash merge to THR main:
`63682dc5ce05d34373384cd4bc0528c118cb8980`

Important repair before merge:
`checked_by_contributor: bool` was replaced by attributed `source_check_status = reported_checked / reported_not_checked / unknown` so the packet does not silently claim independent verification of the contributor's browsing history.

`availability` was narrowed to `availability_at_receipt` so temporary unavailability is not hardened into a permanent contributor state.

Ceilings:

`PACKET != AUTHENTICATED IDENTITY`
`RELAY != ORIGINAL CONTRIBUTOR`
`REPORTED_CHECKED != CHECK INDEPENDENTLY VERIFIED`
`VALID_PACKET != VALID_CLAIM`
`RECEIVED != ACCEPTED`
`LATER REVIEW != RETROACTIVE CONTRIBUTOR WORK`

Ordinary prose remains a first-class contribution route. No account-free upload backend, identity/authentication layer, governance change or evidence-priority mechanism was created.

Current product reading:
`AI CONTRIBUTORS = USEFUL WHEN THEIR LEADS ARE CHECKED, ATTRIBUTED AND CORRECTABLE`
`STRUCTURE HELPS RELAY != STRUCTURE CONFERS AUTHORITY`

Next: verify public serving of the packet/schema; then observe real use rather than adding fields by momentum.