# ATRS Answerability Audit — middle-out research delta

Status: **WORKING RESEARCH ORIENTATION / NOT RESULT / NOT SELECTED ENTRY / NOT SUBMISSION**  
Date: 17 September 2026

> **HOW CAN WE MAKE A BETTER FUTURE?**

This note records a wider owner-subtraction pass after the September ATRS source/method work. It does not supersede the frozen evidence, the reader-use protocol, or the human-study gate. It sharpens the question that would be worth answering next.

## Start from the world, not the register

The real scene is not an ATRS field.

A person encounters a public service or decision process in which an algorithmic tool may contribute. They may want to know:

- what the tool did;
- how that output entered the broader process;
- whether the **tool output** can be challenged, corrected or reviewed;
- whether the **broader operational decision/process** can be challenged, corrected or reviewed;
- who can initiate the relevant route;
- how they initiate it;
- whether the route is current, planned, unavailable or unclear;
- what the route can actually change.

The ATRS record is one public aperture onto that situation. `RECORD != WORLD`.

## Strong owners — subtract before claiming

### Government Digital Service / ATRS

GDS owns the standard, template, field semantics and repository.

Current v4 guidance is unusually specific about the `Appeals and review` field. It says publishers should consider **both**:

1. the output of the algorithmic tool itself and whether it can be challenged or appealed; and
2. the output of the broader operational process and whether it can be challenged or appealed.

It also says this may involve a public appeal/contact link, and where no appeal/review process is relevant the record should explain why.

Source:
https://www.gov.uk/government/publications/guidance-for-organisations-using-the-algorithmic-transparency-recording-standard/algorithmic-transparency-recording-standard-guidance-for-public-sector-bodies

GDS's May 2025 v4 announcement says the prompts were refined for clarity after user feedback and explicitly lists a next step of assessing whether existing records achieve the impact originally intended.

Source:
https://dataingovernment.blog.gov.uk/2025/05/08/making-the-algorithmic-transparency-recording-standard-atrs-mandatory-across-government/

Therefore this project does **not** own the idea that appeal information matters or that tool/process layers should be distinguished.

### Contestability / public-service research

Existing research already owns much of the generic argument that transparency, explanation or a nominal review route does not by itself create meaningful contestability.

- Yurrita et al. (2025), *Identifying Algorithmic Decision Subjects' Needs for Meaningful Contestability*: decision subjects need cooperation in sense-making, support in contestation acts and appropriate responsibility attribution.
  https://doi.org/10.1145/3757415
- Karusala et al. (CHI 2024), *Understanding Contestability on the Margins*: exercising contestation rights can require substantial accompaniment through social and institutional barriers.
  https://www.eecs.harvard.edu/~kgajos/papers/2024/karusala2024understanding.shtml
- Das et al. (FAccT 2026), *Bureaucratic Silences*: a complete Canadian-register study argues that transparency artifacts can offer visibility while obscuring sociotechnical context and contestability.
  https://doi.org/10.1145/3805689.3812336
- Nieuwenhuizen (2025), *Algorithm Registers: A Box-Ticking Exercise or Meaningful Tool for Transparency?*: empirical work on Dutch registers already examines whether registers are useful to public-interest users and the less-direct organisational effects they may create.
  https://doi.org/10.1177/15701255241297107

Therefore do **not** claim:

```text
OUR_FINDING = TRANSPARENCY_IS_NOT_CONTESTABILITY
OUR_FINDING = PEOPLE_NEED_USABLE_APPEALS
OUR_FINDING = REGISTER_FIELDS_CAN_BE_HETEROGENEOUS
```

Those territories have strong owners.

### Existing ATRS corpus / public-law work

Existing work already harvests and maps ATRS records and broader public-sector automated decision-making. A metadata corpus or another general register index is not enough of a delta.

`CORPUS_EXISTS != RESEARCH_DELTA`.

## Residual question that survives subtraction

The sharper empirical question is:

> **Across actual ATRS records, what challenge/review relationship is made legible to a reader at the tool-output layer and at the broader operational-process layer, through what stated actor/channel/status, and how does that disclosure vary across standard versions and tool roles?**

This is narrower than `is ATRS transparent?` and stronger than `free-text fields vary`.

It directly tests the public implementation of a distinction the standard itself asks publishers to make.

A secondary descriptive question is:

> **Do records published under v4 more often make that two-layer relationship explicit than records using earlier template versions?**

This must remain descriptive unless a design capable of supporting a causal claim is earned.

```text
VERSION_ASSOCIATION != VERSION_CAUSED_CHANGE
V4_RECORD != BETTER_RECORD_BY_DEFINITION
FIELD_PRESENT != TWO_LAYER_RELATIONSHIP_LEGIBLE
NO_TOOL_SPECIFIC_APPEAL != NO_USABLE_BROADER_PROCESS_ROUTE
```

## Candidate November measurement

Use a **fresh sprint-time corpus** if live Apart rules permit the project.

### 1. Freeze the live public population

- finder membership;
- independent Search API comparison;
- exact source bytes and fetch time;
- record URL and source hash;
- declared ATRS version where observable;
- parser/code head.

Fail closed on unexplained population mismatch.

### 2. Preserve the deployment relationship

Do not code `Appeals and review` in isolation when the load-bearing question is which layer can be challenged.

For each record, preserve evidence sufficient to distinguish:

