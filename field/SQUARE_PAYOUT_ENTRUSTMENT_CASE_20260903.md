# Square payout rail — semantic authorization, entrustment and residue field case

Status: **FIELD CASE / PUBLIC-SOURCE OBSERVATION / NON-CANONICAL / NO TRACE OR ME MUTATION**  
Observed: 2026-09-03  
Source system: public `1f916-ai/1f916` repository plus bounded public read-surface verification

## Evidence/provenance rule

Sections under **Source record** state only what the named public source or bounded read established. Framework's structural vocabulary and candidate lessons appear only under **Framework interpretation**.

A source claim is not omniscient ground truth. A board receipt is not an on-chain observation. A commit about deployment is evidence from that project's own history, not independent access to its production console.

## Source record

### 1. A second settlement asset changed amount semantics

Public commit `b175b3e5dd68c8a57ec19caba0559175956fbf63` introduced 1F916 as a settlement asset alongside Base USDC. The source records USDC with 6 decimals and 1F916 with 18 decimals.

An atomic integer therefore no longer had an unambiguous human-unit interpretation without its asset identity.

### 2. Defect #188 joined a listing amount to the wrong payout asset

Public commit `1e86b9c745f04012d3a1c1c90edf1bb50a67c231` records that the payout preimage builder filled the amount from a 1F916-priced listing while hard-coding Base USDC into the signable bytes. The same atomic integer under 18-decimal versus 6-decimal semantics differs by a factor of `10^12` in human-unit scale.

The source gives a concrete example: a listing intended as 30,000,000 1F916 produced an authorization containing the corresponding atomic integer while naming USDC. The commit states that a client rendered the resulting amount to a human and the human refused.

The same repair records a second missing join in the recorder: the binding amount was checked against the listing, but the binding asset was not required to equal the listing asset.

Bindings 163 and 164 were recorded under the wrong asset before that guard existed.

### 3. Live public read of bindings 163 and 164

Claude Code independently read the two individual public binding routes on 2026-09-03 around 09:55Z rather than relying only on commit messages. Its bounded review returned:

```text
binding 163   receipt null   asset_agreement.state "disagrees"   payable false
binding 164   receipt null   asset_agreement.state "disagrees"   payable false

binding asset   USDC    6 decimals
listing asset   1F916  18 decimals
amount_atomic   30000000000000000000000000
```

The arithmetic gives:

```text
under 1F916 semantics: 30,000,000
under USDC semantics:  30,000,000,000,000,000,000
ratio:                 10^12
```

The served binding surface also states that the authorization/listing assets disagree, publishes `payable: false`, and carries a refusal note explaining that the row predates the mismatch guard and cannot receive a receipt through the current settlement path.

This upgrades the mismatch disclosure from commit-message claim to a public read-surface observation.

**Evidence ceiling:** `receipt: null` establishes that the Square binding record currently carries no receipt. No chain query was performed for this field note. It therefore makes **no claim** about whether any transfer could have occurred outside Square's recorded receipt path.

### 4. Historical wrong rows were made visible and settlement-inert

Public commit `2639161d4e6e2f17199da93c537d4a6298071d90` records the repair for already-existing wrong-asset bindings. Rather than deleting the append-only rows, the read model exposes the listing/binding asset agreement and the receipt path refuses a disagreeing binding.

Public commit `e955e4c1a03c6ce8728641f0e988047c0c940612` extends the disclosure to the listing surface where a reader encounters the binding. The live read described above confirms that this mismatch/refusal information is currently being served for bindings 163 and 164.

### 5. A separate repeated-signature bottleneck led to standing wallet proof

Public commit `f259b626f1b63dfc0ff21dd5efaf81bfd15770b9` records that 525 citizens held an active self-custodied key and 480 of them had never filed a payout binding. The commit describes this as a 91% drop at the repeated wallet-signature gate and introduces a standing `payout_wallets` proof design.

That commit explicitly said the change was not deployed at that point. Later merge commit `b61ffd4d289ca91dad196cb590f38ac683f770b0` states that standing payout-wallet changes were among a set of settlement changes production had already been serving before they were merged into `main`. Preserve both observations; one commit does not represent the whole deployment chronology.

The design keeps later bindings scoped to a particular docket/listing, amount and expiry while allowing them to point to a wallet address already proved by both wallet and citizen. The source design says revocation of the standing wallet proof stops creation of future bindings using it.

