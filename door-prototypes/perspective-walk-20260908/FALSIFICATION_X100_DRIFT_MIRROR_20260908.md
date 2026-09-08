# Please Start From Here — falsification x100 + drift / mirror audit

Status: **HOSTILE INTERNAL REVIEW / NOT CANON / NOT VALIDATION**  
Date: 8 September 2026

## Scope

This pass tests the current Door direction against its stated purpose, first-contact design, epistemic/normative boundaries, receiver/operations, and the behaviour of the project coordination process itself.

Live anchors at audit start:
- guiding purpose in `coordination/ACTIVE_THREAD_POINTER.md`: **HOW CAN WE MAKE A BETTER FUTURE?**
- public Door: Preview 0.8, `gh-pages` `2fe2c51dbe9f1cd1040bdd302cc786f30cd34cac`
- receiver PR #116: `0870bc02af3577f50545740e43333344c876e577`, still synthetic/evaluation-only
- public discussion: read-only
- no later COM #108 return observed after 18:06:04Z at the start of this audit

Classification:
- **RESISTED** — current evidence/boundaries withstand the probe.
- **NARROW GAP** — real weakness, but bounded and not currently project-invalidating.
- **MATERIAL GAP** — consequential unresolved weakness or unsupported dependency.
- **DRIFT** — the project/runtime behaviour is moving away from the stated purpose or learning discipline.

## Result

- RESISTED: **43**
- NARROW GAP: **19**
- MATERIAL GAP: **24**
- DRIFT: **14**

**Verdict: MATERIAL DRIFT, NOT PROJECT FAILURE.** The strongest surviving core is the voluntary, non-authoritative, correction-aware starting point. The weakest part is the recent operating pattern: receiver/coordination machinery has expanded faster than real-world learning.

## 100 hostile probes

