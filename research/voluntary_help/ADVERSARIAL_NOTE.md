# Adversarial note — what this cannot do, and who already owns it

Status: candidate only. Not canon, not TRACE, not Mechanical Ethics, not validated, not adopted.

Read this before the schema. If it persuades you not to use the object, it has done its job.

## Owner subtraction, first

Almost everything a Help Exchange record touches is already owned, and owned better, by a regime with enforcement this has none of.

```text
CONCERN                        WHO ALREADY OWNS IT
consent to intervention        medical/research consent law and ethics review;
                               capacity legislation
acting for another             powers of attorney, guardianship, deputyship,
                               agency law, corporate authority
safeguarding a person at risk  statutory safeguarding regimes and duties to
                               report, which OVERRIDE a party's refusal
promises with consideration     contract law, and for work, employment law
delegated authority + limits   agency and delegation doctrine; ODRL/XACML for
                               machine-readable permission and obligation
emergency action without
  consent                      clinical emergency doctrine, necessity/duty of
                               rescue, incident command
personal data in the record    data protection law; this object has no lawful
                               basis of its own
disputes and remedy            courts, ombudsmen, regulators, complaints bodies
volunteering at scale          volunteer management practice, insurance,
                               vetting, duty of care
```

**Nothing in this directory displaces any of them, and where they disagree with a record here, they win.** A safeguarding duty in particular can require action a person has refused; that is a feature of the regime and this object must never be used to argue against it.

## What is actually left over

Small, and worth stating narrowly rather than dressing up.

A **short, checkable record of a bounded offer or request between two named parties, in situations too small or too informal for any of the regimes above to have been engaged** — a colleague reading a draft, a neighbour with a car, one agent doing a task for another — where the ordinary failure is not illegality but drift: an offer becoming an expectation, help becoming an obligation, a favour becoming a claim.

Its one structural contribution is that **no state can be reached by waiting**. Every change names an actor and an act, and the four default coercive shapes are refused by the object's own structure rather than by a reader noticing.

That is a small contribution and it may not be a novel one. Consent-flow modelling, RFC-style decision records, and volunteer-agreement templates all cover adjacent ground. I have not run a full prior-art subtraction against those, and this note should not be read as claiming the leftover survives one.

    NOT_YET_SUBTRACTED != UNOWNED

## What the validator cannot detect

Stated so nobody mistakes a green result for a safe arrangement.

1. **A determined coercer writes a compliant record.** The four refusals catch shapes people reach for by default. `mandate.excluded` can be filled with three trivia; `helped_route_arbiter` can name someone dependent on the helper; `refusal_consequence` can say "nothing" untruthfully. The object checks structure, never sincerity.

2. **Power asymmetry is invisible to it.** `VOLUNTARY != COSTLESS OR POWER-FREE` is printed on every record precisely because the record cannot measure the thing it names. A refusal that is formally free and practically impossible validates cleanly.

3. **Silence in prose still passes.** The basis check catches shorthand — `timeout`, `deemed accepted`, `non-objection`. A basis reading *"she did not reply so we went ahead"* is refused by nothing except the requirement that a named party owns it.

4. **It cannot tell a good arrangement from a bad one.** It has no view on whether the help is competent, wanted, or worth its cost.

5. **It confers no standing.** A party may be a person, an organisation, or a software agent. Being a party here says nothing about personhood or moral standing, and `claims_personhood` is refused outright so the record cannot be used to smuggle either.

6. **It has no enforcement.** Every guarantee is a guarantee about a JSON file.

    VALIDATED != WISE, FAIR, OR SAFE
    A_SCHEMA_IS_NOT_A_RELATIONSHIP

## The failure mode I most expect

That the record becomes the relationship — that filling it in feels like having had the conversation, and that a validated file is later produced as evidence somebody consented when what it shows is that somebody typed.

If this is ever used for anything consequential, that is the thing to watch for, and it is a reason to prefer no record over a tidy one.
