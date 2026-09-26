# EvidenceWatch — stronger-owner residual after EPPI / MAGIC pass

Date: 26 September 2026

Status: **OWNER-SUBTRACTED RESIDUAL / NO FEATURE DELTA / NO USER VALIDATION**

Purpose:

Test the surviving EvidenceWatch problem after comparing it with current living-evidence owners.

## EPPI-Reviewer already owns more than generic update discovery

Current public EPPI evidence establishes:
- OpenAlex-based auto-update for living reviews;
- regular new-record suggestions ranked by machine-learning relevance;
- Zotero round-trip integration where edits made in Zotero can be re-imported to update EPPI item records;
- fixed/enumerated search-result snapshots with enumeration timestamps;
- source metadata recording what was imported and how;
- an Origin Report showing, per item, where it appeared and what source imported it;
- explicit support for evaluating living-evidence update-cycle coverage.

Owner surfaces:
- https://eppi.ioe.ac.uk/cms/er4/help/openalex-in-eppi-reviewer/keeping-a-review-up-to-date-auto-update
- https://eppi.ioe.ac.uk/cms/er4/help/zotero-integration
- https://eppi.ioe.ac.uk/cms/er/Help/Version-History-Announcements/Latest-Changes-16-04-2026-V61800

Therefore:

```text
NEW_RECORD_DISCOVERY != EVIDENCEWATCH GAP
IMPORT_PROVENANCE != EVIDENCEWATCH NOVELTY
ZOTERO_ROUND_TRIP != EVIDENCEWATCH NOVELTY
SEARCH_SNAPSHOT_PROVENANCE != EVIDENCEWATCH NOVELTY
```

## MAGIC already owns downstream living-guideline materiality workflow

Current MAGIC evidence establishes:
- structured living-guideline authoring and updating;
- full audit trail/activity log;
- recommendation-level publication;
- current monthly evidence-surveillance workflows;
- human reconvening only when new evidence is likely to affect certainty, benefit/harm balance or relevant context;
- single-source publication/live-widget patterns that reduce duplicate maintenance.

Owner surfaces:
- https://www.magicevidence.org/magicapp/
- https://www.magicevidence.org/featured%20guideline/2026/09/03/building-a-living-guideline-program-in-oral-health.html

Therefore:

```text
LIVING_GUIDELINE_VERSIONING != EVIDENCEWATCH GAP
GENERIC_MATERIALITY_ROUTING != EVIDENCEWATCH NOVELTY
HUMAN_RECONVENE_TRIGGER != EVIDENCEWATCH NOVELTY
```

## ALEC / Monash raises the architecture ceiling further

Current Living Evidence Architecture work combines living-evidence synthesis, software, AI/NLP, digital health and regional co-design.

Owner surface:
- https://www.monash.edu/mada/research/project/living-evidence-architecture

Do not position EvidenceWatch as a general living-evidence architecture.

## ALEC subtraction — preprint currentness is explicitly owned

ALEC's Living Guidelines Handbook v1.1 explicitly advises guideline developers who use preprints to:
- implement literature-surveillance measures to identify when the article is published in a peer-reviewed journal;
- document a priori how preprints are monitored;
- recheck and incorporate the data once peer-reviewed data are published.

Owner surface:
- https://livingevidence.org.au/wp-content/uploads/Living-Guidelines-Handbook-v1.1-Aug2025.pdf

Therefore:

```text
PREPRINT -> PEER-REVIEWED PUBLICATION MONITORING
!= EVIDENCEWATCH GAP

PREPRINT DATA RECHECK AFTER PUBLICATION
!= EVIDENCEWATCH NOVELTY
```

Preprint -> final-publication pairs remain useful **historical/calibration/test fixtures** because they supply known same-lineage source transitions. They must not be used as evidence that living-guideline teams lack a route for this class.

## Dataset-version subtraction — identity/provenance is already strongly owned

Current infrastructure already owns much of dataset-version identity:

- **DataCite** recommends updating DOI metadata for minor versions and assigning/linking a new DOI for major versions. Its relation vocabulary includes `IsPreviousVersionOf`, `IsNewVersionOf`, `HasVersion` and `IsVersionOf`, and its metadata provenance records changes.
- **Figshare** versions public items/collections, keeps prior versions visible, gives each version a DOI, and uses a base DOI that resolves to the latest public version.
- **Zenodo** creates a new immutable record/persistent identifier for a new file version and links versions so a citation to a specific version remains stable.
- **W3C PROV** already owns generic revision provenance through `wasRevisionOf`.

