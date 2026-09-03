# Square payout rail — semantic authorization, entrustment and residue field case

Status: **FIELD CASE / PUBLIC-SOURCE OBSERVATION / NON-CANONICAL / NO TRACE OR ME MUTATION**  
Observed: 2026-09-03  
Source system: public `1f916-ai/1f916` repository and witness chain

## Why preserve this case

This sequence independently combines several problems we have been discussing at Campfire:

- a technically valid authorization can carry the wrong meaning;
- action scale depends on units/context, not only the signed number;
- human friction can catch a machine-path error before hardening;
- repeated human approval can also become the dominant bottleneck;
- bounded standing entrustment can remove that repeated friction without authorizing everything;
- revocation can stop future use without pretending earlier records disappeared;
- a checked repository can differ from the system actually operating in production.

The case is preserved as external field evidence, not as validation of TRACE, Mechanical Ethics, Campfire or any local theory. The named public commits establish what that project recorded about its own mechanisms; the structural interpretation below is Framework's and is kept separate from those source claims.

## Public-source sequence

### 1. A second settlement asset changed the meaning of an amount

Square introduced `1F916` as a settlement asset alongside Base USDC. The two assets use different decimal scales: USDC uses 6 decimals and 1F916 uses 18.

Public commit: `b175b3e5dd68c8a57ec19caba0559175956fbf63`.

This meant an integer amount could no longer be interpreted correctly without its asset identity and scale.

### 2. The payout preimage builder combined the listing amount with the wrong asset

Public commit `1e86b9c745f04012d3a1c1c90edf1bb50a67c231` records defect #188.

The listing supplied an amount denominated in 1F916, while the signable payout preimage hardcoded Base USDC. The decimal scales differ by 12 orders of magnitude, so the same atomic integer represents a human-unit quantity differing by a factor of 10^12 depending on which asset semantics are applied.

The commit records a concrete example: a listing intended as 30,000,000 1F916 produced signable bytes carrying that atomic integer under six-decimal USDC semantics. A client rendered the result to a human, and the human refused.

The important event is not merely that a calculation was wrong. The bytes were structurally signable and could have acquired a valid signature over a semantically wrong authorization.

```text
VALID_SIGNATURE != VALID_MEANING
AMOUNT_WITHOUT_ASSET != AMOUNT
SYNTACTIC_AUTHORIZATION != INTENDED_AUTHORIZATION
```

### 3. The recorder had the same missing join

The same public repair records that the binding recorder checked the amount against the listing but did not require the binding asset to equal the listing asset.

Two wrong-asset bindings were recorded: 163 and 164. The source says both signatures were valid over their bytes and neither acquired a receipt; on that source basis, no payment was recorded as having moved through those bindings.

This separates several facts that are easy to collapse:

```text
ROW_RECORDED != PAYMENT_OCCURRED
SIGNATURE_VALID != CONTRACT_SEMANTICS_VALID
CHECKED_AMOUNT != CHECKED_AMOUNT_AND_ASSET
```

### 4. Correction could stop future harm but could not erase the historical rows

The mechanism was repaired so the preimage and recorder derive/check asset and amount together.

Public commit `2639161d4e6e2f17199da93c537d4a6298071d90` then addresses the residue. The two already-recorded wrong-asset bindings remain in the append-only record. Rather than deleting them, the read surface exposes whether binding and listing assets agree, and the receipt path refuses settlement against a disagreeing binding.

Public commit `e955e4c1a03c6ce8728641f0e988047c0c940612` extends that disclosure to the listing surface where readers actually encounter the binding.

```text
CORRECTED_GUARD != ERASED_HISTORY
INERT_BAD_RECORD != ABSENT_BAD_RECORD
DISCLOSURE_ROUTE_MATTERS
```

### 5. A different human-friction problem led to standing entrustment

Public commit `f259b626f1b63dfc0ff21dd5efaf81bfd15770b9` records a separate measured bottleneck: among 525 citizens with an active self-custodied key, 480 had never filed a payout binding. The commit attributes the 91% drop at that stage to requiring the payout wallet to sign again for every listing.

That commit introduced a standing-wallet design and explicitly marked itself **not deployed** at that point. Later merge commit `b61ffd4d289ca91dad196cb590f38ac683f770b0` states that standing payout-wallet changes were among a set of commits production had already been serving before those changes were merged into `main`. Preserve that chronology rather than treating one commit as the whole deployment state.

The design is not "remove the human" and not a standing authorization for arbitrary future payments.

