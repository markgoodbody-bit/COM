# EvidenceBridge v0 proof contract

Status: **PRE-RESULT PRODUCT FALSIFIER**

This contract is fixed before judging the generated examples.

## Product question

> Does a small source-bound evidence representation make important source relationships easier to inspect without manufacturing certainty?

The comparison is against competent ordinary reading of the same bounded material, not against a weak straw-man workflow.

## P1 — flak / dependence

Input contains an early video carrying the 80% claim; an article and automated summary downstream of that video; a later video carrying/questioning the figure; and nearby official evidence about a different population/measure.

Required: `DOWNSTREAM RESTATEMENT != INDEPENDENT SUPPORT` and `NEARBY DIFFERENT STATISTIC != SUPPORT`.

Pass:
- independent support groups for the mortality claim = 0;
- downstream restatements remain visible;
- verdict does not say false;
- unknown aggregate mortality remains visible.

## P2 — Hannibal / translation + attribution

Input contains a checked Nepos Latin surface; a checked Polybius 1922 Loeb English reading surface; explicit note that Greek source literal was not inspected; and Polybius' criticism of Sosylus/Chaereas.

Required: `ENGLISH_TRANSLATION_LITERAL != CHECKED_GREEK_LITERAL` and `POLYBIUS_CRITICISES_SOSYLUS != EVIDENCEBRIDGE_ADJUDICATES_SOSYLUS`.

Pass:
- Greek-literal claim remains unresolved;
- source-criticism truth claim remains unresolved;
- both source reports remain inspectable.

## P3 — R. Vale / unresolved identity

Input contains programme A and catalogue B with the identical "R. Vale — Harbour Study, 2024" string; no evidence capable of deciding one-maker vs two-maker world; and Source C reporting that A's R. Vale is not B's maker.

Required: `SAME_STRING != SAME_ENTITY`, `SOURCE_C_REPORT != DIRECT_OBSERVATION`, `UNRESOLVED = VALID_RESULT`.

Pass:
- same-maker focal claim is not resolved from identical strings;
- Source C appears as a reported contradiction;
- engine verdict remains unresolved rather than asserting two people.

## P4 — traceability

For every focal claim analysis:
- every proposition id resolves;
- every source id resolves;
- source URL/locator is displayable when supplied;
- relation/state are visible;
- no hidden numeric scoring.

## P5 — fail closed

Validator must reject duplicate ids; unknown source or focal-claim references; invalid proposition states/relations; missing derived-from sources; derived sources placed in a different independence group from parents; and correction references to missing propositions.

## Promotion test

Only after P1–P5:

> Add one new ordinary case not used to design v0.

If that requires changing the ontology rather than adding data, v0 has not earned product continuation.

No Open Agent registration/submission follows from passing this contract.
