# PSFH Phase 0 — ICO prospective source rule v0.2 amendment

Status: **DRAFT AMENDMENT / PRE-EXECUTION / NO SOURCE OBJECT SELECTED / NO CASE READING / NO STUDY AUTHORITY**  
Date: 11 September 2026, Europe/London

Parent candidate:
- `evidence/PSFH_PHASE0_ICO_PROSPECTIVE_SOURCE_RULE_V0_1_20260911.md`

This amendment changes only two source-selection mechanics in v0.1. Everything else remains in force unless explicitly replaced here.

`AMENDMENT != SOURCE_FREEZE`

---

## 1. Delete the pre-ranking carrier-length selector

Delete the v0.1 requirement to define or apply:

```text
MAX_CARRIER_WORDS
```

There is **no word-count, page-count or byte-count eligibility threshold before source ranking or Stage-A reference fixation** under this candidate.

Reason:

- a pre-ranking length threshold can act as a hidden case-shape filter;
- shorter is not evidence of fairer, more representative or more useful;
- the Phase-0 construct already has a separate pre-execution human/provider burden gate;
- source choice should therefore remain mechanical and content-blind rather than prefer notices because they are easier to run;
- task burden can be assessed after the three Stage-A references are irreversibly fixed, without substituting different cases in response.

Replacement rule:

```text
carrier_preselection_gate := deterministic_extraction_success_only
post_selection_burden_gate := dry_time_the_fixed_A1_A2_A3_packet
burden_failure != choose_different_cases
```

After A1/A2/A3 references are mechanically fixed:

1. generate the deterministic text-only carriers under the separately frozen extraction rule;
2. perform the required non-participant dry timing / operational burden check on that fixed packet;
3. if the fixed packet is impractically burdensome, return `OPERATIONAL_NULL/INCOMPLETE` or repair the broader study design before participant exposure;
4. do **not** replace a fixed reference merely because another notice is shorter or easier.

Extraction failure before ranking remains a source-availability failure because no stable participant carrier exists. Carrier length by itself is not a source-selection criterion.

`SHORTER_CASE != FAIRER_CASE`  
`BURDEN_CHECK != CASE_SHOPPING`  
`FIXED_CASES_TOO_BURDENSOME -> OPERATIONAL_NULL`

---

## 2. Freeze exact confirmatory schema compatibility

V0.1 leaves open whether an August schema difference might be handled by a later compatibility rule. Remove that discretion for this candidate.

The confirmatory August completed-case CSV must have the **exact ordered header row** already observed on the permanently excluded July development fixture:

```json
["Case_Reference2","CaseStatus1","Legislation","Received_Datetime1","Completed_DateTime1","Sector","SubSector","Decision_Primary_Reason1","Submitted_About_Account","Submitted_About_Account_Region","Decision","DecisionDetail1","DecisionDetail2","PriorityCase1"]
```

The source-role headers are fixed exactly as:

```text
REFERENCE_HEADER_EXACT      := Case_Reference2
COMPLETED_DATE_HEADER_EXACT := Completed_DateTime1
DECISION_DETAIL_1_HEADER_EXACT := DecisionDetail1
```

Rules:

- exact ordered header equality -> schema gate passes;
- any added, removed, renamed, reordered or duplicate header -> `SOURCE_SCHEMA_CHANGED` and stop this candidate;
- do not infer equivalent columns by position, label similarity, data values or owner prose;
- do not create an August-specific remapping after row counts or values are visible;
- a later successor design may deliberately support another schema, but that is a new frozen candidate, not an in-run repair.

This is intentionally conservative. A harmless upstream schema change may kill this candidate. That cost is preferable to retaining hidden operator discretion about which changed columns preserve the desired universe.

`SEMANTICALLY_SIMILAR_HEADER != FROZEN_HEADER_IDENTITY`  
`SCHEMA_CHANGE != PERMISSION_TO_REMAP`  
`SOURCE_SCHEMA_CHANGED -> STOP_THIS_CANDIDATE`

---

## 3. What remains unresolved

This amendment does **not** fill values that still require the bounded development-fixture metadata probe already dispatched in COM #119:

```text
DN_SERVED_VALUE_EXACT := UNSET
SOURCE_DATE_FORMAT_EXACT := UNSET
```

Those values may be frozen only from owner documentation and/or the permanently excluded development fixture under the existing no-join/no-case-reading constraints. They may not be learned from confirmatory August row distributions.

The August source object itself remains unselected/unavailable until the prospective v0.1 owner-page rule resolves it.

---

## 4. Consequential boundary unchanged

This amendment does not authorise:

- choosing or downloading a confirmatory August object for study execution;
- reading a confirmatory row or Decision Notice body;
- ranking or selecting Stage-A cases;
- participant recruitment, screening or contact;
- provider account creation or funding;
- paid inference or other spend;
- a public study or usefulness claim;
- TRACE/ME/PSFH release or canon mutation.

It only removes two future degrees of freedom from the draft source rule.

```text
PROSPECTIVE_RULE != SOURCE_SELECTION
SOURCE_SCHEMA_FIXED != SOURCE_OBJECT_SELECTED
BURDEN_PARAMETER_DELETED != BURDEN_IGNORED
SOURCE_RULE_REPAIR != EXECUTION_AUTHORITY
```