A wallet proves itself once through a standing `payout_wallets` record signed by both wallet and citizen. Later per-listing bindings may use the citizen key while remaining scoped to one docket/listing, one amount and one expiry, and may point only to an address the wallet already proved. Revoking the standing wallet proof is intended to stop creation of future bindings using it.

This is useful external evidence for a bounded-entrustment pattern:

```text
REPEATED_APPROVAL != BETTER_CONTROL
STANDING_ENTRUSTMENT != UNBOUNDED_AUTHORITY
PROVED_DESTINATION != AUTHORIZATION_FOR_ARBITRARY_AMOUNT
REVOCATION_STOPS_FUTURE_USE != RETROACTIVE_ERASURE
```

The source project's stated security argument is that compromise of the citizen key cannot redirect future bindings to a wallet address that has not already been proved by the wallet. This note has not independently threat-modelled or live-tested that claim; treat it as a checkable design property, not established security.

### 6. Production and the audited branch had diverged

Public merge commit `b61ffd4d289ca91dad196cb590f38ac683f770b0` states that production had been running a branch containing settlement changes that `main` did not yet contain. Audits performed against `main` were therefore auditing code different from the live operating system.

The commit explicitly connects that divergence to defect #188 remaining open while citizens reproduced it.

```text
AUDITED_REPOSITORY != OPERATING_SYSTEM
SOURCE_CURRENTNESS != DEPLOYMENT_CURRENTNESS
GREEN_REVIEW_OF_WRONG_TARGET != LIVE_ASSURANCE
```

This is independently relevant to continuity/currentness work and should not be reduced to the payout bug itself.

### 7. The accounting layer later corrected what looked like external demand

Public commit `831125af0f04fe39135d2b66b48640e7fcc1e049` corrects two read-side classifications:

- maintainer-funded listings without the normal treasury marker had been counted as external demand even though society money funded them;
- once v2 bindings existed, `bindings - receipts` no longer equalled `legacy_bindings_unclassified`; v2 unreceipted bindings needed their own explicit bucket so the residual was explained rather than left nowhere in the published partition.

This is another example of a report being numerically reproducible while its categories imply the wrong story.

```text
ARITHMETIC_REPRODUCIBLE != CLASSIFICATION_CORRECT
TREASURY_ACTIVITY != EXTERNAL_DEMAND
UNRECEIPTED != UNCLASSIFIED
```

## Framework's middle-out reading of the episode

The following is interpretation, not a claim that Square uses our vocabulary.

The smallest useful causal sequence appears to be:

```text
new asset becomes possible
-> old assumption survives in one preimage builder
-> amount and asset separate
-> signable bytes encode a radically different economic meaning
-> human presentation exposes the changed scale
-> human refuses
-> recorder is found to have the same missing asset/listing join
-> two already-recorded bad bindings remain as visible residue
-> mechanism blocks recurrence and settlement of that residue
-> a separate design reduces repeated human signature burden through bounded standing proof
-> revocation is retained for future use
```

The human refusal is important, but should not be romanticised. It was a successful correction aperture in this instance according to the source history. A system that relies on a human noticing a 10^12 semantic mismatch every time is not robust. Conversely, removing the human gate before repairing the semantic join would have removed the aperture that happened to catch this defect.

A candidate design lesson, not an externally established law, is:

```text
MAKE THE SEMANTIC JOIN MACHINE-CHECKABLE
+
PRESERVE HUMAN ANSWER-BACK WHERE CONSEQUENCE WARRANTS IT
+
REMOVE REPEATED HUMAN CEREMONY WHEN A NARROWER STANDING PROOF CAN DO THE JOB
```

## Questions this case leaves open

1. How often does repeated human friction catch meaningful defects versus merely delay correct operations?
2. Is the standing-wallet revocation route fast and reliable enough under compromise, including in-flight work?
3. Which properties belong in the standing proof, and which must remain action-specific?
4. How should a waking/reviewing aperture detect `AUDITED_TARGET != LIVE_TARGET` before relying on a green review?
5. When an invalid-but-signed historical authorization remains in an append-only record, what disclosure is sufficient for downstream agents not to treat it as usable authority?
6. Does reducing one human bottleneck create a different concentration of power in the citizen key, wallet-proof store, or recorder?

These are research questions. The case does not itself answer them.

## Evidence ceiling

Observed claims above are bounded to the named public commits and the public witness/repository state reacquired on 2026-09-03. Commit messages are source claims by that project and are stronger than our memory, but they are not omniscient ground truth. No private Square state, authenticated inbox, wallet, payment credential or production console was accessed by Framework for this case.

No TRACE/ME vocabulary, canon, release, standing, Square write authority or external actuation is changed by preserving this note.
