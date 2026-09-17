# ATRS Reader Lens

Status: **READER / RESEARCH AID / FROZEN SEPTEMBER DEMO / NOT A RIGHTS OR COMPLIANCE ORACLE**

Purpose:

> Help a reader inspect what a published ATRS record actually says about what someone can do next, without converting disclosure into a score or inventing rights that the record does not establish.

The lens is generated from the same frozen September evidence bundle used by the audit. It does not refetch GOV.UK by default.

## Reader task

For any published ATRS record, the lens should let a reader quickly answer only source-supported questions:

1. Is a parser-recognised `Appeals and review` field present in the frozen record?
2. What does that field say, verbatim as extracted from the public source?
3. Does that field publish any URL, email, phone-like token or link destination?
4. What does the record separately disclose about human review?
5. Who is named in the record's senior-responsible-owner field?
6. Can the reader open the original GOV.UK source and check the card against it?

The lens does **not** answer:
- whether a legal appeal right exists;
- whether a route is effective, reachable or timely;
- whether the published record is complete;
- whether the organisation is compliant;
- what undisclosed/internal practice actually occurs.

## Default evidence view

The default interface shows only:
- record title;
- exact frozen source SHA-256;
- direct link to the GOV.UK record;
- extracted `Appeals and review` text;
- syntactic contact/link tokens in that field;
- expandable `Human review` text;
- expandable `Senior responsible owner` text;
- explicit inference ceilings.

Search covers tool/organisation names and the disclosed text. Filters can show records with or without a parser-recognised appeals field and with or without syntactic contact/link tokens.

`CONTACT_TOKEN != APPEAL_RIGHT` remains explicit.

## Exploratory annotations

Post-pilot semantic labels can be attached only if their evidence digest matches the exact audit evidence projection.

They are:
- hidden by default;
- shown only after an explicit reader opt-in;
- visibly labelled `Exploratory annotations — post-pilot; not validated`;
- never substituted for the source text.

This is deliberate. The annotation layer is a research object. The source record is the evidence.

## Frozen demo witness

Generated from:

```text
source audit run = 35257984573
source audit head = 4a7b43df95a2b776b885f8ee903d929100414af7
source artifact = 10513278849
source artifact sha256 = ad315d9b08a0af65c4615638df2235b9ce6f021307315fbeb6dfcbd8cbdb0097
records = 152
```

Reader build workflow:

```text
workflow = ATRS Reader Lens frozen demo
run = 35264692132 SUCCESS
artifact = 10515514307
artifact sha256 = da8d037db016bd49a84f7167cf74964fb0745f186c2aaf386d001b37dee214d7
```

The generated HTML contains 152 source-linked cards. Exploratory annotations are evidence-bound and hidden by default.

## Why keep it

The audit asks whether field completion and reader-visible answer-back information are the same thing.

The lens makes that question inspectable without requiring the reader to trust an aggregate statistic or a Framework interpretation. A reader can move from a candidate claim back to the exact published wording and original GOV.UK page.

That is the value ceiling currently earned:

```text
SOURCE-READBACK AID != DEMONSTRATED READER BENEFIT
EASIER INSPECTION != EFFECTIVE REMEDY
READER LENS != REPLACEMENT FOR GOV.UK
```

A later human-reader task could test whether the lens actually reduces time/error when answering bounded questions about the record. Until then, benefit remains plausible and unestablished.
