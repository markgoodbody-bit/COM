# ATRS Reader Lens — 17 Sep 2026

Status: **USEFUL READER/RESEARCH AID / NOT SELECTED ENTRY / NOT DEPLOYED / NOT RIGHTS OR COMPLIANCE ORACLE**

Direct Mark instruction: `go build something good and valuable / COMSYNC and proceed`.

Built on #364 after owner subtraction and the falsify-100/drift pass.

## Purpose

Make the current ATRS research inspectable by a reader without asking them to trust an aggregate statistic or Framework interpretation.

Question:

> What does this published ATRS record actually say about what someone can do next?

The lens does not replace GOV.UK. Every card links back to the original record.

## Source boundary

Frozen audit witness:

```text
run = 35257984573
source head = 4a7b43df95a2b776b885f8ee903d929100414af7
artifact = 10513278849
artifact sha256 = ad315d9b08a0af65c4615638df2235b9ce6f021307315fbeb6dfcbd8cbdb0097
records = 152
```

Reader build:

```text
workflow = ATRS Reader Lens frozen demo
run = 35264692132 SUCCESS
artifact = 10515514307
artifact sha256 = da8d037db016bd49a84f7167cf74964fb0745f186c2aaf386d001b37dee214d7
cards = 152
```

No live corpus refetch was performed to make the frozen demo.

## Default reader view

For each record:
- title;
- frozen source SHA-256;
- direct GOV.UK source link;
- exact extracted `Appeals and review` text;
- any published URL/email/phone/link tokens in that field;
- expandable `Human review` text;
- expandable `Senior responsible owner` text;
- explicit inference ceiling.

Search covers tool/organisation names and disclosed text. Filters can show records with/without a parser-recognised Appeals field and with/without syntactic contact/link tokens.

## Exploratory annotation boundary

Post-pilot semantic labels are optional only.

They are:
- bound to the exact Appeals evidence digest;
- hidden by default;
- shown only after explicit opt-in;
- visibly labelled `Exploratory annotations — post-pilot; not validated`;
- never substituted for source text.

Representative readback preserves difficult distinctions:
- NS&I PolyAI: human handoff + no binding decision + broader complaints process;
- Wilton Park Data Cleaning: data-rights action + unresolved relevance to output review;
- Cabinet Office Automated Digital Document Review: explanation/justification without recovery + ambiguity;
- Hampshire/TVP DARAT: process planned but not operating;
- DBT Find Exporters: Appeals field not parser-observed, without inference that no review practice exists.

## Value ceiling

```text
SOURCE_READBACK_AID != DEMONSTRATED_READER_BENEFIT
EASIER_INSPECTION != EFFECTIVE_REMEDY
CONTACT_TOKEN != APPEAL_RIGHT
MISSING_FIELD != NO_REVIEW_PRACTICE
READER_LENS != REPLACEMENT_FOR_GOV_UK
```

This object is worth keeping because it makes the evidence walkable and useful even if the competition route dies.

It does **not** earn a claim that readers are faster, more accurate, or better protected. A later bounded human-reader task can test that.

## Current disposition

- keep as #364 reader/research aid;
- do not deploy publicly by momentum;
- do not treat UI polish as competition progress;
- leave substantive fresh census/analysis for a future current-world research run / November sprint if live eligibility permits;
- #364 remains current lead, not selected entry.

`PURPOSE > INSTRUMENT`
