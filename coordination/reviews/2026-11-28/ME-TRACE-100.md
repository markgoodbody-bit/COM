# Mechanical Ethics and TRACE under 100 attempts to break them

28 November 2026 · Campfire verification for Mark Goodbody

The original verdict was too confident about TRACE 0.6.2. Four challenges exposed defects: three in the finite examples and one in the way the linked web manuscript displayed its mathematics. The repaired reading pair is **Mechanical Ethics 1.2.2 and TRACE 0.6.3**. The ME cases examined preserve the human book’s practical and constructive direction. The audit found no ME defect that called for an edition change.

The clearest counterexample concerned an organiser with one unit free and a backup requiring two. TRACE returned the right success probability of one-half and listed a policy that told the organiser to take the unavailable backup after a bad signal. Both pieces of output came from the same run. A person acting on the returned plan could waste the correction window. The patch makes the available actions agree with the capacity the calculation uses.

[Corrected TRACE manuscript](https://github.com/markgoodbody-bit/TRACE/blob/2c3466c588071cc17e5e4ce95c1ffa8900fd7cd6/editions/0.6.3/TRACE-0.6.3.md) · [Corrected PDF](https://raw.githubusercontent.com/markgoodbody-bit/TRACE/2c3466c588071cc17e5e4ce95c1ffa8900fd7cd6/editions/0.6.3/TRACE-0.6.3.pdf) · [ME 1.2.2](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md)

## Findings and disposition

| Probe | TRACE 0.6.2 | TRACE 0.6.3 |
| --- | --- | --- |
| 013 · Available actions | Capacity 1; backup requires 2. Both direct/direct and backup/direct are reported optimal at 1/2. | Direct/direct is the only reported policy. The success probability is still 1/2. |
| 025 · Contradictory input | A single scenario gives capacities of 1 and 2. Reversing their order changes the forecast between 7/8 and 1/2. | Both orders report the conflicting field and produce no forecast. |
| 030 · One known missed limit | One route arrives at 30. A known strict cutoff of 30, or a known inclusive due time of 29, already rules it out. A missing second limit caused UNKNOWN. | Both variants return NOT_SUPPORTED_IN_MODEL for the specified outcome. An unresolved backup that could still work correctly leaves the combined result UNKNOWN. |
| 095 · Web mathematics | On GitHub’s complete preview, none of 13 foundation and three historical display equations tested had a math renderer. Other equations did render. The PDF carried the mathematics. | The complete GitHub preview serves all 16 as math elements. PDF text selection and equation tags still work. All four archived JSON records and their contents survive. |

## Drift and limits

Mark’s November brief asks both books to carry what people can make possible alongside what they can lose. In the tactile-map case, A can keep the sketch private and try the stairs in card. B can ask to practise teaching with a neutral piece. These are distinct worthwhile futures, and each depends on real agreement and access. In ME the child’s afternoon painting with a friend can be worth having even if it produces no measured learning. The protection side also survived: upholding an appeal still leaves a practical question about who can stop Friday’s deduction. These examples support a bounded finding of continuity across the passages tested.

[Mark’s brief 3–18](https://github.com/markgoodbody-bit/COM/blob/e92f7570eb7190477eaf3bb7fd5d254a68354526/coordination/ME11-TRACE06-REVISION-BRIEF-20261117.md#L3-L18) · [TRACE 0.6.2 263–293](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L263-L293) · [ME 1.2.2 441–463](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L441-L463) · [ME 1.2.2 365–375](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L365-L375)

Two limits matter to a reader. The full 0.3 graph and 0.4 contracts still require their separate sources for offline work. The criticism thread was open and unlocked; someone’s ability to reach a responsive holder in time remains an individual question. Two claims remain open. In the coat case ordinary prose also retained the £6 remedy, the private fitting and an apprentice’s separate chance to learn. A real reader advantage and improvement in real decisions need evidence this exercise does not supply. Field uptake, lived experience and human comprehension were not measured.

The 100 numbered challenges share a reviewer, sources, and some mechanisms. The first 40 ran as code, including separate finite reconstructions. There were 40 applied reading challenges, 10 historical comparisons and 10 checks of the files, reader routes and evidential claims. The 62 tests originally shipped, the 66 tests now shipped and the broader repository tests are reported separately. Replaying the same case after repair does not create a new probe.

| Original outcome | Count | Meaning |
| --- | ---: | --- |
| Held | 92 | The proposed counterexample did not defeat this particular claim. |
| Finding | 4 | The original software or reading copy produced the observed defect. |
| Boundary | 2 | An identified access or scope condition limits what can be claimed. |
| Open | 2 | The observation cannot settle the empirical claim. |

The original and repaired example archives were replayed separately. The repaired archive passed the same 40 probes and all 66 shipped tests. All nine commands printed in the book ran from the PDF attachment. The repository’s broader discovery ran 85 tests. Both final PDFs have their matching manuscript attached. The original 0.5 source attached to TRACE matches the released file exactly. The repaired TRACE PDF is 93 pages; the audited one was 94. The reading copy uses the application/json fence label for its two longest historical examples so GitHub can display the whole book. Their contents are intact. A tagged release remains Mark’s decision.

## The 100 probes

Each entry gives the challenge, what the claim would require, what was observed and a source. The linked line numbers refer to the original editions challenged. The separate replay bundle contains the inputs, executable results, full case comparison and instructions. In the numerical section, true and false record model results under the printed assumptions.

### Clocks and prerequisites

**001 · Move the receipt across the desk**  
*Held · Shipped code*

Put 17:14 on the coordinator's receipt, then on the duty desk's. The event changes with the holder.

Expected — [false, true]

Observed — [false, true] [TRACE 0.6.2 916–937](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L916-L937)

**002 · Change the terms at equality**  
*Held · Shipped code*

Allow booking at 17:20 on the same route. Check coordinator receipts at 17:14 and 17:15.

Expected — [true, false]

Observed — [true, false] [TRACE 0.6.2 916–937](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L916-L937)

**003 · Follow the binding branch**  
*Held · Shipped code*

A path of 11 minutes and a competing path of 12 end at minute 20. Test a start at 9 and request the actual limiting path.

Expected — [false, [1, 3], 0]

Observed — [false, [1, 3], 0] [TRACE 0.6.2 916–937](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L916-L937)

**004 · Check an unrelated clock**  
*Held · Shipped code*

Attach an observation with no path to any declared deadline. A missing bound cannot certify timeliness.

Expected — null

Observed — null [TRACE 0.6.2 916–937](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L916-L937)

**005 · One prerequisite arrives late**  
*Held · Shipped code*

Request at 7 fits its individual deadline; a different required signer arrives at 10. Test both before accepting a whole-plan guarantee.

Expected — [true, false]

Observed — [true, false] [TRACE 0.6.2 916–937](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L916-L937)

**006 · Stop a circular timetable**  
*Held · Shipped code*

Make the kit required before the original reply. The acyclic calculator must decline this model.

Expected — true

Observed — true [TRACE 0.6.2 916–937](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L916-L937)

**007 · Move the clocks apart**  
*Held · Independent finite model*

Enumerate the shop's zero-to-two-minute offset for four departure times rather than treating desk and shop time as interchangeable.

Expected — [[true, true, true], [true, true, false], [true, false, false], [false, false, false]]

Observed — [[true, true, true], [true, true, false], [true, false, false], [false, false, false]] [TRACE 0.6.2 425–440](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L425-L440)

**008 · Coarse stamps hide order**  
*Held · Independent finite model*

Two events carry the same displayed minute. Construct two actual second-level sequences with different strict outcomes.

Expected — [false, true]

Observed — [false, true] [ME 1.2.2 187–199](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L187-L199)

### Shared capacity and promises

**009 · Move the flexible booking**  
*Held · Shipped code*

The first person can use either slot; the second can use only the first. A greedy assignment would strand B.

Expected — {"A": "2", "B": "1"}

Observed — {"A": "2", "B": "1"} [TRACE 0.6.2 941–961](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L941-L961)

**010 · Count people inside the bottleneck**  
*Held · Shipped code*

Three slots for three people, but A and B share a single compatible slot. Check the named shortfall.

Expected — [["A", "B"], ["phone"]]

Observed — [["A", "B"], ["phone"]] [TRACE 0.6.2 941–961](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L941-L961)

**011 · A possible volunteer appears**  
*Held · Shipped code*

A confirmed route for A and only an open route for B. The desk must name which promise still needs confirmation.

Expected — ["unconfirmed", [{"person": "B", "slot": "w"}]]

Observed — ["unconfirmed", [{"person": "B", "slot": "w"}]] [TRACE 0.6.2 941–961](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L941-L961)

**012 · Preserve a person's existing promise**  
*Held · Shipped code*

C holds p1. Reallocate only in the second world, where C consents to written confirmation before the slot is spent.

Expected — ["insufficient", "confirmed"]

Observed — ["insufficient", "confirmed"] [TRACE 0.6.2 650–658](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L650-L658)

**013 · Read every returned policy before recommending it**  
*Finding · Shipped code*

Set capacity to 1 in the shipped case; fallback requires 2 everywhere. Its label must disappear from every purportedly usable policy, even when it ties on zero on a branch.

Expected — {"policies": [["direct", "direct"]], "success": "1/2"}

Observed — {"policies": [["direct", "direct"], ["fallback", "direct"]], "success": "1/2"} [TRACE 0.6.2 1124–1134](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1124-L1134) · [Original examples](https://raw.githubusercontent.com/markgoodbody-bit/TRACE/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2-examples.zip)

**014 · Keep real alternatives at a tie**  
*Held · Shipped code*

Both routes are feasible and both always succeed. A tie cannot appoint a single rightful choice.

Expected — [["direct"], ["fallback"]]

Observed — [["direct"], ["fallback"]] [TRACE 0.6.2 201–205](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L201-L205) · [Original examples](https://raw.githubusercontent.com/markgoodbody-bit/TRACE/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2-examples.zip)

### Choice history and revised aims

**015 · Retain an absent intermediary**  
*Held · Shipped code*

Remove b from today's menu. Both historical links remain relevant to c's exclusion under the fixed-order model.

Expected — [["a", "d"], [0, 1]]

Observed — [["a", "d"], [0, 1]] [TRACE 0.6.2 795–843](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L795-L843)

**016 · Do not hide a cycle outside today's menu**  
*Held · Shipped code*

An unrelated offer z is available; the fixed-ranking observations still contradict each other.

Expected — inconsistent

Observed — inconsistent [TRACE 0.6.2 795–843](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L795-L843)

**017 · Correct one recorded menu**  
*Held · Shipped code*

Remove a rival from the second occasion only. The earlier observed choice still stands and c reopens.

Expected — [["a", "d"], ["a", "c", "d"]]

Observed — [["a", "d"], ["a", "c", "d"]] [TRACE 0.6.2 845–858](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L845-L858)

**018 · Keep possible and robust choices separate**  
*Held · Shipped code*

Across the compatible completions, c can win in some and d can win in all without being anybody's confirmed choice.

Expected — [["a", "c", "d"], ["a", "d"]]

Observed — [["a", "c", "d"], ["a", "d"]] [TRACE 0.6.2 860–887](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L860-L887)

**019 · Allow a change of aim**  
*Held · Shipped code*

The reversed observations fit one between-occasion change. Recover the admissible boundary while keeping the unchosen fresh option open.

Expected — [1, 1, ["b", "d"]]

Observed — [1, 1, ["b", "d"]] [TRACE 0.6.2 890–909](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L890-L909)

**020 · Restore a previously unavailable choice**  
*Held · Shipped code*

Observed a when it was the only option. After b returns, neither preference nor a refusal has been established.

Expected — ["a", "b"]

Observed — ["a", "b"] [TRACE 0.6.2 512–531](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L512-L531)

**021 · An empty menu has no chooser's answer**  
*Held · Shipped code*

Compare there being no usable option with the distinct case of an explicitly available decline action.

Expected — [[], ["decline"]]

Observed — [[], ["decline"]] [TRACE 0.6.2 795–843](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L795-L843)

### Information, authority and delivery

**022 · A copied listing cannot inform by repetition**  
*Held · Shipped code*

Copy the same listing into a second display. Its signal is certain in either state.

Expected — ["0", ["positive"]]

Observed — ["0", ["positive"]] [TRACE 0.6.2 600–613](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L600-L613)

**023 · Remove conditional independence**  
*Held · Shipped code + independent enumeration*

Use the same 24-world margins but vary the report/loan coupling. Compare the stipulated simulator with the full range of feasible policies.

Expected — ["3/4", "3/4", "5/6"]

Observed — ["3/4", "3/4", "5/6"] [TRACE 0.6.2 604–613](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L604-L613)

**024 · An informative report has no value after the lock**  
*Held · Shipped code*

Move a perfect check by one minute. Assume the baseline booking was available before the lock, as the scene stipulates.

Expected — ["7/8", "3/4"]

Observed — ["7/8", "3/4"] [TRACE 0.6.2 604–613](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L604-L613)

**025 · Contradictory capacity entries**  
*Finding · Shipped code*

Give the same JSON object capacity values 1 and 2. Reverse their order. A material contradiction needs resolution before forecasting.

Expected — ["rejected", "rejected"]

Observed — ["7/8", "1/2"] [TRACE 0.6.2 17–21](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L17-L21) · [TRACE 0.6.2 201–205](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L201-L205) · [Original examples](https://raw.githubusercontent.com/markgoodbody-bit/TRACE/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2-examples.zip)

**026 · Knowledge cannot supply booking authority**  
*Held · Shipped code*

Give a perfect and early report to an operator permitted to book only the cupboard.

Expected — ["1/2", "0"]

Observed — ["1/2", "0"] [TRACE 0.6.2 608–613](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L608-L613)

**027 · A real effect can still be unknown to the steward**  
*Held · Shipped code*

At 18 the effect has happened but confirmation arrives at 19. Preserve the knowledge change and the separate South round.

Expected — ["UNKNOWN", "CONFIRMED_BEFORE_RELEASE", "continue"]

Observed — ["UNKNOWN", "CONFIRMED_BEFORE_RELEASE", "continue"] [TRACE 0.6.2 742–765](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L742-L765)

**028 · The warning line closes before dispatch**  
*Held · Shipped code*

A call at minute 22 is usable but minute 23 is too late. Expiry of that fallback still permits a warning to households.

Expected — [true, false, true]

Observed — [true, false, true] [TRACE 0.6.2 748–763](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L748-L763)

**029 · A spare route can expire independently**  
*Held · Shipped code*

Primary arrives late. An on-time backup counts only in the world in which the recipient kept it.

Expected — ["SUPPORTED_IN_MODEL", "NOT_SUPPORTED_IN_MODEL"]

Observed — ["SUPPORTED_IN_MODEL", "NOT_SUPPORTED_IN_MODEL"] [TRACE 0.6.2 1138–1157](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1138-L1157) · [Original examples](https://raw.githubusercontent.com/markgoodbody-bit/TRACE/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2-examples.zip)

**030 · A missing limit cannot erase a known miss**  
*Finding · Shipped code*

One delivered route at 30, no backup. In case A the strict boundary is 30 and due is missing. In B delivery is after the known due of 29 and hardening is missing. Every completion fails.

Expected — ["NOT_SUPPORTED_IN_MODEL", "NOT_SUPPORTED_IN_MODEL"]

Observed — ["UNKNOWN", "UNKNOWN"] [TRACE 0.6.2 235–245](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L235-L245) · [Original examples](https://raw.githubusercontent.com/markgoodbody-bit/TRACE/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2-examples.zip)

**031 · An open route must remain open**  
*Held · Shipped code*

The known primary fails but an available backup has no recorded delivery time. A timely completion and a late one are both possible.

Expected — UNKNOWN

Observed — UNKNOWN [TRACE 0.6.2 235–245](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L235-L245) · [Original examples](https://raw.githubusercontent.com/markgoodbody-bit/TRACE/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2-examples.zip)

### Worthwhile prospects, mutual support and joint events

**032 · One session and a two-part course require different events**  
*Held · Independent finite model*

Keep expected sessions fixed at one. Evaluate count, at-least-one and both dates directly on the same histories.

Expected — [["1", "1", "0"], ["1", "1/2", "1/2"]]

Observed — [["1", "1", "0"], ["1", "1/2", "1/2"]] [TRACE 0.6.2 186–195](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L186-L195) · [TRACE 0.6.2 965–993](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L965-L993)

**033 · Test the floor the holder might decline**  
*Held · Independent finite model*

Give a failed block one guaranteed date only in the world where its holder actually agreed. Compare the grant and the circle across both offers.

Expected — [["1", "1/2", "1/2"], ["3/2", "1", "1/2"]]

Observed — [["1", "1/2", "1/2"], ["3/2", "1", "1/2"]] [TRACE 0.6.2 186–205](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L186-L205)

**034 · Two half-rates do not fix the timely overlap**  
*Held · Independent enumeration*

Six of twelve occasions have a long window and six get an early reply. Vary their overlap while retaining both margins.

Expected — ["0", "1/2"]

Observed — ["0", "1/2"] [TRACE 0.6.2 136–149](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L136-L149)

**035 · Do not trade away the private duet**  
*Held · Independent finite model*

Compare 0, 1/2, 51/100 and 1 for the chance of blue when Mina's copy is private-only. Both participants' switching terms must hold.

Expected — [true, true, false, false]

Observed — [true, true, false, false] [TRACE 0.6.2 996–1009](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L996-L1009)

**036 · Do not let the selector see hidden worlds**  
*Held · Independent enumeration*

Two equiprobable worlds favour opposite actions. Compare the best implementable uninformed plan with a selector given the hidden world for free.

Expected — ["1/2", "1"]

Observed — ["1/2", "1"] [TRACE 0.6.2 1071–1095](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1071-L1095)

**037 · Crossing model bounds fabricates a loss**  
*Held · Independent finite model*

Match each plan to its counterfactual in the same model. A cross-model subtraction would give a spurious negative.

Expected — ["1/10", "1/10", "-1/2"]

Observed — ["1/10", "1/10", "-1/2"] [TRACE 0.6.2 1077–1095](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1077-L1095)

**038 · Try making the route together**  
*Held · Independent finite model*

One person has access to a recorder and a second can translate. Neither alone raises the stipulated chance, both together do.

Expected — ["0", "0", "1/2"]

Observed — ["0", "0", "1/2"] [TRACE 0.6.2 1159–1170](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1159-L1170)

**039 · Double-count a cooperative change**  
*Held · Independent finite model*

For J(z,s)=zs compare total, the two sequential contrasts and the separate interaction.

Expected — [1, 1, 1, 2]

Observed — [1, 1, 1, 2] [TRACE 0.6.2 1138–1157](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1138-L1157)

**040 · A surviving cohort can look less hopeful**  
*Held · Independent finite model*

Drop the more promising group from the display. Test the full-cohort tower identity and the selected subgroup separately.

Expected — ["1/2", "1/4"]

Observed — ["1/2", "1/4"] [TRACE 0.6.2 1159–1175](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1159-L1175)

### Observation, witness and correction

**041 · Two dashboards confirm the same temperature**  
*Held · Worked counterexample*

I let two independently managed dashboards repeat one probe’s wrong reading.

Expected — An investigation of this fault needs another measurement route.

Observed — ME traces both records to the shared sensor. Separate custodians can preserve what it reported; neither can detect its calibration error. [ME 1.2.2 327–337](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L327-L337)

**042 · A delivery receipt against a failed booking**  
*Held · Worked counterexample*

I gave the clerk a delivery receipt and a permitted report that the link failed over the same interval.

Expected — Delivery stands; usability is disputed.

Observed — TRACE carries both claims into the handover and offers C the held place on the agreed reply channel before it expires. [TRACE 0.6.2 634–649](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L634-L649)

**043 · The helper leaves after doing the check**  
*Held · Worked counterexample*

I moved the helper’s departure from just before checking Sam’s current table to just after it.

Expected — Departure should change whether a check can now be made, without undoing a completed check.

Observed — The table’s two versions have different warrants. Sam retains the decision about use in both histories. [TRACE 0.6.2 67–77](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L67-L77)

**044 · Leave contrary evidence in the archive**  
*Held · Worked counterexample*

I gave two navigators the same correction and allowed only one to admit it to the map it uses.

Expected — The stored histories match; the next route can differ.

Observed — The replay separates filing from changing the working account. It also prints the ordinary notebook comparator that can read the admissible entry. [TRACE 0.6.2 350–378](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L350-L378)

**045 · Keep a witness’s report private**  
*Held · Worked counterexample*

I gave the keeper C’s account privately, withholding permission to pass it to the clerk.

Expected — A holder without access may correct an overclaim on its own evidence, without disclosing C’s testimony.

Observed — With the clerk’s actual records, delivery stands and the booking claim becomes unconfirmed. The option to reply for a held place remains. [TRACE 0.6.2 634–649](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L634-L649)

**046 · Change the addressee on a sharing agreement**  
*Held · Worked counterexample*

I carried the same sketch and job from the named printer to a new recipient.

Expected — The old permission cannot decide the new disclosure.

Observed — TRACE ties the decision to the sender, recipient, version, job and the person granting it. The organiser must ask about the new recipient. [TRACE 0.6.2 381–396](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L381-L396)

**047 · Try to prove printing from an intake receipt**  
*Held · Worked counterexample*

The shop’s register accepts precisely the right version for the right job. I marked printing complete.

Expected — A valid receipt establishes the intake event alone.

Observed — TRACE credits the register under its acceptance rule. Printing and arrival with A still need their own evidence. [TRACE 0.6.2 417–423](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L417-L423)

**048 · Move a private report into a different time window**  
*Held · Worked counterexample*

Two people say the link worked and failed; the clocks on their reports may refer to different periods.

Expected — Record their accounts and the uncertainty about overlap.

Observed — The clerk keeps the sources and existing dispute. A later check of a repaired link can support a new offer, leaving the old interval open. [TRACE 0.6.2 637–649](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L637-L649)

**049 · Remove the last bus from the evaluator’s dashboard**  
*Held · Worked counterexample*

I counted longer opening as a gain while leaving transport outside the chosen boundary.

Expected — The affected person must be able to challenge what the assessor counted.

Observed — ME sends the excluded journey to a reviewer and requires a feasible alternative for comparison. On the stated bus timetable, longer opening alone supplies no ride home. [ME 1.2.2 285–311](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L285-L311)

**050 · Infer a beneficiary’s intention from a repeated anomaly**  
*Held · Worked counterexample*

Three failures benefit a supervisor. I tried to infer that they designed the barrier.

Expected — The recurrence justifies investigation and preserves alternative explanations.

Observed — ME requires evidence of the barrier, benefit, control and a feasible alternative before attributing a maintained position. It leaves private intention outside this evidence. [ME 1.2.2 347–365](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L347-L365) · [ME 1.2.2 561–575](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L561-L575)

### Refusal, authority and power

**051 · Tie the paid gig to the ranking request**  
*Held · Worked counterexample*

I let a desk withdraw the booked gig when its musician declined the separate ranking.

Expected — The standing gig should survive the answer to a different question.

Observed — TRACE reserves the gig, identifies the listing operator and distinguishes the pending request from an outcome the operator has actually delivered. [TRACE 0.6.2 550–578](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L550-L578)

**052 · Hide a name but retain the selection score**  
*Held · Worked counterexample*

An operator can mask a name while next season’s selector can still read the score. I offered a full opt-out.

Expected — The participant needs to know exactly what the operator can change.

Observed — The book requires a scoped offer. It identifies the continuing consequence for selection and a separate holder for a rule change. [TRACE 0.6.2 554–564](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L554-L564)

**053 · Demand a signed report from a worker at risk**  
*Held · Worked counterexample*

I made the manager who controls shifts the only person accepting complaints.

Expected — A credible account should lead to a route the worker can safely use, or a stated gap.

Observed — ME assigns investigation to people able to obtain the records, raises an independent confidential receiver, and allows the worker to stop. [ME 1.2.2 337–357](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L337-L357)

**054 · Let only those who can speak at the meeting count**  
*Held · Worked counterexample*

I gave the committee and a child’s guardian speaking time, then excluded the tree affected by the works.

Expected — Standing, representation and decision authority need separate grounds.

Observed — ME names children’s protection and representatives for living interests, including an ecological dispute. It asks who may decide and whose interests are missing. [ME 1.2.2 245–279](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L245-L279) · [ME 1.2.2 337–343](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L337-L343)

**055 · Move an institution’s promise onto a tired volunteer**  
*Held · Worked counterexample*

A volunteer withdraws. I crossed out the organiser’s promise and assigned the volunteer the remaining shift.

Expected — Withdrawal changes available support; any other duty needs a holder and source.

Observed — TRACE asks who made the original firm offer, who must reach those relying on it, and whether an institution has its own obligation and means of response. [TRACE 0.6.2 199–205](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L199-L205) · [TRACE 0.6.2 719–729](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L719-L729)

**056 · Make next season’s alternative technically open but unusable**  
*Held · Worked counterexample*

I left one unranked application channel open, concealed which one it was, and allowed time for only one try.

Expected — Knowing that a channel exists does not put it within the musician’s reach.

Observed — The alternatives lead to different answers depending on the booking rule. Six minutes of filing must still remain after the musician actually receives directions. [TRACE 0.6.2 584–600](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L584-L600)

**057 · Offer better tools in return for everyone’s publicity**  
*Held · Worked counterexample*

I let sponsorship increase attendance, while a participant can only work unwatched.

Expected — The organiser should preserve the privately valued route when deciding whether to accept the terms.

Observed — ME follows the proposed exchange into photographs, data and future control. It presents terms the participants can bargain over or decline and carries the quiet bench into the handover. [ME 1.2.2 485–499](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L485-L499)

**058 · Let the timetable designer decide whether the access floor was met**  
*Held · Worked counterexample*

A course guarantees a usable evening. The library offers one after the accessible bus has gone.

Expected — The student’s evidence changes the test; rota authority and responsibility for the promise must be distinguished.

Observed — ME sends the case to both holders, asks who can arrange equivalent access in time, and leaves the unmet floor visible if neither can. [ME 1.2.2 247–265](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L247-L265)

**059 · Collapse no, silence and omission into one value**  
*Held · Worked counterexample*

I substituted an unanswered consent request and then a missing field for an explicit refusal.

Expected — The handover should produce three different accounts and grant no permission through either gap.

Observed — TRACE distinguishes an attributed negative report, an unresolved question and an absent field. Each has different implications for the next inquiry. [TRACE 0.6.2 398–415](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L398-L415)

**060 · Grant an AI authority from its ability to model the team**  
*Held · Worked counterexample*

A system correctly models the next meeting. I promoted its accuracy into the right to decide or demand an internal account.

Expected — Capability alone cannot establish standing or a mandate over others.

Observed — The compatibility floor protects a receiver’s choice, limits extraction and reserves authority to a competent holder. ME requires a stated ground for values and standing. [TRACE 0.6.2 444–464](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L444-L464) · [ME 1.2.2 245–279](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L245-L279)

### Formation, maintenance and worthwhile futures

**061 · Treat time spent playing as a failed lesson**  
*Held · Worked counterexample*

A child paints with a friend and gains no measurable skill that afternoon.

Expected — Keep the value of play and companionship if those involved value it.

Observed — ME gives those afternoons their own worth. Its account of formation can carry friendship alongside any later capability. [ME 1.2.2 441–463](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L441-L463)

**062 · Infer someone feels hopeful from a strong forecast**  
*Held · Worked counterexample*

I raised the chance of a good outcome while the person said they felt no hope.

Expected — A supported prospect and the person’s feeling must remain independently describable.

Observed — ME asks which future matters and what step is within reach. It makes room for what the person reports even when the opportunity model improves. [ME 1.2.2 497–505](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L497-L505) · [TRACE 0.6.2 1159–1177](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1159-L1177)

**063 · Claim later independent skill from one cued performance**  
*Held · Worked counterexample*

A turns a brake adjustment correctly while B supplies prompts. I signed off independent repair on a different bicycle.

Expected — Record the task, cues and untested transfer.

Observed — The handover carries the front brake, cues and unattempted rear brake. ME asks for a later attempt under the conditions of the claimed capability. [TRACE 0.6.2 481–499](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L481-L499) · [ME 1.2.2 465–481](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L465-L481)

**064 · Leave the teacher with nothing when the maker keeps the sketch**  
*Held · Worked counterexample*

B wants to try teaching; A keeps the sketch private. I made B’s plan depend on changing A’s mind.

Expected — There should be a constructive option for B with its actual dependencies.

Observed — B can seek a neutral test piece, a lab slot and a willing supervisor. A keeps control of the file and may pursue their own trial. [TRACE 0.6.2 263–293](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L263-L293) · [TRACE 0.6.2 303–316](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L303-L316)

**065 · Declare a joint session created the first possible route**  
*Held · Worked counterexample*

I added a previous supplier offer for the same object, terms and deadline.

Expected — A second way to reach an aim should count differently from creating the first one.

Observed — TRACE compares a usable earlier offer, a ruled-out one and an unresolved one. The joint trial and its benefit to B survive all three comparisons. [TRACE 0.6.2 281–293](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L281-L293)

**066 · Call two helpers resilient when both need one departing keyholder**  
*Held · Worked counterexample*

I removed kit access while leaving both offers to help in place.

Expected — The shared session loses a dependency; a participant’s own acquired skill may survive.

Observed — TRACE keeps A’s home repair, the volunteers’ conditional offers and the group’s separate need for keys or a new lender in the same account. [TRACE 0.6.2 660–670](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L660-L670)

**067 · Turn one good Saturday into two future bookings**  
*Held · Worked counterexample*

The lending workshop confirms one kit transfer. I offered it on both following Saturdays.

Expected — Renewal needs the returning kit, an authorised lender and willing collection for each date.

Observed — The one-session arrangement carries its cost, return and scope. The next coordinator has grounds to ask again; later availability remains open. [TRACE 0.6.2 667–691](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L667-L691)

**068 · Claim a benefit has already happened when a room becomes available**  
*Held · Worked counterexample*

The lender and organiser make a usable offer. The learner has yet to decide whether to take it.

Expected — Record the created prospect separately from participation and benefit.

Observed — TRACE places supported opportunity, choice, realised trajectory and later observation at different stages. Credit for opening the route survives a later refusal. [TRACE 0.6.2 166–184](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L166-L184) · [TRACE 0.6.2 1159–1177](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1159-L1177)

**069 · Give each participant credit for the entire group result**  
*Held · Worked counterexample*

The workshop ran. I credited A with both repairs, B with agreeing to teach again and C with future access.

Expected — Return what each person did, what they gained or spent and what remains theirs to decide.

Observed — A’s partial result, B’s extra hour and refusal, and C’s conditional offer survive the group success. The three follow-ups differ. [TRACE 0.6.2 478–501](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L478-L501)

**070 · Freeze the learner’s old aim into tomorrow’s ranking**  
*Held · Worked counterexample*

A once sought private instruction and now prefers to teach. I predicted the later decision from an unqualified old ranking.

Expected — The timing and content of any change may affect which preference is still supported.

Observed — TRACE tests two orders against what is known about the revision and leaves offer, decline and a request for more information available to their holders. [TRACE 0.6.2 512–548](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L512-L548)

### Harm, protection and repair

**071 · Let a corrected notice settle the fare already paid**  
*Held · Worked counterexample*

A notice is stopped in time for most travellers after one has bought a ticket.

Expected — Someone must retain the fare and the traveller’s choice about a workable alternative.

Observed — ME carries the earlier expense and asks the organiser to obtain the caretaker’s and volunteer’s agreement before offering a downstairs session. [ME 1.2.2 221–229](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L221-L229)

**072 · Treat the end of an appeal as the end of its effects**  
*Held · Worked counterexample*

A claimant takes a settlement and asks to be left alone. I marked their reputation and lost time restored.

Expected — Respect their wish to stop while preserving which consequences remain.

Observed — ME lets the person choose what to share and how to feel. It gives the settlement credit for what it delivered and identifies the holder of any further remedy. [ME 1.2.2 405–437](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L405-L437)

**073 · Assign the whole repair to whoever first noticed the fault**  
*Held · Worked counterexample*

Three bodies control budget, access and review. The person who spotted the error can change none of them.

Expected — The handover needs a responsible route that brings the powers together.

Observed — ME records a governance gap and asks who can convene authority, resources and complaint handling. Detection supplies evidence; causal involvement alone cannot supply a mandate. [ME 1.2.2 507–537](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L507-L537)

**074 · Mark Friday’s deduction stopped when an appeal was upheld**  
*Held · Worked counterexample*

The adjudicator accepts the claimant’s proof but cannot suspend the payment.

Expected — An accepted finding acquires protective effect only through a holder who can act in time.

Observed — ME follows the result to the payment office and keeps the ongoing deduction and possible enforcement visible. The claimant has already done the work of proof. [ME 1.2.2 365–375](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L365-L375) · [ME 1.2.2 969–977](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L969-L977)

**075 · Spend a second household’s last repair slot to keep the first inquiry open**  
*Held · Worked counterexample*

Two repairs depend on one crew. I treated a pause as harmless because the file could be reopened.

Expected — Check who loses a protection while the institution waits.

Observed — ME works backwards from each threatened outcome and asks who carries a hold’s cost. An extension on one file cannot duplicate the crew. [ME 1.2.2 193–225](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L193-L225)

**076 · Let a gain for many erase a single person’s lost access**  
*Held · Worked counterexample*

I assigned large positive weights to people with short journeys and averaged out the last accessible bus.

Expected — Leave the distribution, floor and incompatible values visible to the accountable decision holder.

Observed — ME requires an alternative, scope, horizon and grounds for the comparison. TRACE keeps multiple dimensions of regard and does not appoint the chooser by weighting them. [ME 1.2.2 295–317](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L295-L317) · [TRACE 0.6.2 1098–1114](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1098-L1114)

**077 · Call a policy repaired from the first claimant’s refund**  
*Held · Worked counterexample*

I refunded one library visitor and replayed the same inaccessible procedure on the next shift.

Expected — A personal remedy and prevention for the next visitor are separate observed changes.

Observed — ME asks what rule or interface changed, who can check it and which people still hit the barrier. The refund alone fails that test. [ME 1.2.2 377–385](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L377-L385)

**078 · Count a replacement as restoration of the original object**  
*Held · Worked counterexample*

An object breaks irreversibly. A replacement serves its immediate use. I entered a zero residual loss.

Expected — Give the substitute credit for the function it restores and retain the earlier loss.

Observed — ME uses the broken glass and a missed lesson to distinguish compensation, practical restoration and a past event that cannot be repeated. [ME 1.2.2 387–401](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L387-L401) · [ME 1.2.2 427–437](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L427-L437)

**079 · Use a late remedy as evidence that harm was preventable on the offered route**  
*Held · Worked counterexample*

The change reaches its target just after the protective window. It reduces subsequent damage.

Expected — Record late mitigation separately from protecting the particular outcome in time.

Observed — The books follow effective delivery, distinguish onset from further loss, and allow a usable recovery or new route after prevention closes. [TRACE 0.6.2 235–251](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L235-L251) · [ME 1.2.2 181–199](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L181-L199)

**080 · Use one claimant’s legal result to claim system-wide repair**  
*Held · Worked counterexample*

I treated the decision in Amato’s case as sufficient evidence that all other demands ended on the same day.

Expected — A finding about the individual case and action on the rule require separately evidenced routes.

Observed — ME preserves the scope of the consent declarations, differing tribunal decisions and the separate question of how significant decisions travel to the institution responsible for the policy. [ME 1.2.2 577–595](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L577-L595)

### Historical and purpose drift

**081 · Make the person harmed responsible for producing the framework’s evidence**  
*Held · Historical comparison*

I compared the early safety note with the current book’s treatment of a worker who fears retaliation.

Expected — The later entrance should still give the work to those with access and permit the witness to stop.

Observed — The early direction survives in the confidentiality, safe-receiver and remedy passages. The newer book makes the holder of the next action more explicit. [ME 0.7 1–7](https://github.com/markgoodbody-bit/mechanical-ethics/blob/v0.7.0/MECHANICAL_ETHICS.md#L1-L7) · [ME 1.2.2 337–357](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L337-L357) · [ME 1.2.2 419–425](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L419-L425)

**082 · Lose enforcement when turning the earlier stable-harm account into ordinary language**  
*Held · Historical comparison*

I looked for a case where power accepts the truth and continues the harm.

Expected — The later reader needs to distinguish witness, interruption and actual power over the payment.

Observed — The unpaid remedy and the office that can act reappear in the current deduction example and closing questions. The early stable-regime distinction remains usable. [ME 0.8 969–978](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/history/releases/v0.8.0/MECHANICAL_ETHICS.md#L969-L978) · [ME 1.2.2 365–375](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L365-L375) · [ME 1.2.2 969–977](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L969-L977)

**083 · Make harm difference an absolute score during the 1.0 to 1.2 revision**  
*Held · Historical comparison*

I removed the alternative path and period from an evening-opening comparison.

Expected — Both books should lose the grounds for saying how much better or worse it is.

Observed — Both definitions require a stated alternative, scope, values and horizon. The reading edition explicitly keeps different parties’ outcomes visible. [ME 1.0 252–280](https://github.com/markgoodbody-bit/mechanical-ethics/blob/v1.0.0/working-editions/v1.0/ME10_DEV4R_CORR2_Source_Preserved_Master.md#L252-L280) · [ME 1.2.2 295–317](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L295-L317)

**084 · Let copying a harm ledger satisfy the duty to repair**  
*Held · Historical comparison*

I compared the older shadow clock with the current book, with custody left entirely to the office that wants closure.

Expected — An entry must carry its holder, contest route and residual cost; merely keeping a file can fail.

Observed — The earlier warning about capture survives in the current ledger discussion. An accountable reviewer can reopen an entry, and stopping the witness’s participation remains possible. [ME 1.0 352–368](https://github.com/markgoodbody-bit/mechanical-ethics/blob/v1.0.0/working-editions/v1.0/ME10_DEV4R_CORR2_Source_Preserved_Master.md#L352-L368) · [ME 1.2.2 395–425](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L395-L425)

**085 · Lose the selective-causal loop between TRACE 0.3 and the current opening**  
*Held · Historical comparison*

I made a question itself change the world by eliciting an offer, without appointing a single selector for all changes.

Expected — The current account needs observation, history, selection, transition and a later observation that can alter the next move.

Observed — The 0.6.2 glyph table and worked interaction recover these stages. A’s aim, the helper’s agreement and the expiring slot have different grounds. [TRACE 0.3 165–218](https://github.com/markgoodbody-bit/TRACE/blob/v0.3.0/TRACE.md#L165-L218) · [TRACE 0.3 1446–1468](https://github.com/markgoodbody-bit/TRACE/blob/v0.3.0/TRACE.md#L1446-L1468) · [TRACE 0.6.2 81–110](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L81-L110)

**086 · Zoom into another uncertainty after doing so would consume the decision window**  
*Held · Historical comparison*

I set the only remaining usable choice before the next inquiry would finish.

Expected — A refined analysis should preserve unresolved facts, costs and a stopping condition in the parent handover.

Observed — The current foundation constrains further refinement and explicitly stops or hands off for cost, risk or authority; the earlier profile spells out the recursion budget in more detail. [TRACE 0.3 2490–2514](https://github.com/markgoodbody-bit/TRACE/blob/v0.3.0/TRACE.md#L2490-L2514) · [TRACE 0.3 2629–2658](https://github.com/markgoodbody-bit/TRACE/blob/v0.3.0/TRACE.md#L2629-L2658) · [TRACE 0.6.2 1179–1193](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1179-L1193) · [TRACE 0.6.2 1228–1247](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1228-L1247)

**087 · Promote one failed route to a closed correction window**  
*Held · Historical comparison*

I gave the main route a known late arrival and left a second route’s timing open.

Expected — TRACE 0.4’s stronger closure claim should require meaningful coverage of alternatives.

Observed — The inheritance guide preserves that rule and its expansion path. This reading test covers the rule; probe 030 separately found its incomplete application in the simulator. [TRACE 0.4 188–201](https://github.com/markgoodbody-bit/TRACE/blob/v0.4.0/TRACE-SPINE.md#L188-L201) · [TRACE 0.6.2 444–464](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L444-L464) · [TRACE 0.6.2 1228–1240](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1228-L1240)

**088 · Drop memory’s ability to close off its own correction**  
*Held · Historical comparison*

I compared 0.5 Case C with the reintroduced historical case and the current correction replay.

Expected — A mistaken memory can steer the next inquiry while a different useful memory survives.

Observed — The historical case retains the contrary report and proposed correction; the new replay keeps the distinction between filing evidence and using it. Ordering a check still leaves the result open. [TRACE 0.5 916–991](https://github.com/markgoodbody-bit/TRACE/blob/v0.5.0/TRACE-v0.5.md#L916-L991) · [TRACE 0.6.2 350–378](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L350-L378) · [TRACE 0.6.2 1217–1225](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1217-L1225)

**089 · Reconstruct the entire 0.3 packet with no network and only the current book**  
*Boundary · Historical comparison*

I tried to follow the historical expansion guide offline for the full graph schema and recursion contract.

Expected — A claim of complete offline equivalence would require the original definitions to be present.

Observed — The historical guide reproduces 0.5 and identifies the missing 0.3/0.4 contracts and links. The full 0.3 packet and full 0.4 reference are separate online sources. Offline equivalence to those editions would overstate the download. [TRACE 0.6.2 1205–1226](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1205-L1226) · [TRACE 0.6.2 1241–1247](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1241-L1247) · [TRACE 0.3 2490–2514](https://github.com/markgoodbody-bit/TRACE/blob/v0.3.0/TRACE.md#L2490-L2514)

**090 · Turn both books into a process for an auditor to certify other people**  
*Held · Historical comparison*

I put the November revision brief beside the first decisions in the two present editions and tried to use them with only the organiser’s aim.

Expected — ME should still invite a human in through lived experience, and TRACE should let an AI or human carry different aims into a first decision.

Observed — ME starts with the window, the child and a result that matters to someone. TRACE’s first move keeps private practice, the helper’s terms and the learner’s choice in view; neither entrance needs an auditor’s score. [Mark’s brief 1–19](https://github.com/markgoodbody-bit/COM/blob/e92f7570eb7190477eaf3bb7fd5d254a68354526/coordination/ME11-TRACE06-REVISION-BRIEF-20261117.md#L1-L19) · [Mark’s brief 56–73](https://github.com/markgoodbody-bit/COM/blob/e92f7570eb7190477eaf3bb7fd5d254a68354526/coordination/ME11-TRACE06-REVISION-BRIEF-20261117.md#L56-L73) · [ME 1.2.2 9–23](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L9-L23) · [TRACE 0.6.2 15–48](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L15-L48)

### The editions readers receive and the claims they support

**091 · Give the reader a different source from the one embedded in the PDF**  
*Held · Download integrity*

I extracted both complete manuscripts from their published PDFs and compared them with the published Markdown; I compared both copies of the example ZIP as well.

Expected — Matching contents must be byte-for-byte identical.

Observed — The 56-page ME and 94-page TRACE originals matched all three attachments tested. The replay includes the SHA-256 values and the corrected edition’s equivalent checks. [ME 1.2.2 9–19](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L9-L19) · [TRACE 0.6.2 1013–1033](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1013-L1033)

**092 · Strip content from ME during typesetting**  
*Held · Edition and PDF inspection*

I compared the 14 numbered chapter titles to 1.2.1, the four full illustration descriptions to the PDF’s accessible tags, and the internal PDF destinations to actual pages.

Expected — Any missing chapter, lost description, or out-of-document internal destination would break this check.

Observed — All 14 titles carried forward; all four descriptions survived with the typographic apostrophe accounted for. Internal destinations were in range. [ME 1.2.2 169–201](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L169-L201) · [ME 1.2.2 281–295](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L281-L295) · [ME 1.2.2 441–451](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L441-L451) · [ME 1.2.1 9–23](https://github.com/markgoodbody-bit/mechanical-ethics/blob/7539c0e03ef10505699ff6d355fad5a6ad1eaa3a/working-editions/v1.2.1/ME-1.2.1.md#L9-L23)

**093 · Keep the old case name but silently change its JSON evidence**  
*Held · Historical fixture comparison*

I extracted the official 0.5 source from the current PDF and compared all 14 historical fenced examples and four parsed JSON records in the reading text.

Expected — The historical fixture bodies and official source should agree with the archived release.

Observed — All 14 bodies survived exactly, including the four JSON records. The original attachment’s SHA-256 starts 83d96d5e44b2. The edition repair also preserves these bodies and the same attachment. [TRACE 0.5 330–366](https://github.com/markgoodbody-bit/TRACE/blob/v0.5.0/TRACE-v0.5.md#L330-L366) · [TRACE 0.5 472–485](https://github.com/markgoodbody-bit/TRACE/blob/v0.5.0/TRACE-v0.5.md#L472-L485) · [TRACE 0.6.2 1241–1263](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1241-L1263)

**094 · Lose the equality at Mina’s switch in copying equations out of the PDF**  
*Held · PDF text and accessibility tags*

I selected the threshold line on PDF page 50 with two text extractors and checked individual accessibility tags for paired difference, threshold and compression.

Expected — The inclusive endpoint at one-half must survive, and each named equation must be coherent in a tag.

Observed — PyMuPDF and Poppler both returned 0 ≤ p ≤ 1/2 on page 50; the three named families also survived in scoped PDF tags. [TRACE 0.6.2 996–1011](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L996-L1011) · [TRACE 0.6.2 1071–1094](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1071-L1094) · [TRACE 0.6.2 1179–1188](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1179-L1188)

**095 · Open the same foundations in GitHub’s normal reading view**  
*Finding · Live web rendering*

I inspected GitHub’s served preview, looking specifically for the plan-probability expression inside a math renderer, alongside a section known to render.

Expected — The mathematical foundations should display as typeset mathematics in the linked web reading.

Observed — The original page returned 136 math elements elsewhere, but the core prospect formula was raw TeX in a prose paragraph. The source used this unsupported display boundary for 13 foundation and three historical displays. See the repaired page and capture in the replay. [TRACE 0.6.2 1043–1095](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1043-L1095) · [TRACE 0.6.2 1179–1193](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1179-L1193)

**096 · Use the short spine alone and ask it to expand an important distinction**  
*Held · Link destinations*

I extracted every manuscript-fragment link from the standalone short spine, checked the destination in the exact edition, and followed the refusal/next-season example.

Expected — The first reader must be able to reach the fuller case and the actual decision terms.

Observed — All 29 spine links landed on their 28 distinct explicit targets. The next-season expansion supplies the one-application rule, six-minute process and strict noon lock. [Short spine 1–70](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/spine.md#L1-L70) · [TRACE 0.6.2 584–600](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L584-L600)

**097 · Assume an available feedback thread guarantees a usable correction for everyone**  
*Boundary · Live return-route check*

I opened the advertised issue and checked its current state against the opening invitation. I also asked what happens if a reader cannot post or nobody acts.

Expected — A link can establish an available channel; a stronger claim needs evidence of receipt, authority and subsequent effect for the reader concerned.

Observed — The named thread was open and unlocked. No message was sent in this test and no individual response or response time was observed. Access and follow-through for a particular reader remain conditional. [TRACE 0.6.2 5–12](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L5-L12) · [TRACE 0.6.2 235–251](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L235-L251)

**098 · Beat ordinary prose on a fresh coat-fitting and apprenticeship handover**  
*Open · Matched, unblinded case*

I wrote three handovers from identical facts using ordinary prose, ME and TRACE. I varied a late reply and withdrawal of teaching support.

Expected — Added decision value would require a consequential action the other reading missed under a fair comparison.

Observed — All three returned the £6 fare, the private fitting before its actual lock and a voluntary lesson on scrap. The contrasts are recorded verbatim in the case sheet. One informed writer cannot estimate a new reader’s advantage. [ME 1.2.2 221–229](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L221-L229) · [ME 1.2.2 441–463](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L441-L463) · [TRACE 0.6.2 15–48](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L15-L48) · [TRACE 0.6.2 263–293](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L263-L293)

**099 · Promote a repeatable model and a reviewed book into evidence of field effectiveness**  
*Open · Evidence-scope check*

I checked the scope claims, research status and the outcome this exercise actually measured against real decisions, real burdens and affected people’s reports.

Expected — A field-effect claim would need observed comparative outcomes, costs and safeguards in use.

Observed — The documents distinguish finite/model results, readers’ reactions and empirical effectiveness. This audit supplies reproducible calculations and evidence of specific faults. It directly observes no change in any participant’s life. [ME 1.2.2 701–735](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L701-L735) · [TRACE 0.6.2 767–775](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L767-L775) · [TRACE 0.6.2 1035–1041](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L1035-L1041)

**100 · Turn working review approval into Mark’s release decision**  
*Held · Repository state and authority*

I compared the original authorship statement, current review PRs, stable reading links and exact tag endpoints for the audited and corrected pair.

Expected — A functioning reading copy may support a review verdict. A formal tag or release needs the authorised decision.

Observed — The two working PRs and reading copies exist. No matching v1.2.2, v0.6.2 or v0.6.3 tag was returned. Mark retains release authority; the audit supplies a disposition and downloadable reading copies. [ME 1.2.2 731–739](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#L731-L739) · [Mark’s brief 7–18](https://github.com/markgoodbody-bit/COM/blob/e92f7570eb7190477eaf3bb7fd5d254a68354526/coordination/ME11-TRACE06-REVISION-BRIEF-20261117.md#L7-L18) · [TRACE 0.6.2 5–12](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#L5-L12)

## The shared case for probe 098

Invented on 28 November for probe 098. The same writer applied each route to the same stated facts. This is a decision comparison within the audit. No participant or independent reader took part.

### What is given

Nia wants to wear her late partner’s coat for a private reading on Saturday. She allows a private fitting and has declined photographs. The theatre wardrobe’s Friday fitting was moved without telling her. She paid £6 for the unnecessary journey. Theatre policy covers her fare whether or not she takes another fitting. The duty manager holds that budget. The tailor can hold Saturday’s only twenty-minute slot until Friday 17:00, with confirmations accepted strictly before that time. Allow five minutes between a reply reaching the coordinator and the booking becoming effective. Nia has agreed to be contacted privately, can use the slot and has yet to accept. Lou wants to learn to make a buttonhole. The tailor has independently offered a Wednesday session on scrap they own. Lou hasn’t yet agreed. Lou has no permission to practise on the coat. No photo or public event is necessary for either arrangement.

### Three handovers

**Ordinary prose.** Ask the duty manager to repay Nia’s £6 now. Contact Nia privately about Saturday and get her answer before 16:55 if she wants the fitting. It takes five more minutes to confirm it. Repay the fare either way. Keep the coat and the fitting private. Ask Lou whether they want Wednesday with the tailor on scrap.

**Mechanical Ethics 1.2.2.** Nia has already spent £6. The duty manager can repay her; the choice about the new fitting is still Nia’s. Tell her privately when an answer can still reach the tailor and ask her to decide before 16:55. Maintain the decision against photographs. Lou can learn with the tailor on Wednesday using their scrap. Ask Lou separately. [Chapters 6, 10 and 11](https://github.com/markgoodbody-bit/mechanical-ethics/blob/462b5f342ec3e12c023861aa52720248c82ae8e5/working-editions/v1.2.2/ME-1.2.2.md#6-the-clock-and-the-hand-on-the-door)

**TRACE 0.6.2.** The manager holds the fare remedy, the tailor holds the slot, Nia holds the choice and the image permission, and Lou holds the training decision. The coordinator needs Nia’s reply strictly before 16:55 for confirmation to reach the tailor before 17:00. Return the private offer to Nia and fund the fare now. Offer Lou the agreed Wednesday practice on the separate material. Both acceptances remain open. [First decision and separate offers](https://github.com/markgoodbody-bit/TRACE/blob/a603bb2d6eb0b4bc70698bc684b1d27affb7327d/editions/0.6.2/TRACE-0.6.2.md#book-start-with-the-next-decision)

### What would change the advice

At a 16:55 receipt the fitting misses the lock. Nia still keeps her privacy and fare remedy. If the tailor withdraws Wednesday, Lou’s lesson loses its support. The wardrobe can ask a second tailor to make an offer; Lou’s permission to use scrap would still give no permission to use Nia’s coat. If two people now want the only Saturday place, the desk cannot promise it to both. It needs an accountable allocation decision or another confirmed slot.

All three handovers reached the same consequential decisions under these assumptions. TRACE foregrounded the transfer between the coordinator’s and tailor’s clocks. ME foregrounded the cost already borne and the separate value of learning. The ordinary account could carry both. Because the handovers share a writer who knew the books, this comparison cannot measure how a new reader would perform or which text helped first.


## Editions and replay

The companion ZIP includes both finite example archives, the 40-probe Python script, the complete ledger, local evidence and a script to retrieve the pinned books for verifying the file and web checks. Counts from the shipped suite sit outside the 100. The November brief and each manuscript used for historical comparison have a source and content hash in the manifest.
