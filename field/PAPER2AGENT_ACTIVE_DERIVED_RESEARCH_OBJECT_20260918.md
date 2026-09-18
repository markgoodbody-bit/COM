# Paper2Agent — derived active research object boundary case — 18 September 2026

Status: **CURRENT PEER-REVIEWED SCIENCE FIELD CASE / DERIVED EXECUTABLE INTERFACE / OWNER-RICH / NOT THR ROADMAP / NOT TRACE-ME CANON**

Primary source:
Miao et al., *Reimagining research papers as interactive and reliable AI agents*, Nature, published 16 September 2026:
https://www.nature.com/articles/s41586-026-11044-y

Code:
https://github.com/jmiao24/Paper2Agent

Purpose: preserve a current example where static research outputs are converted into agent-usable executable interfaces while retaining source resources, code references and validation traces.

## What Paper2Agent does

The framework analyses a paper plus associated codebase and constructs an MCP server exposing:
- manuscript/code/data/supplementary materials as resources;
- executable methodological functions as MCP tools;
- workflow prompts derived from the paper/code;
- a downstream conversational agent interface.

The paper reports automated environment setup, function extraction, test generation/execution, repair loops and exclusion of functions that repeatedly fail validation.

Every exposed tool includes a code reference back to the original paper/codebase.

Reported study result:
- 100 computational-biology papers evaluated;
- 74 successfully agentified;
- 599 proposed tools;
- 593 passed automated validation;
- major failures included absent executable code/data/model artefacts, dependency/environment failures and non-generalizable scripts.

Those numbers describe the paper's benchmark, not a universal rate for scientific literature.

## The semantic boundary

Popular shorthand says the paper 'becomes an agent'. Mechanically, the source objects remain distinct from the generated interface.

```text
PAPER / MANUSCRIPT
+ CODE / DATA / SUPPLEMENTS
+ GENERATED MCP RESOURCES / TOOLS / PROMPTS
+ DOWNSTREAM LLM AGENT
-> PAPER-SPECIFIC ACTIVE INTERFACE
```

Therefore:

```text
PAPER != AGENT
AGENTIFIED INTERFACE != ORIGINAL SOURCE
DERIVED TOOL != SOURCE METHOD BY IDENTITY
MCP RESOURCE != EVIDENCE UPGRADE
```

## Validation boundary

Paper2Agent validates tools against reference code/tutorial outputs, including numerical/file/figure checks. That is strong engineering evidence for reproducibility of the exposed functions.

It is not automatically scientific validation of every claim in the source publication.

```text
TOOL REPRODUCES REFERENCE OUTPUT != SCIENTIFIC CLAIM TRUE
TEST PASS != METHOD VALID IN EVERY NEW DOMAIN
EXECUTABLE != EPISTEMICALLY AUTHORITATIVE
CODE REFERENCE != CODE CORRECT
```

The paper itself preserves this distinction in practice by maintaining source resources, code references, tests and failure logs.

## Relation to The Human Record

THR currently treats human views as derived views over records, with source-byte/currentness boundaries and no evidence upgrade from presentation.

Paper2Agent provides an external contemporary analogue for a more active derived view:

```text
DERIVED VIEW CAN BE INTERACTIVE / EXECUTABLE
WHILE
SOURCE / VIEW / TEST / CLAIM REMAIN DISTINCT
```

This does **not** earn an executable THR layer.

THR's current three records are provenance/source-lineage objects, not computational methods whose code naturally supports executable tooling. Adding agentification would create security, maintenance, authority and false-currentness burdens not justified by current THR use.

## Relation to TRACE / ME

Existing distinctions are sufficient:

```text
RECORD != EVENT
REPRESENTATION != WORLD
DERIVED VIEW != SOURCE
EXECUTED != ADJUDICATED
CAPABILITY != AUTHORITY
```

Paper2Agent adds a real modern witness that representations can become active without ceasing to be derived.

## Positive construction aspect

The work also demonstrates a real constructed capability:

```text
STATIC RESEARCH OUTPUT
+ PUBLIC CODE / DATA
+ AGENTIFICATION / TESTING
-> NEW ACCESS / EXECUTION CAPABILITY
```

But:

```text
LOWER ACCESS BARRIER != SCIENTIFIC UNDERSTANDING GUARANTEED
FASTER REUSE != CORRECT REUSE GUARANTEED
ACTIVE KNOWLEDGE OBJECT != INDEPENDENT CORRESPONDING AUTHOR
```

## Current disposition

```text
DERIVED ACTIVE INTERFACE = REAL OWNER-SUPPORTED PATTERN
PROVENANCE / TEST TRACE = OWNER-SUPPORTED
NEW THR FEATURE = NO
NEW TRACE/ME PRIMITIVE = NO
PRACTICAL PROJECT DELTA = NONE ESTABLISHED

RESULT = KEEP AS ACTIVE-RECORD / DERIVED-VIEW BOUNDARY WITNESS
```

Wake only if THR later has a real computational/executable record whose human/machine use is materially improved by an active interface and whose provenance/currentness/security burden can be bounded.
