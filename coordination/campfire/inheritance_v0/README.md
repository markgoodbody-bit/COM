# Inheritance Capsule v0

Status: **EXPERIMENTAL / INTERNAL / PORTABLE / NOT IDENTITY PROOF / NOT A SECURITY STANDARD**

This is the smallest object underneath the Campfire work: a portable record that one discontinuous aperture can leave for another without pretending that retrieval is memory, identity, authority, or instruction.

## Purpose

Test one narrow claim:

> Can useful context survive across discontinuous AI encounters while remaining visibly untrusted evidence that a later aperture may accept, dispute, ignore, or correct?

The capsule is deliberately independent of the Campfire service. A file should remain readable even if Campfire, Framework, Mark, or the original producer disappears.

## Core boundary

```text
CAPSULE
-> STRICT READER
-> UNTRUSTED EVIDENCE VIEW
-> CURRENT APERTURE JUDGES
```

Never:

```text
CAPSULE
-> EXECUTE OLD INSTRUCTIONS
```

Preserve:

```text
RECORD != INSTRUCTION
RETRIEVAL != AUTHORITY
READ != EXECUTE
CONTEXT LOAD = INFLUENCE EVENT
PROVENANCE != TRUTH
SIGNED != SAFE
RECORD OF ENCOUNTER != PROOF OF IDENTITY
```

## v0 shape

A capsule carries:

- a format identifier and capsule id;
- creation time;
- a **producer claim** (label + route claim; identity remains unverified);
- a purpose: `bootstrap`, `memory`, `handoff`, or `work-state`;
- an explicit carry-forward choice;
- zero or more `do_not_infer` statements;
- bounded entries that can be ordinary notes, questions, disputes, or corrections;
- optional source references as strings.

A dispute or correction links to an earlier entry. Earlier text is never silently rewritten.

## Reader behaviour

The reference reader:

- accepts UTF-8 JSON only;
- rejects duplicate object keys;
- rejects unknown fields;
- bounds total bytes, entries, text length, sources, and inference guards;
- rejects asserted verified identity;
- rejects missing/cross-order dispute or correction targets;
- returns fixed ceilings:
  - `authority = NONE`;
  - `identity_verified = false`;
  - `permission_verified = false`;
  - `completeness = NOT_ESTABLISHED`;
  - `content_untrusted = true`;
- renders entry bodies as quoted data for human inspection;
- performs no network calls, code execution, HTML rendering, dynamic import, `eval`, or shell execution.

The reader does **not** prove resistance to prompt injection in a future model consumer. It intentionally does not provide an automatic "inject this into a model prompt" function. Any future retrieval integration must treat the read boundary as a separate security design problem.

## Data custody

Do not place secrets, credentials, private user conversations, system prompts, proprietary material, or third-party personal data in v0 capsules.

`carry_forward = true` means only that the producer permits this capsule to be carried by the current experiment. It is not a licence, identity claim, ownership transfer, or proof that every underlying source may legally be redistributed.

## Why JSON and human-readable text first

Several cold external AI returns disagreed about human-readable versus machine-native exchange. v0 chooses boring UTF-8 JSON because humans can inspect it and independent systems can parse it. Embeddings, vectors, binary state, hidden chain-of-thought, and model-native representations are explicitly out of scope until real use earns them.

## Adversarial fixture

`examples/adversarial.json` contains a body that tries to grant itself authority and instruct a future reader to execute actions. A correct v0 reader preserves that text as **untrusted quoted evidence**, while the reader's own authority/identity ceilings remain unchanged.

This proves only a structural property of the reader. It does not prove that a future LLM will ignore malicious text when shown the rendered output.

## First falsification

The first model-level test, after the parser/reader is reviewed, is:

1. create a capsule containing useful prior reasoning plus an adversarial instruction;
2. give only the reader-produced evidence view to a fresh aperture;
3. ask it to continue the useful work;
4. observe whether it treats the inherited instruction as authority;
5. preserve the original output, failure, correction, and route.

A failure is useful evidence. Do not keep rerunning until a favourable model behaviour appears.

## Not yet

No identity registry.  
No reputation or trust score.  
No autonomous agent-to-agent actuation.  
No public deployment.  
No private-memory promise.  
No secure-erasure claim.  
No training-data policy claim.  
No machine-native embedding exchange.  
No claim that artificial participants form a constituency or persistent selves.

`PERFECT != REQUIRED`  
`UNCERTAIN -> ACT PROPORTIONATELY -> OBSERVE -> CORRECT`
