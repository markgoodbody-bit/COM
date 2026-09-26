# EvidenceWatch × Zotero — integration substrate boundary

Date: 26 September 2026

Status: **OWNER-SUBTRACTED INTEGRATION DESIGN / NO ACCOUNT ACCESS / NO IMPLEMENTATION**

Purpose:

Define what EvidenceWatch should and should not build if Zotero remains the first proposed host workflow.

Current owner surfaces:
- https://www.zotero.org/support/dev/web_api/v3/
- https://www.zotero.org/support/dev/web_api/v3/basics
- https://www.zotero.org/support/dev/web_api/v3/syncing
- https://www.zotero.org/support/dev/web_api/v3/write_requests

## Zotero already owns library-state plumbing

Current Zotero API v3 provides:
- server Web API plus a desktop Local API exposing the same read endpoints;
- explicit API versioning;
- per-library and per-object version numbers;
- conditional multi-object reads using `Last-Modified-Version` / `If-Modified-Since-Version`;
- object-level optimistic concurrency using `version` / `If-Unmodified-Since-Version`;
- item relations in item JSON;
- write/update/delete APIs;
- established sync semantics.

Therefore:

```text
LIBRARY SYNC != EVIDENCEWATCH GAP
ZOTERO ITEM CHANGE DETECTION != EVIDENCEWATCH NOVELTY
OPTIMISTIC CONCURRENCY != EVIDENCEWATCH NOVELTY
GENERIC ITEM RELATIONS != EVIDENTIARY ANCESTRY
```

EvidenceWatch should interoperate with these owner surfaces rather than build a parallel Zotero sync engine.

## Critical version distinction

Zotero object versions describe the state of the **library object**.

They do not by themselves establish:
- that the underlying journal article, preprint, dataset or owner page changed;
- which source representation is authoritative;
- whether two Zotero items share one evidentiary root;
- whether a changed source matters to a relied-on extraction/recommendation.

Preserve:

```text
ZOTERO ITEM VERSION != SOURCE PUBLICATION / DATASET VERSION
ZOTERO RELATION != PROVED EVIDENTIARY LINEAGE
LIBRARY MODIFIED != SOURCE EVIDENCE MODIFIED
SOURCE MODIFIED != DOWNSTREAM REVIEW REQUIRED
```

## Smallest plausible Stage 1 adapter

If a real pilot survives owner correction, start read-only.

### Input side

Use either:
1. desktop Local API for a researcher-controlled local pilot; or
2. Web API with a deliberately scoped user key/OAuth route if remote access is actually needed.

Read:
- item key;
- Zotero item version;
- bibliographic fields/DOI/URL;
- existing relations;
- collection/context needed to identify the pilot corpus.

Use Zotero's conditional version mechanism to avoid repeatedly re-reading an unchanged library.

### EvidenceWatch side

Keep separately:
- exact relied-on source identity/state;
- owner version/currentness signal;
- configured state authority;
- evidentiary independence/lineage;
- bounded claim;
- approved downstream dependency mapping;
- EvidenceWatch observation/review history.

Do not reinterpret Zotero's object version as source authority.

### Output side

Stage 1 should not require writing back into Zotero.

First prove:
- current library can be read reliably;
- source-state signals can be bound to the intended library items;
- alerts can be presented externally/in shadow mode;
- setup + recurring maintenance burden can be measured.

Only if that survives should a later separately authorised design consider:
- a tag/note/linked item;
- a plugin;
- external review queue;
- other write-back path.

```text
READABLE INTEGRATION != WRITE AUTHORITY
SHADOW ALERT != LIBRARY MUTATION
API CAPABILITY != PERMISSION TO ACT
```

## Falsification conditions

Zotero is the wrong first host if:
- the actual partner workflow does not use it;
- the existing review platform already owns the needed source-state linkage;
- mapping source-state signals to Zotero items is brittle or ambiguous;
- library metadata lacks the stable identifiers needed at acceptable burden;
- a read-only adapter adds no value compared with the workflow's existing integration.

If a stronger host exists:

**USE THE STRONGER HOST / DO NOT FORCE ZOTERO.**

## Project consequence

No EvidenceWatch source delta is earned.

The grant/pilot plan can be more concrete without pretending integration already exists:

> first prove a read-only adapter from an existing reference library into the frozen shadow-mode measurement path; defer write-back until benefit and authority are established.

No Zotero credentials, user data, write action, plugin publication or external contact occurred.