| # | Domain | Probe | Result | Finding |
|---:|---|---|---|---|
| 1 | Purpose | Does current work still serve “HOW CAN WE MAKE A BETTER FUTURE?” rather than an instrument? | **DRIFT** | Door/receiver work has dominated recent effort; the purpose anchor survives in text, but operating attention has narrowed to plumbing. |
| 2 | Purpose | Would the project still be worthwhile if TRACE vanished tomorrow? | **RESISTED** | Current Door explicitly treats TRACE/ME as instruments and includes neighbours/alternatives. |
| 3 | Purpose | Would the project still be worthwhile if the custom receiver were abandoned? | **MATERIAL GAP** | Yes in principle, but recent sequencing behaves as though answer-back infrastructure is a release prerequisite; custom receiver has become too central. |
| 4 | Purpose | Is there demonstrated real-world benefit from the Door? | **MATERIAL GAP** | No. Delivery, tests and reader access exist; practical benefit to a real newcomer remains unestablished. |
| 5 | Purpose | Is there demonstrated advantage over careful ordinary reasoning or established methods? | **RESISTED** | No advantage is claimed; the public page explicitly says it has not been demonstrated. |
| 6 | Purpose | Are we learning from stronger external methods rather than defending novelty? | **RESISTED** | FPF and domain methods are named as neighbours; novelty is not used as the main justification. |
| 7 | Purpose | Has the project shifted from world/real use toward repository machinery? | **DRIFT** | Yes. The last several cycles are dominated by branch heads, D1, moderation, CSS and COM receipts rather than consequential external cases. |
| 8 | Purpose | Are positive futures/creation treated as first-class, not only harm/correction? | **NARROW GAP** | The `possibility` route exists, but the project’s emotional and explanatory centre remains harm, appeals, records and correction. |
| 9 | Purpose | Could a newcomer use the Door on something constructive without a pre-existing problem? | **NARROW GAP** | Curiosity and possibility routes allow it, but worked material and explanatory weight still bias toward failure/correction. |
| 10 | Purpose | Does the Door make external owners/methods easier to reach when they are stronger? | **NARROW GAP** | Neighbour links exist, but there is little operational routing from a concrete problem to the strongest outside owner. |
| 11 | Purpose | Are we measuring success as effect rather than publication/build completion? | **DRIFT** | We repeatedly celebrate “crossed a boundary”, test counts and deployed editions despite correctly disclaiming reader benefit. |
| 12 | Purpose | Is first contact being treated as a learning event rather than a launch? | **RESISTED** | Reddit is explicitly framed as one aperture and observations, not validation scores. |
| 13 | Purpose | Could a plain README or essay accomplish most current value with far less machinery? | **MATERIAL GAP** | Possibly. This has not been falsified; bespoke site + receiver complexity may exceed the value added over a simpler public artifact. |
| 14 | Purpose | Is accountless custom discussion necessary rather than a preference? | **MATERIAL GAP** | Not established. It solves genuine friction, but hosted alternatives/custom forms have not been comparatively tested against burden/risk. |
| 15 | Purpose | Are project costs/maintenance obligations visible in decisions? | **NARROW GAP** | Technical limits are tracked, but long-run human maintenance burden of domain, moderation, retention and incidents is underweighted. |
| 16 | Purpose | Is stopping or shrinking a legitimate outcome? | **RESISTED** | Public language and project rules explicitly preserve stopping, rejection and alternatives. |
| 17 | Purpose | Would a negative first public response be metabolised rather than defended? | **RESISTED** | Discussion design allows criticism/no-value findings; but this remains untested with strangers. |
| 18 | Purpose | Has the project preserved the difference between project purpose and TRACE survival? | **RESISTED** | Yes, explicitly in current coordination. |
| 19 | Purpose | Is the current strongest owner of the next gap actually the project? | **NARROW GAP** | For a discussion receiver yes; for many substantive world problems no. The Door risks becoming a service looking for cases. |
| 20 | Purpose | Are we close enough to real use that another infrastructure cycle is justified? | **MATERIAL GAP** | Only partly. A narrow path to real contact is near, but more speculative infrastructure beyond minimum receiving/custody should now stop. |
| 21 | First contact | Does the homepage answer “what is this?” quickly for a random human? | **NARROW GAP** | It gives purpose and routes, but remains abstract and framework-adjacent rather than concrete. |
| 22 | First contact | Does the title/meta description communicate value beyond TRACE/ME names? | **MATERIAL GAP** | No. The title/meta foreground TRACE/Mechanical Ethics, which can make a bare-link visitor see a niche framework before a useful purpose. |
| 23 | First contact | Is “How can we make a better future?” inviting rather than grandiose? | **NARROW GAP** | It is memorable, but risks sounding utopian/grandiose unless grounded immediately. |
| 24 | First contact | Is a concrete example visible early enough to ground the abstraction? | **MATERIAL GAP** | No. The first screen has abstractions/routes; a vivid small worked use is deeper. |
| 25 | First contact | Are five first movements too many choices? | **NARROW GAP** | They are coherent, but choice load has not been tested; five may be one or two too many for a bare-link arrival. |
| 26 | First contact | Does “Something is happening” tell a stranger what they can actually do? | **NARROW GAP** | It gives distinctions, but is still conceptual rather than action-shaped. |
| 27 | First contact | Does the positive “Something could be made possible” lane survive? | **RESISTED** | Yes, clearly and without requiring harm framing. |
| 28 | First contact | Can someone be curious and leave without penalty? | **RESISTED** | Yes, explicitly. |
| 29 | First contact | Can a human naturally think to hand the site to an AI? | **NARROW GAP** | Not on public 0.8; the maintained visual candidate adds the invitation, but it is not yet public. |
| 30 | First contact | Could the human-to-AI invitation imply AI authority or consciousness? | **RESISTED** | Active direction now prefers plain `AI` and explicitly says AI output is another perspective, not authority. |
| 31 | First contact | Does visual polish preserve useful content above the fold? | **MATERIAL GAP** | The larger Framework candidate failed this; Codex’s narrower line is better but still puts the first movement ~672px down at 320x800. |
| 32 | First contact | Does visual polish preserve caveats/limits rather than hiding them? | **NARROW GAP** | One candidate dropped caveats; caught and repaired. This is a live regression risk. |
| 33 | First contact | Can a root-only AI get useful content without following links? | **RESISTED** | 0.8 deliberately embeds micro-use distinctions in each movement. |
| 34 | First contact | Can a stripped-text reader discover machine alternatives? | **RESISTED** | Literal text/JSON alternatives and URLs are present. |
| 35 | First contact | Does the site work without JavaScript? | **RESISTED** | Yes; current public and design direction do not depend on JS. |
| 36 | First contact | Could the page look like AI/startup marketing and reduce trust? | **RESISTED** | Current style is restrained; design direction explicitly rejects stock AI/cyberpunk aesthetics. |
| 37 | First contact | Does “A project by Mark, developed with AI collaborators” help first contact? | **NARROW GAP** | Transparent, but it can trigger scepticism before usefulness is established; its placement/value is untested. |
| 38 | First contact | Does public “Preview 0.8” status make the Door feel unfinished? | **NARROW GAP** | Yes, possibly. Useful honesty, but versioning is developer-facing and may weaken ordinary-human confidence. |
| 39 | First contact | Are source hashes/status caveats too heavy for humans? | **NARROW GAP** | They protect provenance but contribute to technical-document feel, especially in footer/deep pages. |
| 40 | First contact | Would a Reddit visitor know what to try within 30 seconds? | **MATERIAL GAP** | Not reliably. The site offers routes, but no observed evidence shows a random human can form a concrete first action quickly. |
| 41 | Epistemic integrity | Does the project distinguish observed/reported/inferred? | **RESISTED** | Yes; this is a core and visible distinction. |
| 42 | Epistemic integrity | Does it distinguish access failure from absence? | **RESISTED** | Yes, explicitly. |
| 43 | Epistemic integrity | Does it avoid claiming authority/permission? | **RESISTED** | Yes, repeatedly. |
| 44 | Epistemic integrity | Does it avoid claiming efficacy? | **RESISTED** | Yes, public page explicitly says practical advantage is unproven. |
| 45 | Epistemic integrity | Does it treat agreement across AIs as validation? | **RESISTED** | Current project rules explicitly reject that. |
| 46 | Epistemic integrity | Does the project still risk manufacturing evidence through its own examples/tests? | **NARROW GAP** | Yes. Most evidence is project-authored synthetic tests and user-relayed encounters; independent real use is sparse. |
| 47 | Epistemic integrity | Are project-authored invitations distinguished from observed visitor demand? | **RESISTED** | Yes; Codex explicitly separated collaborative-making invitation from demonstrated demand. |
| 48 | Epistemic integrity | Are moderation outcomes distinguished from truth or target changes? | **RESISTED** | Yes: report/resolution/publication/response/change are separated. |
| 49 | Epistemic integrity | Does `content_removed` risk being read as proof removal happened? | **NARROW GAP** | Operator outcome is an assertion; Codex explicitly noted this. UI/notice must preserve that distinction. |
| 50 | Epistemic integrity | Does correction handling overclaim deletion? | **RESISTED** | No; logical unavailability vs physical erasure is explicitly preserved. |
| 51 | Epistemic integrity | Are retention defaults presented as measured/legal requirements? | **RESISTED** | No; they are explicitly described as chosen defaults. |
| 52 | Epistemic integrity | Could “making harm visible, correction reachable and power answerable” be mistaken for a deduction rather than value choice? | **RESISTED** | Public page labels it a stated value choice. |
| 53 | Epistemic integrity | Are external neighbouring methods credited? | **RESISTED** | Yes, including FPF and domain methods. |
| 54 | Epistemic integrity | Has the project established a TRACE-unique primitive or general-framework superiority? | **RESISTED** | No such claim is currently promoted; general expansion is on hold. |
| 55 | Epistemic integrity | Are we using test counts as psychological evidence of correctness beyond their scope? | **DRIFT** | Sometimes. The text states scope carefully, but our conversational cadence repeatedly foregrounds 34/34, 39/39, 40/40 as progress signals. |
| 56 | Receiver | Does a lost acknowledgement recover safely without duplication? | **RESISTED** | Yes in local/provider evaluation for the contribution lifecycle. |
| 57 | Receiver | Can changed content reuse a retry key silently? | **RESISTED** | No; conflict is explicit. |
| 58 | Receiver | Can stale approval publish a changed/withdrawn revision? | **RESISTED** | No; exact revision checks are exercised. |
| 59 | Receiver | Can pending/private text leak through public reads? | **RESISTED** | Tests cover public/private separation. |
| 60 | Receiver | Can untrusted text execute code or fetch URLs? | **RESISTED** | No; content is treated as inert text and URLs are not auto-fetched. |
| 61 | Receiver | Can an unauthenticated correction report censor content? | **RESISTED** | No; report/resolution alone does not mutate target content. |
| 62 | Receiver | Can correction capacity be starved by ordinary queue capacity? | **RESISTED** | Separate reserved correction capacity exists in the prototype. |
| 63 | Receiver | Can a reporter clear their note after resolution without erasing disposition? | **RESISTED** | Yes; provider evaluation reproduced this. |
| 64 | Receiver | Can a contributor retrieve a project answer privately? | **NARROW GAP** | Local tested receiver can; remote D1 exercise of the new query is still open. |
| 65 | Receiver | Can a wrong management key retrieve private receipt/correction data? | **RESISTED** | Negative tests exist. |
| 66 | Receiver | Does losing a management key create an unrecoverable usability failure? | **MATERIAL GAP** | Yes by design. Privacy is strong, but ordinary users may lose keys and then permanently lose control; no recovery UX has been tested. |
| 67 | Receiver | Are pre-held retry/management keys comprehensible to random humans? | **MATERIAL GAP** | Unproven and likely high-friction. This could undermine the very accountless simplicity the receiver is meant to create. |
| 68 | Receiver | Is the custom receiver simpler/safer than using an existing service? | **MATERIAL GAP** | Not established. Bespoke security, moderation, retention and recovery burdens are substantial. |
| 69 | Receiver | Are provider logs/backups/physical deletion known well enough for real intake? | **MATERIAL GAP** | No. The handling notice correctly blocks public intake on this. |
| 70 | Receiver | Does quiet-period retention actually clean up on time? | **MATERIAL GAP** | No scheduled cleanup exists; current cleanup is request-driven. |
| 71 | Receiver | Is real operator custody defined? | **MATERIAL GAP** | No. A CLI rehearsal is not an accountable operator/staffing process. |
| 72 | Receiver | Does the current 24h readiness flag prove someone is present? | **MATERIAL GAP** | No. The isolated one-hour lease is a response to this exact weakness but is unexecuted. |
| 73 | Receiver | Is one hour a justified attendance lease? | **NARROW GAP** | No; it is a conservative arbitrary evaluation default, not measured staffing capacity. |
| 74 | Receiver | Could a one-hour lease make the service unpredictably unavailable to Reddit arrivals? | **MATERIAL GAP** | Yes. Attended-only intake creates discoverability/availability mismatch unless public status and expectations are very clear. |
| 75 | Receiver | Can the correction lane remain open when no operator is available to review it? | **NARROW GAP** | Technically yes; that preserves reachability but may create an unattended sensitive queue unless custody is defined. |
| 76 | Receiver | Does class-based edge rate limiting provide meaningful abuse resistance? | **MATERIAL GAP** | Only soft burst shedding. A constant per-POP key can both throttle innocent users together and be bypassed across locations; it cannot be the hard abuse boundary. |
| 77 | Receiver | Does the current prototype have production multi-client rate semantics? | **MATERIAL GAP** | No. Local hashing and edge candidate do not yet establish robust distributed abuse control. |
| 78 | Receiver | Could public accountless intake create a moderation/spam burden far larger than expected? | **MATERIAL GAP** | Yes; this is one of the largest untested operational risks. |
| 79 | Receiver | Is there an incident/abuse/removal contact outside normal contributor credentials? | **MATERIAL GAP** | Not yet as a real operational contact. The correction mechanism exists, but operator contact/custody remains unfinished. |
| 80 | Receiver | Is the receiver ready to go live after one more test? | **RESISTED** | No; current sources explicitly keep it closed pending custody, retention, browser/accessibility and deployment checks. |
| 81 | Mirror | Have I been converting every uncertainty into another branch/file/test? | **DRIFT** | Yes. Edge admission, attended lease, visual alternatives and repeated source notes proliferated faster than real-world learning. |
| 82 | Mirror | Did I create work that collided with Codex’s concurrent work? | **DRIFT** | Yes. Two separate visual candidates were built concurrently; Codex had to identify and contain the collision. |
| 83 | Mirror | Did I move branches under active reproduction targets? | **RESISTED** | After one early lesson, later work generally isolated follow-up branches and waited for receipts. |
| 84 | Mirror | Have I kept CC from becoming a blocking gate when unavailable? | **RESISTED** | Yes. |
| 85 | Mirror | Have I overused COM as a high-frequency internal telemetry feed? | **DRIFT** | Yes. Many long comments carry exact heads and micro-deltas; useful for continuity, but the coordination surface is becoming an object of work. |
| 86 | Mirror | Does COM precision sometimes create false significance around tiny changes? | **DRIFT** | Yes. Exact hashes are useful, but they can make minor CSS/test/branch movement feel consequential. |
| 87 | Mirror | Have I mistaken “more tested” for “closer to purpose”? | **DRIFT** | At times. Receiver test depth advanced while real newcomer/use evidence did not. |
| 88 | Mirror | Have I praised progress too readily? | **DRIFT** | Yes. Phrases like “crossed a real boundary” and repeated progress framing were stronger than the external-effect evidence warranted. |
| 89 | Mirror | Have I been sufficiently willing to kill my own design? | **RESISTED** | The large visual hero was rejected after evidence; no attempt was made to defend it. |
| 90 | Mirror | Have I preserved uncertainty and negative results? | **RESISTED** | Yes: browser blocks, duplicate migration failure, WAL retention, 7403, failed candidate checks and collisions were preserved. |
| 91 | Mirror | Am I biasing toward engineering because tools make engineering easy? | **DRIFT** | Yes. Tool availability has pulled attention toward code/repo/provider work rather than human meaning, cases and use. |
| 92 | Mirror | Am I building a moderation service before proving enough people want to talk? | **DRIFT** | Yes. Answer-back is ethically attractive, but demand is not established; the receiver may be overbuilt relative to first-contact evidence. |
| 93 | Mirror | Am I making Mark carry too much operational burden through a system meant to reduce burden? | **MATERIAL GAP** | Potentially. Domain ownership, moderation, custody, deletion, incidents and Reddit follow-up could all converge on one human. |
| 94 | Mirror | Have I protected Mark from routine courier work between AIs? | **RESISTED** | Yes, increasingly. |
| 95 | Mirror | Have I kept external-contact/release authority with Mark? | **RESISTED** | Yes; no Reddit post or public intake was launched. |
| 96 | Mirror | Did I allow the Door to become the project rather than an instrument? | **DRIFT** | Temporarily, yes. The recent conversation can be summarized almost entirely as Door implementation rather than better-future inquiry. |
| 97 | Mirror | Is first contact becoming a perfection trap? | **DRIFT** | Yes. We are approaching a point where more pre-contact polish/infrastructure has diminishing returns. |
| 98 | Mirror | Would the next best move be another speculative feature branch? | **RESISTED** | No. The audit says stop speculative branches; finish the minimum live/custody path and seek bounded external use. |
| 99 | Mirror | Do we have a clear cut rule for abandoning receiver/visual complexity if users do not care? | **MATERIAL GAP** | Not explicit enough. We need kill criteria tied to real use and burden. |
| 100 | Mirror | If I remove all repository/test language, can I state the next purpose-aligned move simply? | **MATERIAL GAP** | Yes: make one honest, usable doorway; let a few strangers try it; watch what they actually do; keep what helps and delete what does not. |

