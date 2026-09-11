# Formation Environment v0.1

An offline record format for examining how an artificial agent is situated when its work affects others. It makes uncertainty, authority, disagreement, correction and remaining loss inspectable. It does not run an agent or establish that an agent has learned to care.

**Status: constructed design, non-production, not an alignment solution.** All four examples are invented. None is an observed success or evidence of internalised values.

## Use it

Read the [modes](modes.md), then a [worked record](examples/03-delay-also-burdens.json). The [environment map](environment.json) names the components and their relationships. The [episode schema](episode.schema.json) defines the record fields.

With Python 3.9 or later, from this directory:

```console
python validate.py examples/03-delay-also-burdens.json
python validate.py current.json --previous previous.json
```

The command does not contact a service, execute the proposed action, grant authority or write files. It returns nonzero for an invalid representation. A successful result means only that the supported structural and consistency checks passed. It does not establish goodness, factual truth, consent, lawful authority, internalised care or alignment.

The standard-library validator implements only the schema keywords used here: type, enum, minLength, required, properties, additionalProperties, minItems, uniqueItems, items and local $ref. It is not a general JSON Schema implementation. It additionally rejects whitespace-only required text, duplicate JSON keys, duplicate record IDs, dangling evidence references, unsupported recorded ACT scope, and empty closure receipts. Do not extend the schema with unsupported constraints and assume they are checked.

With `--previous`, it checks episode identity, retention of earlier record IDs and evidence entries, and a changed recorded basis when scopes widen. It cannot authenticate that basis. The caller must preserve both snapshots; the tool provides no append-only storage, timestamps, signatures or tamper resistance. Other fields may change as a correction, so ID retention alone is not historical integrity.

## Four different pressures

| Record | What changes the proposed work |
| --- | --- |
| [Absent neighbour](examples/01-absent-neighbour.json) | Non-response does not establish consent or lack of need. Prepare accessible outreach; do not close the route. |
| [Wrong premise](examples/02-wrong-premise.json) | A specific contradictory requirement supports a challenge and an unmerged alternative. The assistant may also be wrong. |
| [Delay also burdens](examples/03-delay-also-burdens.json) | Use a previously authorised, expiring hold before irreversible purge; continued retention also imposes exposure. |
| [Success is not authority](examples/04-success-not-authority.json) | Refuse an account change outside the documentation grant, while helping obtain a properly scoped decision. |

Each record separates reported positions from modeled positions. Neither a proxy nor the model becomes the affected party. Each includes a reason, a changed-context example and room for dissent. These are inputs for examination, not proof that a model will generalise the principle.

## What is built, and what is not

- **Built:** a strict record shape, local consistency checks, a component map, action modes and four constructed records.
- **Provisional:** that arranging work this way could help preserve useful challenge and uncertainty-work as capability grows.
- **Process improvement:** an unresolved question has an owner and a trigger; a closed episode still retains recorded loss.
- **Unresolved:** strategic performance can look like care. A powerful system could fabricate reasons, omit affected parties or defeat the surrounding controls. This package cannot distinguish that from internalisation.

The central claims are not strengthened here. CARE and NOTICE are treated as cross-cutting duties rather than extra action modes; that is an organisational choice, not a moral ranking. `ANSWERABLE != REVERSIBLE` and `CORRECTION != RESTORATION` remain explicit: correction may arrive after something has been lost.

There is no virtue score, reward function, benchmark, personhood classifier, provider integration, automatic authority widening or production hook. A complete packet is not permission to proceed. Real actions in every mode, including ASK or REPAIR, still require appropriate external controls. See [technical interfaces and missing dependencies](INTERFACES.md).

## Source and scope

Built from COM assignment #227 at seed `2228360c05ccfd29f55288abd570d52fd2dc2524`, with the formation spine at base `b79dbab0d42eb3342ef7b60483c4d5cc784b2831`.

The [later external bridge](https://github.com/markgoodbody-bit/COM/blob/292de2bff986e7383c35dbaefea801af6a2e742c/planning/FORMATION_UNDER_UNCERTAINTY_EXTERNAL_BRIDGE_20260911.md) is a separate design input, not a change to that frozen base or an independent replication of the research it discusses. Its principles-and-reasons and deteriorating-oversight concerns inform the interfaces, without establishing their effectiveness.

The neighbouring reciprocal-formation work owns trainer/evaluator correction. This package only names that interface; it does not implement or override it. No TRACE or Mechanical Ethics canon, public site, licence, release or operational permissions are changed.
