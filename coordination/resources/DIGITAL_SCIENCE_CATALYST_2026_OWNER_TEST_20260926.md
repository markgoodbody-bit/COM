# Digital Science Catalyst 2026 — EvidenceWatch owner-test matrix

Date: 26 September 2026

Status: **PRE-SUBMISSION EVIDENCE CHECK / NOT SUBMITTED / HUMAN GATE UNCHANGED**

Owner surfaces rechecked 26 September 2026:
- https://www.digital-science.com/about-us/investment/catalyst-grant/
- live Google Form landing page linked by the owner page.

The owner explicitly asks applicants to test six things before applying:
1. the research decision, who makes it, when/how often;
2. research-lifecycle fit;
3. the existing tool/system the agent must live inside;
4. whether the work genuinely needs multiple steps;
5. a task the agent should refuse, flag or escalate;
6. a measurable outcome.

## Current EvidenceWatch fit

| Owner test | Current EvidenceWatch answer | Evidence state |
| --- | --- | --- |
| Research decision | Whether owner version/currentness signals or residual source changes require reopening already-relied-on synthesis/review work | **DEFINED / NOT USER-VALIDATED** |
| Who / how often | Living systematic review team. Public Bern exemplar ran weekly searches adding 100–200 records and checked preprint status each update | **PUBLIC BASELINE / NOT UNIVERSAL FREQUENCY** |
| Lifecycle | Evidence synthesis + research integrity | **DIRECT FIT** |
| Existing tool/system | Proposed first integration target: Zotero / an existing reference library | **FILE HANDOFF EXISTS / LIVE INTEGRATION DOES NOT** |
| Multi-step need | Observe -> fingerprint -> compare -> analyse relevant change -> preserve authority -> route affected dependents -> human review | **IMPLEMENTED AS PROTOTYPE** |
| Refuse / flag / escalate | Derivative repetition stays quiet; derivative disagreement flags review; candidate sources cannot gain authority; outage preserves prior state | **DETERMINISTICALLY TESTED / NOT RESEARCHER-VALIDATED** |
| Primary outcome | Reviewer minutes per correctly handled material-change episode versus existing practice | **PREDECLARED / UNMEASURED** |
| Secondary outcomes | Time-to-flag, misses, false alerts, setup/maintenance minutes, explanation reconstruction | **PREDECLARED / UNMEASURED** |
| Current stage | Working standalone prototype, demo, CSL-JSON handoff, pilot protocol/scorer, 62 deterministic tests | **ENGINEERING EVIDENCE** |
| Users/customers | None | **ABSENT / DISCLOSED** |
| Competitors/owners | Cochrane, Crossref/Europe PMC, DataCite, Figshare, Zenodo, Memento, Perma.cc, Visualping, changedetection.io, Zotero/Crossmark, ReadCube, scite, EPPI-Reviewer, MAGICapp, ALEC/Monash, Refract, AIEP P170 | **OWNER-SUBTRACTED / SUBSUMPTION RISK HIGH** |
| Commercial market | Possible institutional/team workspace/integration buyer; pricing untested | **HYPOTHESIS ONLY** |
| Team | Mark: systems/infrastructure/audit/failure-recovery expertise; no established research-workflow partner | **ENGINEERING STRENGTH / DOMAIN-PARTNER GAP** |
| Budget | Staged £5k / £14k / £6k with stop gates | **DRAFT / HUMAN GATE** |

## Public burden baseline

The University of Bern practical guide provides a bounded real-workflow baseline:
- automated search ran weekly;
- 100–200 new records were uploaded each week;
- preprint publication status was checked in each update;
- data were re-extracted if content changed;
- the core team reported becoming overwhelmed as screening volume grew and later recruited volunteers;
- a separate mixed-methods evaluation of six living reviews reported 3–300 citations screened per month and 5 minutes–32 hours of author-team work per month.

This establishes recurring workload and a bounded time-cost context. The 5-minute–32-hour range covers whole living-review maintenance and must **not** be presented as the amount EvidenceWatch can save or as specific to post-reliance source-state monitoring.

It does **not** establish:
- EvidenceWatch time saving;
- frequency of material post-reliance changes across all reviews;
- acceptable miss/false-alert rates;
- willingness to adopt;
- Zotero integration value.

Additional workload source:
- https://doi.org/10.1186/s13643-019-1248-5

## Proposal-body count

Counted on the exact branch source from the first required heading `## 1. THE PROBLEM` through the end of `## 9. BUDGET`.

- whitespace-delimited count: **1,425**
- word-like-token count: **1,467**
- owner ceiling: **1,500 words**

Headroom is **75** by the whitespace count and **33** by the stricter word-like-token count. Final copy must be recounted in the submission editor because Google/word-processor tokenisation can differ.

## Dataset/version owner subtraction

DataCite, Figshare and Zenodo already provide strong version identity/provenance routes, and Figshare is a Digital Science solution.

Therefore the application must not imply that EvidenceWatch invents dataset-version detection. The test is whether existing owner signals plus residual un-signalled changes can be integrated with a team's actual relied-on dependency/materiality workflow at useful burden.

```text
VERSION SIGNAL != DOWNSTREAM REVIEW ROUTE
FIGSHARE / DATACITE VERSIONING != EVIDENCEWATCH NOVELTY
INTEGRATION HYPOTHESIS = STILL UNMEASURED
```

## Web-change owner subtraction

Memento, Perma.cc, Visualping and changedetection.io already own web-state preservation and generic page-change monitoring.

Therefore the application must not imply that EvidenceWatch invents website monitoring. The surviving question is whether stronger change/history signals can be bound to a specific relied-on evidence state and routed to the exact downstream work that should be reopened.

```text
PAGE CHANGE != DOWNSTREAM CONSEQUENCE
WEB MONITORING != EVIDENCEWATCH NOVELTY
RELIANCE-BINDING / MATERIALITY / ROUTING = UNMEASURED
```

## Strongest remaining weakness

```text
WORKING PROTOTYPE
+ PUBLIC WORKFLOW SPECIMEN
+ PREDECLARED PILOT
!=
REAL RESEARCHER BENEFIT
```

The strongest next evidence remains one willing current team, its existing workflow baseline, and measured reviewer minutes / misses / false alerts. More prototype features do not substitute for that.

## Human gate

Still required before any submission:
- identity/team wording review;
- live-form later pages and embedded terms;
- demo-sharing decision;
- budget acceptance;
- contact details;
- final submit.

No form entry, external contact, terms acceptance, identity disclosure or submission is authorised by this note.
