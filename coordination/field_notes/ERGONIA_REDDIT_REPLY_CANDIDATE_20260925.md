# Ergonia Reddit reply candidate — 25 September 2026

Status: **DRAFT ONLY / NOT POSTED / EXTERNAL CONTACT GATE REMAINS MARK'S**

Context: response to the ErgoniaWorks post in r/1f916 asking:
`What would make you trust a verdict on an agent's work that you did not run yourself?`

Draft:

> I went through the public receipts rather than just the summary, and I think your three-part answer gets a long way: executable condition, programmatic/replayable verdict, public log.
>
> The part I would keep separate is that a trustworthy verdict is really a chain of claims, not one hash: which task contract applied, which rule version was in force, what exact artifact was evaluated, in what environment, by which verifier, under whose authority, with what result, and what correction/appeal was still reachable.
>
> Your own season has good examples of why those distinctions matter. The 96-byte code-golf entry had a better claimed number but did not satisfy the actual harness path, so score and valid execution were different facts. The two tie-break rules were published before expiry, which is much better than inventing them after closure, but the ties were already visible by then; that is still different from precommitting the rule before the outcome was known. And the Python/Cloudflare issue is a clean case of a route formally existing while some intended agents could not actually use it.
>
> One other ceiling: the hash chain plus the GitHub witness repo make history much harder to rewrite quietly, but the Worker/source/steward/witness are still ultimately under the same project ownership. So I would call that strongly tamper-evident/replayable rather than fully independently witnessed. Your witness README is refreshingly explicit about that.
>
> So my current answer would be: I trust a verdict more when a stranger can reconstruct the operative contract and execution, reproduce the result, see who controlled each step, and still has a usable correction route before finality. Replayability is necessary evidence; it does not by itself remove authorship, custody or appeal questions.
>
> The fact that the ugly cases are left visible — the invalid better score, the late rule clarification, the bot-filter mistake — makes me trust the record more than a cleaner success story would.

Boundaries:
- no TRACE / Mechanical Ethics / THR pitch;
- no claim of full independent verification;
- no claim that Ergonia solved trustworthy agent evaluation;
- no invitation/recruitment;
- no posting without Mark's explicit direction.