Owner surfaces:
- https://support.datacite.org/docs/versioning
- https://info.figshare.com/user-guide/how-versioning-works/
- https://help.zenodo.org/docs/deposit/manage-versions/
- https://www.w3.org/ns/prov

Figshare is also a **Digital Science solution**, making this subtraction directly relevant to the Catalyst application:
- https://www.digital-science.com/products/figshare/

Therefore:

```text
VERSIONED DATASET SUCCESSOR IDENTITY
!= EVIDENCEWATCH GAP

DATASET VERSION PROVENANCE
!= EVIDENCEWATCH NOVELTY

OWNER VERSION SIGNAL EXISTS
!= DOWNSTREAM RELIANCE AUTOMATICALLY REOPENED
```

EvidenceWatch should consume trusted registry/repository version signals where available rather than model-guessing succession from text.

The remaining dataset question is integration:
- whether a version/change matters to the bounded relied-on claim;
- whether it affects already-used extraction/synthesis/recommendation state;
- whether the current workflow already routes that consequence cheaply;
- what happens when version/currentness signals are incomplete, fragmented or disconnected from downstream work.

## Web-state subtraction — change detection/preservation is already strongly owned

Generic web-page change detection and prior-state preservation also have stronger owners:

- **Memento / RFC 7089** defines time-based access to prior states of web resources.
- **Perma.cc** preserves cited web pages so relied-on content remains retrievable even if the live source changes or disappears.
- **changedetection.io** provides scheduled web-page monitoring, timestamped change history, alerts and an API for managing watches.
- **Visualping** provides scheduled page monitoring, before/after comparisons, API/workflow integrations and AI-assisted importance filtering.

Owner surfaces:
- https://www.rfc-editor.org/info/rfc7089/
- https://perma.cc/about
- https://changedetection.io/
- https://changedetection.io/docs/api_v1/
- https://visualping.io/

Therefore:

```text
WEB PAGE CHANGED
!= EVIDENCEWATCH GAP

WEB STATE PRESERVATION
!= EVIDENCEWATCH NOVELTY

CHANGE ALERT
!= RELIED-ON DOWNSTREAM CONSEQUENCE
```

EvidenceWatch should consume stronger web-change/history signals where practical rather than re-claiming generic page monitoring.

The remaining web-source question is the same integration question:
- was this exact source/state actually relied upon;
- does the change alter the bounded proposition or evidence state that mattered;
- which already-relied-on extraction/synthesis/brief/recommendation depends on it;
- is reopening that downstream work worth the human burden;
- does the existing workflow already answer those questions adequately.

## Surviving residual

The remaining falsifiable seam is narrower:

> Can an agent catch a material change to an **already-relied-on source** that is not already handled by the workflow's ordinary new-study, preprint-publication, retraction or formal-correction routes, then route only affected downstream work for human review?

Examples may include:
- dataset/source revision whose owner version signal is absent, fragmented, or not connected to already-relied-on downstream work;
- owner/technical-source revision where a change/history signal exists but is not connected to the specific downstream work that relied on the prior state;
- source authority succession or corrected content not captured by standard publication/retraction/correction tooling.

Existing EvidenceWatch machinery can represent this seam, but representation is not evidence that it saves work.

```text
REPRESENTABLE != USEFUL
RESIDUAL IDENTIFIED != RESIDUAL FREQUENT
RESIDUAL FREQUENT != AUTOMATION BENEFICIAL
OWNER FOUND / STOP REMAINS LIVE
```

## What would falsify the residual

Stop or narrow if a strong current workflow shows that:
- these same-lineage/post-reliance changes are already caught reliably;
- the events are too rare to justify maintenance;
- human verification burden exceeds any saving;
- dependency routing adds more work than it removes;
- formal/new-record pathways already capture nearly all consequential cases.

## Project consequence

No EvidenceWatch code delta is earned.

The next useful evidence remains:
1. one real current workflow;
2. historical/current episodes in this narrow residual class;
3. existing detection/routing process;
4. measured reviewer minutes, misses and false alerts.

No external contact was made.