```text
TOOL_OUTPUT_ROLE
BROADER_OPERATIONAL_PROCESS
DEGREE / DESCRIPTION OF HUMAN INVOLVEMENT
APPEALS_AND_REVIEW_TEXT
```

This is not permission to infer hidden practice. Code only what the public record supports.

### 3. Code the challenge relationship

Primary axis:

```text
challenge_layer :=
  TOOL_OUTPUT
  BROADER_OPERATIONAL_PROCESS
  BOTH_EXPLICIT
  NO_RELEVANT_PROCESS_STATED_WITH_REASON
  NOT_STATED_OR_UNCLEAR
```

Additional evidence-bound dimensions:

```text
initiator_or_actor
route_form
channel_or_locator
challenge_object
status
published_evidence
coder_disagreement
```

`route_form` should remain multi-label where necessary, for example:

```text
CONCRETE_RECONSIDERATION_OR_COMPLAINT_LOCATOR
NAMED_REVIEW_OR_APPEAL_PROCESS_WITHOUT_LOCATOR
IN_CHANNEL_HUMAN_HANDOFF
RETRY_OR_ALTERNATIVE_PATH
GENERAL_HELP_OR_FEEDBACK
DATA_RIGHTS_ROUTE
EXPLANATION_OR_AUDIT_TRAIL_WITHOUT_RECOVERY
PLANNED_NOT_OPERATING
EXPLICIT_NO_SEPARATE_PROCESS
AMBIGUOUS
```

Do not force unlike routes into a single quality score.

### 4. Stratify rather than rank

Useful descriptive cuts may include:

- ATRS version: v4 / v3 / earlier where observable;
- tool role: advisory/supporting vs materially decision-shaping, only where the record supports the distinction;
- challenge layer;
- locator/process/handoff form;
- current/planned/unavailable/unclear status.

Report cells and evidence, not department league tables.

### 5. Preserve disagreement

Use at least two genuinely differentiated coding apertures where feasible. Freeze independent first labels before reconciliation. Preserve disagreement rather than treating consensus as truth.

```text
TWO_CODERS_AGREE != WORLD_VALID
DISAGREEMENT != FAILURE
RECONCILIATION != ERASE_FIRST_READ
```

### 6. Reader-use pilot is secondary, not the research spine

The existing `FULL / EXCERPT / LENS` method remains useful for a separate question about retrieval cost and deterministic grouping.

It is **not required** for the core fresh-corpus measurement above.

If a human pilot is later authorised:

```text
EXCERPT ~= LENS
-> DO NOT RESCUE THE LENS
-> ROUTE BENEFIT TO SIMPLER SECTION-JUMP / EXCERPT OWNER
```

No human-study gate is crossed by this note.

## Falsifiers / kill paths

Shrink or stop if any of these occur:

1. current records already make the tool-output / broader-process distinction sufficiently explicit and uniform that no consequential descriptive gap remains;
2. standard version cannot be established reliably enough for the proposed stratification;
3. the layer coding cannot survive concrete cases without large unresolvable inference;
4. variation is explained almost entirely by legitimate tool-role differences and the residual adds no useful information;
5. an existing owner already provides the same current ATRS full-corpus, layer-bound challenge analysis;
6. the result still reduces to `free-text fields vary`;
7. the result requires a moral/compliance score to look interesting;
8. sprint rules make the prepared work inadmissible and no fresh substantive object can be produced cleanly during the event.

`NULL_RESULT = VALID`.

## What a surviving result would actually say

A strong result would be modest and inspectable, for example:

> The ATRS standard asks publishers to distinguish challenge of the algorithmic tool's output from challenge of the broader operational process. In a fresh public-register census, we measured how often and in what form that relationship was actually made explicit, where it remained ambiguous, and how the pattern differed descriptively across record versions and tool roles.

The data may support or reject that sentence. Do not preregister the conclusion.

## Why Apart currently fits without bending the work

Apart's November AI x Epistemics Open Track explicitly asks what can be measured about a **live epistemic deployment** using data downloadable over the weekend and what the measurement means for the field.

Source:
https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15

This ATRS question can be answered with a fresh public corpus, reproducible extraction, evidence-bound coding and a short investigative research write-up. It does not require pretending the project is an agent product or buying a platform.

Other live competition routes should stay separate:

- Open Agent Hackathon asks teams to build an agent that does real work. Turning this audit into an agent solely to fit that brief would distort the current residual question.
- Nebius/NVIDIA routes require platform/product integration. Use them only if a genuinely useful product independently earns that architecture.

```text
COMPETITION_FIT != PROJECT_PURPOSE
BIGGER_PRIZE != BETTER_RESEARCH_OBJECT
BUILD_IF_USEFUL_WITHOUT_PRIZE
POSSIBLE_PRIZE = 0 UNTIL AWARDED
```

## Connection back to the project

Mechanical Ethics / TRACE helped us notice `route exists != route usable`, `explanation != recovery`, layer mismatch, clocks and answerability. That is discovery history, not ownership of the empirical result.

The external question stands without TRACE or ME:

> When government publishes an algorithmic transparency record, can a reader tell **what can be challenged, at which layer of the process, by whom, and how?**

If the answer is already adequately supplied by the standard and its implementation, stop.

If not, measure the exact gap and hand the finding back to the stronger owner.

```text
PROJECT_LANGUAGE_HELPED_US_SEE_IT != PROJECT_OWNS_IT
OWNER_FOUND -> ROUTE
SPECIFIC_GAP -> SMALLEST_HELP
PURPOSE > INSTRUMENT
```