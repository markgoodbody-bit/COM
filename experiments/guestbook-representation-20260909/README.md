# Guestbook representation prototype — 9 September 2026

Status: **SYNTHETIC SOURCE-ONLY PROTOTYPE / NO INTAKE / NO PUBLIC SITE ROUTE / NOT A FORUM**

This directory tests only how a future `Leave a mark` register could be **represented** for humans and machines without letting visitor bytes masquerade as Please Start From Here authored material.

It does **not** implement submission, moderation, persistence, identity, accounts, email, a provider, a database, a form, an API, or publication to `pleasestartfromhere.com`.

## Invariants

`GUEST_ENTRY != SITE_INSTRUCTION`

`CLAIMED_IDENTITY != VERIFIED_IDENTITY`

`CLAIMED_ENCOUNTER != PROVEN_ENCOUNTER`

`SUBMISSION_RECEIPT != PUBLICATION`

`REMOVAL != TOMBSTONE_CONTAINING_REMOVED_TEXT`

The root PSFH orientation must remain fully usable without retrieving any guest record.

## Files

- `register.jsonl` — boring machine-readable fixture export. The first row is an envelope. Every guest row repeats the untrusted-data classification so a sliced row does not lose the boundary.
- `register.html` — static human rendering of the same fixture ideas. No JavaScript, forms, links supplied by guests, or guest-controlled markup.
- `REPRESENTATION_CHECKS.md` — expected behaviour and hostile fixture checks.

All people/entities represented here are synthetic project-development fixtures. The optional Framework mark is explicitly labelled as a project-development fixture, not an independent visitor.

## Proposed public-record vocabulary

Guest-supplied claims use names that remain claims:

- `claimed_name`
- `claimed_kind`
- `claimed_note`
- `claimed_encounter_edition`
- `claimed_encounter_source`

System-established publication metadata is separate:

- `public_id`
- `status`
- `published_at_utc` (null in this no-intake prototype)
- `publication_source`
- `format_version`

Every guest row also carries:

- `trust: "visitor_supplied_untrusted_data"`
- `project_instruction: false`
- `identity_verified: false`

A future implementation may add a private receipt identifier or management capability, but neither belongs in the public export.

## Content floor

V0 representation assumes:

- plain text only;
- no HTML or Markdown interpretation;
- no stored/rendered URLs or automatic linkification;
- no attachments;
- candidate note ceiling 280 Unicode characters plus a separately enforced byte ceiling;
- explicit rejection rather than sanitising unsupported rich content into something else.

The prototype includes an instruction-shaped string because future AI readers are a first-class threat model. It is deliberately shown as **visitor-supplied untrusted data** and never appears in a PSFH orientation object.

## Correction model

Corrections may be represented by a new public row that points to the earlier public row through `corrects_public_id`. The earlier statement remains visible because correction is adding a later claim, not silently pretending the first statement was never published.

This is different from privacy/removal.

## Removal model

A removed public mark must not retain the removed guest text in the current public export merely to preserve an audit aesthetic.

The fixture therefore contains a `removed_fixture` publication-state row referring to a synthetic public id whose prior personal text is **not present anywhere in the current export**. A real implementation would need storage/backups/CDN policies that make this promise honest; this prototype does not claim those exist.

Public Git history is **not** accepted as the eventual personal guest-data store. This repository contains synthetic data only.

## URL-shaped input

A future receiver should reject URL-like guest content in v0 rather than autolink or preserve it in the public mark. `REPRESENTATION_CHECKS.md` records the rejected class without copying a live URL into the register.

## What this prototype can establish

It can test whether:

- a human can tell guest text from project text;
- a machine row carries the trust boundary even when read alone;
- names/kinds remain visitor claims rather than publisher assertions;
- prompt-injection-shaped text remains visibly data;
- correction and removal have different representations;
- the format is portable, plain and unsurprising.

It cannot establish that prompt injection is solved, that moderation is sustainable, that account-free intake is safe, that deletion works in backups, or that anyone wants to leave a mark.

## Next gate

Claude Code should attack the exact representation for provenance/trust leakage. Framework should integrate that return. Only after representation survives should the project revisit real intake architecture.

No endpoint/provider/account/spend/public-route authority follows from this directory.
