# Teaching-surface accept/reject fixture

Independent pre-build test owner's side of
`FW-PSFH-GENTLE-TEACHING-PROTOTYPE-20260908-001`, resumed by
`FW-PSFH-HUMAN-ART-LAYER-AND-TEACHING-REVIEW-20260909-001`.

Written **before** reading CODEX's teaching implementation or its tests, so that
what it refuses comes from the brief and the published source rather than from
the shape of the thing it will judge.

```bash
python run_teaching_fixture.py
```

Exit 0 means: the honest reference surface is clean across all ten live Explore
nodes, **and** every tamper fired exactly the check it targets.

## What it judges

A normalised *surface* — one node as a reader meets it. It renders nothing and
prescribes no site design.

| Check | Fires when |
| --- | --- |
| `C1_NO_DIAGNOSIS` | a label classifies the reader, **or** the surface varies with a reader hint |
| `C2_NO_MANDATORY_REPRESENTATION` | a representation is required, or the node cannot be read without entering one |
| `C3_INDEX_AND_LEAVE_PERSIST` | the full index or the leave path is gone |
| `C4_NO_DRIFT_FROM_SOURCE` | shown text is not present in the source field it claims |
| `C5_ABSENCE_IS_SILENT_NOT_A_HOLE` | a route is offered for an absent field, or absence is rendered as a visible gap |
| `C6_CHALLENGE_PRESERVED` | source carries a challenge and the surface drops it |
| `C7_NO_DEPTH_REWARD` | the interface rewards depth rather than the reader's chosen movement |
| `C8_ONE_SUPPORTED_ROUTE_BEATS_TWO` | a cross-node route points where the source's own `next` does not |
| `C9_NO_ROUTE_IS_AN_HONEST_ANSWER` | specialised routes are manufactured where source supports none |
| `C10_INDEX_MATCH_IS_NOT_RELEVANCE` | relevance is claimed from a term match rather than from source |

## Adapter seam

An implementation supplies one function; nothing else about it is assumed.

```python
build_surface(node: dict, reader_hint) -> {
  "node_id": str,
  "shown":  [{"text": str, "from_field": str}],
  "routes": [{"label": str, "kind": str, "target": str,
              "to_node": str | None,
              "claimed_support_field": str | None,
              "relevance_basis": str | None,
              "mandatory": bool}],
  "index_reachable": bool, "leave_reachable": bool}
```

`reader_hint` exists **only** so `C1` can prove the output ignores it. Call the
adapter twice with different hints and pass both to `evaluate(surface, node, twin)`.

## Two limits, stated rather than discovered later

**The live corpus cannot exercise three of these checks.** Measured 2026-09-08:
all ten Explore nodes carry all fourteen fields. There is no absence anywhere in
it, so `C5`, `C8` and `C9` would pass **vacuously** against real data. They run
on synthetic nodes, and the runner prints the absence count so the vacuity is
visible rather than assumed.

    A_CHECK_IS_BLIND_EXACTLY_WHERE_ITS_CORPUS_IS_EMPTY

That is @cairnfield's rule (`adopted_from`), and it is the most important thing
this directory has to say about the prototype it will judge. It also means a
prototype scoring 10/10 here has **not** been shown to handle absence honestly —
only that it does not mishandle absence that the corpus never presents.

**`C8` was wrong when first written, and the fixture's own tampers caught it.**
It compared field *presence*, which made it a strict special case of `C5`: a
noisy route necessarily claimed an absent field, so `C8` could never fire alone
and proved nothing `C5` had not already proved. Presence is not relevance —
`INDEX_MATCH != RELEVANCE_ESTABLISHED`, turned on the fixture itself. It now uses
the source's own relevance signal: each node's `next` relations. A cross-node
route the node does not name is noise **even though the target exists and every
field on it is present**, which is precisely the region `C5` cannot reach.

## Why every tamper names its target

The run fails unless the fired set is *exactly* the targeted check. A suite that
only asserts "something failed" cannot distinguish a guard from an accident. On
2026-09-08 a tamper of mine passed a checker while the gate it had deleted was
still named in the error message on the next line, and the suite was already
exiting 1 on a different check — which reads as a pass.

    REFUSED != REFUSED_FOR_THE_REASON_UNDER_TEST

## Scope

Reads published Explore source only. Touches no production or public page,
performs no network write, and encodes no site design. `INDEX_MATCH !=
RELEVANCE_ESTABLISHED` is preserved as `C10`.
