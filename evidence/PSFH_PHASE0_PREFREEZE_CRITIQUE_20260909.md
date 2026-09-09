# Phase 0: design gaps before freeze

Status: DESIGN CRITIQUE / SYNTHETIC ARITHMETIC ONLY / NO STUDY EXECUTION
Basis: candidate atff54721de507d006212d17f201c6b287a8cfb75d;
FW COM119/5601095493. Prepared by Codex, 9 September 2026.

## Earned logical gaps

1. **Empty-set scoring is undefined.** F1 is2m/(a+b); when both builders return
   zero, this is0/0. The design allows unanimous-zero accounts to count toward
   survival but gives no scoring or pooling rule for them. All-zero results
   cannot support the proposed recall denominator even if absence agreement
   is perfect. Do not silently score that as either failure or success.

2. **A permissive empty-set convention can dominate the pooled median.**
   Synthetic example, not selected accounts: two unanimous-zero accounts, then
   one account where each builder names5 points and exactly2 are shared by all3.
   If empty-empty F1 is set to1, the9 pair scores are
   `[1,1,1,1,1,1,0.4,0.4,0.4]`. Their median is1. The nonempty account's median
   is0.4, satisfying the proposed lower floor; it has2 consensus points. Thus
   these F1/coverage conditions can pass despite the informative account falling
   below0.60. This is conditional on the unchosen empty-set convention, not a
   claim that the current incomplete protocol has already returned PASS.

3. **External-fact denominator is inconsistent.** Points needing facts absent
   from the account are excluded from the consensus core, but a later gate asks
   whether fewer than20% of core points have that dependence. After correct
   exclusion that fraction is necessarily zero (or undefined for an empty core).
   To measure source insufficiency, preserve and assess pre-exclusion candidates
   with an explicitly named denominator instead.

4. **Matcher agreement needs a candidate-pair rule.** If all cross-builder pairs
   are offered, easy NOT MATCH decisions can dominate80% agreement. If only likely
   matches are offered, whoever selects them can suppress difficult candidates.
   Specify the pair universe, separate positive/negative agreement and report
   UNCERTAIN rather than presenting one percentage as sufficient.

5. **Pairwise matching does not yet define a three-builder core.** A1↔B1 and
   B1↔C1 do not themselves establish A1↔C1. Broad/narrow points can produce
   inconsistent triangles. Specify family formation and conflicting one-to-one
   matches before an adjudicator sees outputs; do not use transitive closure
   silently to create consensus.

## Provisional repairs, not a replacement protocol

- Report zero-account agreement separately from nonempty extraction reliability.
  Predeclare how much nonempty reference material is required for later recall;
  there is no justified numeric requirement adopted here.
- Keep source-sufficiency exclusions observable before filtering.
- Define the matching universe and treatment of inconsistent families before
  selecting an aggregation or numerical threshold.
- Freeze only after those decisions. Current result is INCOMPLETE DESIGN, not
  failed empirical construct, evidence of usefulness, or a reason to replace cases.

No public accounts were selected, annotated or replaced. No reference builder,
participant, paid model, private reasoning trace or Mark-as-gold-standard was used.
The arithmetic example is a check of the proposed rule, not Phase0 data.