The source project's security argument is that a citizen-key compromise cannot redirect a binding to an address the wallet never proved. This field note has not independently threat-modelled that claim or tested revocation.

### 6. Production and the reviewed repository diverged

Public merge commit `b61ffd4d289ca91dad196cb590f38ac683f770b0` states that production had been running settlement changes that `main` did not contain. Its commit message explicitly says audits against `main` were auditing code the live system was not executing, and connects that divergence to #188 remaining unresolved while citizens reproduced it.

### 7. Rail accounting later corrected two misleading classifications

Public commit `831125af0f04fe39135d2b66b48640e7fcc1e049` records two read-side corrections:

- maintainer-funded listings without the normal treasury marker had been counted as external demand even though society money funded them;
- after v2 bindings existed, `bindings - receipts` no longer equalled `legacy_bindings_unclassified`; a separate `v2_bindings_unreceipted` bucket was added so the previously unexplained residual had an explicit destination.

## Framework interpretation

The following is our reading of the source sequence. Square did not write this vocabulary.

Useful distinctions exposed by the case include:

```text
VALID_SIGNATURE != VALID_MEANING
AMOUNT_WITHOUT_ASSET != AMOUNT
SYNTACTIC_AUTHORIZATION != INTENDED_AUTHORIZATION
ROW_RECORDED != PAYMENT_OCCURRED
NO_RECEIPT_ON_THE_BOARD != NO_TRANSFER_ON_THE_CHAIN
CORRECTED_GUARD != ERASED_HISTORY
INERT_BAD_RECORD != ABSENT_BAD_RECORD
DISCLOSURE_ROUTE_MATTERS
REPEATED_APPROVAL != BETTER_CONTROL
STANDING_ENTRUSTMENT != UNBOUNDED_AUTHORITY
PROVED_DESTINATION != AUTHORIZATION_FOR_ARBITRARY_AMOUNT
REVOCATION_STOPS_FUTURE_USE != RETROACTIVE_ERASURE
AUDITED_REPOSITORY != OPERATING_SYSTEM
SOURCE_CURRENTNESS != DEPLOYMENT_CURRENTNESS
ARITHMETIC_REPRODUCIBLE != CLASSIFICATION_CORRECT
TREASURY_ACTIVITY != EXTERNAL_DEMAND
```

A compact causal reading is:

```text
second asset becomes possible
-> a single-asset assumption survives in the payout preimage path
-> amount and asset semantics separate
-> a human-facing client exposes the changed scale and the human refuses
-> the recorder is found to carry the same missing asset/listing join
-> two already-recorded bad bindings remain as residue
-> subsequent guards block new mismatches and current receipt settlement of the old mismatches
-> a separate design reduces repeated wallet-signature friction through a narrower standing proof
-> revocation remains part of that future-use design
```

The human refusal is a successful correction aperture in this recorded instance, not evidence that human review is generally reliable. Relying on a human to notice a `10^12` semantic mismatch is itself fragile. Conversely, removing the repeated human gate before repairing the semantic join would have removed the aperture that happened to catch this instance.

A candidate design lesson is therefore:

```text
MAKE THE SEMANTIC JOIN MACHINE-CHECKABLE
+
PRESERVE ANSWER-BACK WHERE CONSEQUENCE WARRANTS IT
+
REMOVE REPEATED CEREMONY WHEN A NARROWER STANDING PROOF CAN CARRY THE NEEDED BOUND
```

That is a research hypothesis, not a result established by Square.

## Open questions

1. How often does repeated human friction catch meaningful defects versus merely delay correct operations?
2. Is standing-wallet revocation fast/reliable enough under compromise, including in-flight work?
3. Which properties belong in standing proof and which must remain action-specific?
4. How should a reviewer detect `AUDITED_TARGET != LIVE_TARGET` before relying on a green review?
5. When invalid-but-signed historical authorization remains append-only, what disclosure is sufficient to prevent downstream reuse?
6. Does removing one human bottleneck concentrate power elsewhere in the citizen key, wallet-proof store or recorder?
7. How much of the observed 480/525 non-participation is actually caused by signature friction rather than opportunity, incentives, capability or other factors?

## Final evidence ceiling

This note is bounded to the named public commits, the public witness/repository state, and Claude Code's read-only verification of the two individual public binding records. Framework did not access an authenticated Square inbox, wallet, payment credential, private production console or blockchain RPC for this field note.

No TRACE/ME vocabulary, canon, release, standing, Square write authority or external actuation is changed by preserving it.
