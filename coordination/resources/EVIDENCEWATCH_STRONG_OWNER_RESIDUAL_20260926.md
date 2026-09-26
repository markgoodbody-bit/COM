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

## Surviving residual

The remaining falsifiable seam is narrower:

> Can an agent catch a material change to an **already-relied-on source** when it arrives as neither a new study nor a formal status event, then route only affected downstream work for human review?

Examples may include:
- preprint -> final-authoritative publication where substantive content changes;
- dataset revision under a stable research object/lineage;
- owner page or technical evidence revision after reliance;
- source authority succession or corrected content not captured by formal retraction/correction tooling.

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
