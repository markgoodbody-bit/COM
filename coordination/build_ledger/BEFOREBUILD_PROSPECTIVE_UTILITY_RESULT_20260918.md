# BeforeBuild prospective-utility result — 18 September 2026

Status: **INTERNAL METHOD VALUE OBSERVED / STANDALONE PRODUCT NOT EARNED / PR #385 CLOSE UNMERGED**

> HOW CAN WE MAKE A BETTER FUTURE?

## Question

Does BeforeBuild add material prospective value over disciplined ordinary owner/build-vs-buy review, and is its owner-adapter burden low/reusable enough to justify a standalone product?

## Baseline before BeforeBuild

COM #118 predates BeforeBuild and already established the PSFH guestbook problem and most load-bearing requirements:
- guest bytes must remain outside PSFH authored trust regions;
- v0 plain text / no links / no rich content;
- real removal rather than public-Git immutability;
- export/portability;
- bounded abuse/stop controls;
- custody, retention/backups, provider/network logs and operator capacity remain consequential;
- prefer/reuse an existing receiver if it can meet the contract rather than building a second lifecycle system.

So BeforeBuild did **not** discover the guestbook need, its safety boundary, or the principle of owner reuse.

## What BeforeBuild added prospectively

BeforeBuild selected current Remark42 v1.16.4 as a near owner and executed the actual owner against six pre-existing hard cases.

Observed owner trial:
- PASS anonymous/account-free;
- PASS true removal from current public owner readback;
- PASS export portability;
- PASS bounded abuse/stop via read-only control;
- FAIL separate PSFH trust-region representation;
- FAIL tiny no-link/no-rich-content mark contract.

Decision-core result:
`BUILD_PROBE`

Reason: a real current need existed; the relevant owner passed most hard cases but left two bounded PSFH-specific gaps.

The subsequent PSFH-specific adapter probe then closed those two bounded gaps in loopback without taking over the owner's persistence/auth/moderation/delete/export responsibilities.

Adapter probe result:
- owner intake PASS;
- pre-owner rich-content rejection PASS;
- PSFH untrusted-data row PASS;
- owner-rendered HTML ignored PASS;
- current export after delete PASS;
- public deployment NOT ATTEMPTED;
- backup erasure NOT ESTABLISHED;
- production security NOT ESTABLISHED.

## What changed because of the trial

Before the trial, #118 had a general architectural preference:
> reuse an existing receiver if it can meet the contract.

After the trial, that preference became a bounded executable statement:
> Remark42 can carry four of six tested owner responsibilities; the surviving custom work is a small PSFH content/trust adapter, while backup-erasure and production-security questions remain outside the probe.

That is useful evidence. It narrows implementation scope and prevents rebuilding storage/auth/moderation/export/delete machinery.

But it does **not** establish a novel product method or a deployment decision.

## Owner subtraction

Current build-vs-buy / vendor-selection practice already owns the core method:
- define success/acceptance criteria before selection;
- run proofs of concept on real/current use cases and edge cases;
- test candidate integrations rather than trust feature lists;
- account for integration and total ownership cost;
- stop duplicate custom work when a candidate satisfies the need.

BeforeBuild therefore cannot claim `run vendors/owners on hard cases before building` as a contribution.

## Automation-cost pressure

Current experimental surface is substantial:
- deterministic decision core: ~330 lines;
- core tests: ~158 lines;
- CI/workflow: ~774 lines;
- PSFH/Remark42 adapter: ~194 lines;
- adapter tests: ~133 lines;
- plus fixtures/docs.

Not every CI line is product code, but the present evidence shows owner execution requires materially bespoke work.

`OWNER ADAPTER COST = MATERIAL`
`REUSABLE LOW-FRICTION ADAPTER LAYER = NOT ESTABLISHED`

## Disposition

`METHOD UTILITY = OBSERVED`
`PROSPECTIVE EVIDENCE VALUE = OBSERVED`
`DECISION NOVELTY = NO`
`LOW-FRICTION REUSABILITY = NOT ESTABLISHED`
`STANDALONE PRODUCT UTILITY = NOT EARNED`
`OPEN AGENT / NEBIUS PRODUCT = NOT EARNED`

Therefore:

**Preserve BeforeBuild as an internal operating tactic, not a maintained product. Close #384/#385 unmerged.**

The surviving tactic is small:

`STRONG OWNER FOUND -> RUN OWNER ON OUR HARD CASES WHEN CHEAP/SAFE -> RECORD LOSS -> REUSE / INTEROPERATE / SHRINK / STOP BEFORE CUSTOM BUILD`

This may be used inside the existing WORLD / REAL USE process without a new named framework layer.

## Reopen condition

Only reopen a product-shaped BeforeBuild if a genuinely prospective case shows both:
1. the executable owner trial changes a material build decision that disciplined ordinary review would likely have missed; and
2. the owner can be tested through a reusable low-bespoke adapter/contract rather than a custom CI project.

Do not manufacture a second case to satisfy this gate.

`USEFUL METHOD != PRODUCT`
`AUTOMATION COST IS PART OF THE RESULT`
`BUILD_PROBE != PRODUCT EARNED`
`PURPOSE > INSTRUMENT`