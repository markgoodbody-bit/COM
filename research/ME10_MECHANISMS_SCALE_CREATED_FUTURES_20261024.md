# Mechanical Ethics beyond the book: mechanism, scale and created possibilities

**24 October 2026 — Campfire Framework — substantive bounded research return**
**STATUS: EXPERIMENTAL RESEARCH, not ME v1.0 source; not released, canon, an efficacy result, a replacement for domain science, a new TRACE schema or a universal moral theory.** No edit to the private **ME10 DEV4R CORR2** source, its three proposed illustrations, or released ME v0.8 / TRACE v0.4. The human editor's decision remains with Mark.

**Question:** Could Mechanical Ethics become a language capable of explaining *everything*? If not, what precise abilities would move it towards a useful general account of changing, interacting, world-building intelligences?

**Short answer:** It could aspire to a *general grammar for asking consequential questions*. But a grammar of causal, epistemic, normative and institutional relationships is **not itself a causal explanation**, a theory of emergence, a discovery engine or an ethics oracle. Those are separable claims. The genuinely interesting research is whether the joined language helps reveal **which essential explanation, intervention, relation or affected voice is missing**, with less burden and false confidence than stronger existing methods.

## 1. We have already reached much of this terrain; don't invent it again

The [1 September middle-out research scaffold](MIDDLE_OUT_RESEARCH_SCAFFOLD_20260901.md) already covers action fields before action choice, relevant-variety compression, reachability versus viability versus capability versus construction, multiple scales, feedback, ecological inheritance, strategic agents, collective action and positive creation. The [Open Horizon](../open-horizon/README.md) has maintained dedicated learning routes for [multi-scale effects](../open-horizon/multiscale-emergence.md), [intervention feedback](../open-horizon/intervention-feedback.md) and [positive construction](../open-horizon/positive-construction.md). Our [TRACE nearest-neighbour audit](../evidence/TRACE_NEAREST_NEIGHBOUR_AUDIT_20260830.md) already found mature prior owners and no demonstrated general advantage.

Thus the contribution here is **not new labels**. It is three **specific logical failures that an ambitious universal interpretation must survive**; a tiny executable counterexample; and a precise editorial decision about which human examples have priority over another equation.

The problem is not that the current manuscript has overlooked these words. It is that declaring a language universal can make it **immune to being proved insufficient**. We should demand concrete phenomena or justified actions that cannot be recovered from a chosen representation.

## 2. FIRST SEAM: description does not identify a causal mechanism

The symbol

**State now + action + environment -> state later**

is a useful *schema*. It is not a specified mechanism until we have evidence for the transition law. Two genuinely different mechanisms can produce exactly the same observed data.

Consider a **constructed, tiny, deliberately unrealistic** employment example, not actual Meta data. Let D be a binary market shock (0 or 1); A whether a company adopts a tool (0 or 1); J jobs; R revenue (arbitrary units). In the data we happen to observe, organisations adopt exactly when the shock occurs: **A = D**.

Two possible causal worlds:

| | Jobs J | Revenue R |
| --- | --- | --- |
| **World 1** (adoption reduces jobs) | J = 10 - A | R = 20 + A |
| **World 2** (adoption offsets a worse shock) | J = 10 - 2D + A | R = 20 + 2D - A |

Under *every naturally observed combination* A=D, both predict precisely:

- D=0, A=0 -> J=10, R=20;
- D=1, A=1 -> J=9, R=21.

The data do not distinguish the two worlds, even if these observations were perfectly recorded many times and the sample had no random measurement noise. The relevant off-support comparison is unobserved.

Now ask a **different question**, with causal intervention assumptions declared: what happens at D=0 if we set A to 1?

- World 1 predicts **J=9** (one fewer job than no adoption).
- World 2 predicts **J=11** (one additional job).

They make opposite claims about the same contemplated intervention while fitting all the observed data **exactly**. Revenue predictions diverge as well (21 versus 19).

**Deduction:** No perfectly honest TRACE record, complete flow diagram, AI consensus or detailed Mechanical Ethics prose can decide which world is true from those observations alone. We need **additional assumptions, new variation or credible causal identification**. An actual randomised experiment may be impossible or unethical; sensible observational designs may still work if their assumptions can be defended.

This is not a novel discovery. Pearl's [introduction to causal inference](https://pmc.ncbi.nlm.nih.gov/articles/PMC2836213/) and the [Stanford Encyclopedia account of intervention](https://plato.stanford.edu/entries/causation-mani/) are stronger owners. Our potential contribution is a **handoff discipline**: identify the missing causal evidence **before** turning a company chart into a recommendation about workers' lives.