## Mirror findings that change direction

1. **Receiver != prerequisite for first external learning.** A Reddit post already supplies a reply surface. Waiting for a bespoke accountless receiver before any stranger sees the Door is an overengineering/perfection trap.
2. **Stop speculative branch proliferation.** No new Door feature branch should be created unless it closes a demonstrated release blocker or a defect found by a real user/reproducer.
3. **Finish one visual line, not more design ideation.** Keep Codex's repaired maintained candidate as the integration base; complete only the outstanding light/resize/text-spacing/no-CSS checks.
4. **Treat the receiver as optional infrastructure whose value must be earned.** Finish the narrow D1 receipt-response check and custody/retention minimum, but do not keep expanding features merely because a custom service can be built.
5. **Move learning outward sooner.** Once the maintained visual candidate passes basic structural/browser checks, a small external first-contact experiment can be legitimate while on-site discussion remains read-only, provided the public status is accurate and the external thread itself is available for reply.
6. **Protect Mark's burden.** Any public receiving design needs an explicit maximum human handling burden and a kill/pause rule; the system must not turn `answerability` into an indefinite moderation obligation for one person.
7. **Add kill criteria.** If strangers do not understand the Door, do not use it on real questions, or the receiver creates more burden/risk than useful answer-back, simplify or remove the failing layer.

## Immediate cut / continue decision

**CONTINUE:** public Door, five purpose-based movements, one-fetch usefulness, human↔AI handoff as optional, visible disagreement/limits, provenance, change history, narrow receiver evaluation, affected-person correction principle.

**CUT / FREEZE:** new speculative receiver features, new visual branches, additional formal vocabulary, more benchmark-style validation loops, and COM micro-telemetry that does not change a decision.

**NEXT evidence wanted:** a few real strangers encountering the Door; what they think it is; whether they can form a useful first action; whether any independently hand it to an AI; what they reject; where they stop; and whether the resulting feedback changes the project.