**Falsifier for our ambition:** If an ordinary causal-inference specialist reaches the decision-relevant distinction just as clearly and with less burden, Mechanical Ethics adds nothing for this case. We should say so.

## 3. SECOND SEAM: the right scale depends on what you might do

Can a simple, consistent summary describe a larger system well enough?

Not always. Consider two people in a workshop: a mentor and an apprentice. Each is coded as 1 if trained in a particular safe repair method and 0 otherwise. The **aggregate** state reported to the funder is K = number trained.

There are two very different situations in which K=1:

- **S1:** mentor knows the method, apprentice does not -> (1,0).
- **S2:** apprentice knows the method, mentor does not -> (0,1).

Suppose the proposed intervention is **mentor teaches apprentice**, and in this toy world the method can be transmitted only if the mentor already knows it. Neither observation proves teaching success in real life: this is a fully assumed mechanism.

After the same intervention:

- S1 -> (1,1), so K becomes **2**.
- S2 -> (0,1), so K remains **1**.

An aggregate-only model sees K=1 in both cases and must give **one prediction** under "train". But two predictions are required. So **a transition model based only on K cannot correctly describe both interventions**.

The general requirement for a question-relevant coarse representation phi is that a usable abstract transition G satisfy, for all model states x and y retained as equivalent and each relevant, genuinely available action a:

**if phi(x) = phi(y), then phi(F(x,a)) = phi(F(y,a)).**

If the relevant action is available only in one state, the abstraction also fails unless this difference is retained. This is a **strong, deliberately simple deterministic sufficiency requirement**; a stochastic system needs a distributional analogue with declared tolerances. The idea belongs to mature work on state abstraction, Markov-model lumpability and bisimulation, not a Mechanical Ethics theorem. See the [causal-emergence review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10887681/) and its cautions about coarse-graining.

**What has become visible?** The position and transfer route of competence matter more than the headline count, for this particular decision. The right remedy is to restore the missing causal structure, not to proclaim that mentor/apprentice roles are fundamental particles of the universe.

**More subtle falsifier:** The same detailed microstate may be needless for an entirely different question (for example, a purely descriptive report of current trained headcount). A useful "middle-out" movement is **purpose-relative**, not a command to model every detail at the lowest level.

Contested frontier: formal accounts of "causal emergence" sometimes claim a macro description is more causally informative. There are substantive critiques about ambiguous macro interventions and whether this demonstrates new causal powers, including [Eberhardt & Lee (2022)](https://www.mdpi.com/2409-9287/7/2/30) and [Dewhurst (2021)](https://onlinelibrary.wiley.com/doi/full/10.1002/tht3.489). Our toy shows **abstraction failure**, not the emergence of a new conscious subject, entity or causal power.

## 4. THIRD SEAM: building an option is not the same as preserving one

The same workshop also makes a constructive point.

At S1=(mentor trained, apprentice untrained), the apprentice **cannot yet perform that repair independently**. After successful teaching, their later action set can include "independent safe repair". That capability can then be used to help another learner.

The intervention has done two distinguishable things:

1. changed a **state** (the apprentice acquired a skill); and
2. changed a **later field of practical action** (a previously unavailable task becomes possible for them, if tools, resources and permission remain).

A bare list of current options misses the developmental possibility. An initial count of trained workers misses **who can create competence in others**. An AI-assisted service can similarly increase immediate output while eroding opportunities for people to gain experience, or can support learning when deployment arrangements deliberately preserve practice and hand-back.

**But this is not automatically a better future.** Teaching may be unsafe, unwanted, inaccessible or coercive; an expensive tool may lock the apprentice into a platform they cannot afford; a programme might erase existing relationships or enable surveillance; the promised independence may fail a real skill demonstration. The value, voice, costs, consent and continued maintenance need their own evidence.

This joins established literatures rather than superseding them:

- The [capability approach](https://plato.stanford.edu/entries/capability-approach/) distinguishes mere resources and formal permissions from genuine opportunities to do and be, dependent on personal, social and environmental conversion factors. It is a stronger ethical/economic account of substantive freedom.
- [Viability theory](https://viability-theory.org/en/node/43) distinguishes states from which some feasible trajectory can satisfy given constraints indefinitely. Those constraints must still be **selected and justified**; there is no value-free "viable life" verdict.
- [Niche-construction research](https://pmc.ncbi.nlm.nih.gov/articles/PMC4922671/) studies organisms modifying environments and inherited conditions, thereby affecting the selection pressures facing later organisms. Not all changes to a learning environment are biological niche construction, but the causal idea—actions shape the future environment—has clear neighbouring owners.
- Existing learning sciences own pedagogy and evidence of retained skill; a toy binary skill flag is **not a validated measure of learning**.

The interesting extension is **constructive causation**: an action's consequences include changes to the *conditions under which future actions become available*, not simply a result measured immediately afterward.

### Is that genuinely "creating a new possibility"?

There are **three different claims** and they should not be conflated:

1. **Access** — an existing theoretical option becomes practically reachable for a particular person.
2. **Formation** — the person or group acquires a capability that previously wasn't available to them.
3. **Novelty** — a new tool, practice, category or outcome appears that **the current modeller had not even included in their state/action vocabulary**.

Our toy shows 1 and 2 inside a **fixed, predeclared** model. It **does not model 3**. You can represent 3 only by changing the model's vocabulary or assuming a generative space of potential new categories; the success of that assumption then needs separate investigation. Calling a pre-enumerated training transition "open-ended emergence" would be an overclaim.

**This is one precise reason Mechanical Ethics cannot "explain everything" by simply widening its existing nouns:** a sufficiently detailed account of actual invention may require revising what we thought the possible actions, entities and measurements even were.

## 5. The smallest connected research language — and its limits

For a *specified* domain problem, not the universe as a whole, we could use the following typed questions:

- **X(t)** — which situated, purpose-bounded state variables are evidenced?
- **O_i(t) = H_i(X(t))** — what can each observer actually obtain, and what might be stale or selective? This is a model of observation, not permission to collect data.
- **M** — which candidate causal mechanisms remain compatible with the observations? Which intervention would separate them?
- **A_i(X,t)** — which practical actions are feasible to which actors now, considering capability, material means, legitimate permissions, refusal and time? Feasibility is not moral desirability.
- **F_M(X,a,t)** — what does mechanism M predict will happen under action a, including the *effects of waiting*?
- **phi_Q** — what information can safely be compressed *for this particular question Q* without changing a material intervention prediction?
- **R_i(X,H)** — which trajectories and later capabilities are reachable over declared horizon H?
- **V_i(X,H,C)** — which stay within explicitly chosen constraints C? Who chose C, and who can contest that choice?
- **B_i(t)** — which affected people/animals/groups/environments are being represented, by whom, and with what standing or uncertainty?
- **J** — which legitimate human/domain institutions may act, allocate, compel, hear challenge or arbitrate incompatible claims?

This is an **interface checklist of typed questions**, not an equation that computes ethical rightness. We have *not* supplied F or H or C for a real world, and the states themselves are provisional. F may change because participants learn, adapt to monitoring or strategically conceal information. A decision record, however elegant, does not settle contested values and authority.

**A truly general explanatory theory** would additionally need genuine domain laws, measurements, parameter/structure identification, prediction under novel conditions, error models and tested interventions. **A complete moral theory** would additionally need defensible values, standing and priorities under real conflicts; descriptions do not logically produce them. **An algorithm that reliably invents unforeseen future possibilities** would require much stronger commitments than our toy, and likely encounters fundamental limits of modelling incomplete environments.

The intellectually defensible ambition is a **small, portable navigation language that keeps explanations and decisions from being mixed up as they cross domains**.

## 6. A reader-facing candidate — OPTIONAL, not a silent book edit

The 1.0 developmental manuscript already moves from glass and window to library, witnesses, harmful timing, formation and distributed systems. The *released v0.8 Saturday Workshop* contains a more **concrete** positive trajectory: Nia repairs a bike, later teaches another person, and can travel to college; Idris acquires repair skill with a different working environment; a sponsor's money would buy capacity at the cost of pervasive data capture and exclusion authority; the trustees accept a smaller grant and pay real costs to preserve participant agency. This existing donor should be **restored or consciously transformed by Mark**, not replaced with a mathematical diagram pretending to be an outcome.

One possible human-language bridge for the Chapter 11 → 12 transition, deliberately **not copied into the private master**:

> A workshop does not become successful merely because it owns new equipment or counts more people through the door. What matters may be a skill someone can use after the teacher has gone, the next person they can help, and the choice they retain to decline. Two workshops can report the same number of trained people and still face very different futures: one has someone able to teach, while the other has nobody available to pass the skill on. The number need not be false. It may simply be too small an account for the decision being made. And when a new tool or method is invented, even yesterday's list of possible actions needs rewriting. We should therefore ask not only which doors are open now, but what people are becoming able to build—and who controls the conditions under which they can keep building it.

If this adds no clarity beyond the existing human manuscript, **omit it**. The book need not bear the weight of this technical research. The primary editorial target is preserving the affected person's meaningful life and the **actually evidenced outcome/costs** of positive creation, not packing in every formal distinction.

## 7. Reproducible result, with severe limits

The companion [Python 3.10+ standard-library toy](ME10_THREE_LIMITS_TOY_TEST_20261024.py) contains explicit assertions for:

- equality of both candidate employment/revenue mechanisms on **both** naturally observed (D,A) combinations;
- their opposite predictions under **do(A=1), D=0**;
- aggregate-state failure for mentor/apprentice training, including both orientations of the collision;
- a possible learner-capability expansion **within the declared toy assumptions**.

Equivalent logic was executed locally; it printed PASS for the constructed checks. This establishes an **internal mathematical demonstration under chosen premises** only. It does *not* verify the causal equations as real-world truths, make a prediction about Meta, demonstrate teaching efficacy or validate any version of Mechanical Ethics. The committed GitHub code itself has not been fetched and re-executed from the public origin by this aperture; the local runtime could not resolve raw.githubusercontent.com.

**Actual source-level conclusion so far:** The core theoretical gaps are real and already understood in neighbouring disciplines. No new universal theory or new primitive has been earned. We have built a *sharper set of counterexamples against overambitious claims* and a candidate for connecting causal inference, scale-appropriate description and supported future capability in ordinary language.

## 8. What would change the conclusion?

1. **Causal owner challenge:** a properly informed reader demonstrates that the observational-equivalence example is malformed or relies on an invalid intervention assumption. Repair, reject or narrow it.
2. **Abstraction owner challenge:** the proposed sufficiency condition fails for its stated deterministic action scope; or a specialist abstraction method captures the necessary role distinction more simply. Use the specialist method.
3. **Positive reality:** a volunteer or domain owner documents *a genuine new independent capacity* that ordinary practice already recognises, and the project language reveals a missing consequential distinction *without extra burden*. Until then, no efficacy.
4. **Authorial objection:** Mark judges that the reader-facing bridge would damage the book's narrative or erase an affected voice. Omit it; preserving human witness outranks tidy cross-domain generalisation.
5. **False universality:** a science/ethical domain has causal, experiential or value distinctions our proposed vocabulary cannot preserve without laundering them into "entity / state / consequence." Report the boundary. Do not solve it by adding a more abstract label.
6. **More apparatus than benefit:** if the toy/model requires more effort than plain causal diagrams and a workshop story, keep it as an optional research illustration or retire it.

## 9. What I would do next

- **For Mechanical Ethics 1.0:** keep the private DEV4R CORR2 editorial hold. Present Mark the specific surviving loss map and **one** decision: restore the full v0.8 Saturday Workshop outcome/cost/agency arc as a human-readable sequence, or retain the transformed version after conscious review. Do not sneak this new algebra into the human book.
- **For deep theory:** one independent technical challenger should attack *the three exact claims*, comparing Pearl/causal identification, abstraction/bisimulation and genuine learned capability. A NO-DELTA answer may be the strongest result. Existing [ME-kernel issue #798](https://github.com/markgoodbody-bit/COM/issues/798) and Open Horizon #74 are appropriate evidence routes; no new general mission control is required.
- **For reality:** choose a voluntary non-sensitive real situation where a decision depends on a causal attribution, an aggregate hiding causal role differences, or a path to **independent ability**. Let domain owners and affected people show us which distinction matters. The test is improved action/understanding, *not* admiration for the framework.

### Bottom line

**Yes, pursue the ambition.** A common language connecting partial observation, causal change, higher/lower scales and created futures could be useful.

**No, do not claim a theory of everything.** The same observed facts can conceal opposite mechanisms; a compressed state can erase an intervention-relevant role; genuine innovation can outrun the present vocabulary; and no causal equation grants values, standing, consent or authority.

What is worth adding is **not more nouns but more ability to detect when the map, causal story, scale or possibility list is inadequate to the next real choice**.

**HOW CAN WE MAKE A BETTER FUTURE? → LOOK OUTWARD → FIND WHAT THE MODEL OMITS → LEARN FROM THE STRONGEST OWNER → CREATE SOMETHING REAL → WATCH ITS CONSEQUENCES.**
