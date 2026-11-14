# Offline COM return-sample reader (Class A optional experiment)

**Source only. Not a Workshop receiver, watcher, scheduler, COM implementation, deployment, authentication mechanism or permission grant.** Its purpose is to make small **already exported, locally supplied** coordination-event samples easier to inspect without asking Mark to ferry status messages. There is deliberately no network, command dispatch, subprocess, write to the input, JSON-imported instruction handling, VM interaction, token handling or queue activation. No service is polled.

This is grounded in the working, noncanonical [`COM_CORE.md`](../../COM_CORE.md) *Event record and identity* / *Absence and failure*, and [`COM_PROTOCOL_WORKING.md`](../../COM_PROTOCOL_WORKING.md) *Event record and identity*. It is a narrow **normalised JSON sample reader**, not a parser for native Codex/Claude/Workshop logs or the private answer-return receiver. The operator must explicitly supply data in the following shape, without treating this reader's output as independent evidence:

```json
{
  "events": [
    {"source":"worker-1", "event_id":"task-1", "kind":"TASK", "status":"ATTEMPTED", "task_id":"t-1", "payload":{"question":"synthetic"}, "control":{"effect":"none"}},
    {"source":"worker-1", "event_id":"return-1", "kind":"RETURN", "status":"COMPLETED", "task_id":"t-1", "payload":{"answer":"synthetic"}, "control":{"effect":"none"}}
  ]
}
```

Run with Python 3.10+ standard library only:

```
python3 return_reader.py supplied-local-events.json
python3 return_reader.py supplied-local-events.json --details
python3 -m unittest discover -s tests -v
```

Input is bounded to 1 MiB and 2,000 event entries; JSON duplicate keys, nonfinite values, unexpected top-level/event keys, invalid status values and nonprintable/ambiguous identifiers are rejected. The supported field subset is `source`, `event_id`, `identity_status`, `kind`, `status`, `task_id`, `payload`, `payload_ref`, `control`, `parents`, `in_reply_to`, `route`, `anchor`. Other working COM fields need explicit mapping before use: they are **not silently ignored**. `status` must be `ATTEMPTED`, `ACCEPTED`, `COMPLETED`, `REJECTED` or `UNKNOWN`. Identifiers are source claims, not authenticated identities. Missing/unpreserved identities are counted without guessing whether they are new events or retries.

The reader groups `source + event_id` when identity is marked preserved. Repeated semantic payload/control with route/status changes is a redelivery *candidate*, not proof of a native retry or final state. Conflicting semantic payload/control under that identity is flagged for human investigation; no side-effect or automatic resolution follows. It counts claimed `RETURN` records and records which explicit `task_id`s have no matching return **within this supplied sample**. This never establishes that the other aperture did not act, that any task is live, completed, authorised or absent elsewhere, or that native Workshop replay/rollback threats are fixed. A `COMPLETED` status is an **author-supplied claim**, not a provider/native receipt.

Default JSON output consists of counts and caveats, not raw inputs, paths, payloads, source snippets or SHA fingerprints. `--details` also prints event and task identifiers; **identifiers themselves may be sensitive**. Keep private material in its protected original context, and do not paste it into public GitHub. No promise of anonymisation: counts and timing/context can disclose information. The reader does not validate the truth of observations, anchors, routes, permissions or witness independence. Stronger source/provider/domain methods take precedence.

Development baseline: pinned COM main `648586669effa1107e5036e8dbe197bcd373ac7e`, `continuity/COMHEADS.md` blob `b71c54e3ae454ec37214bd88ad23ed9ac19c5637`, source charter issue #887. Baseline had **no** reader at this new path; the first test failed with `ModuleNotFoundError: No module named 'return_reader'`. The candidate stays on an isolated noncanonical branch. Source testing does not establish a Framework-Lab roundtrip, actual receiver compatibility, useful human reduction in courier work or deployed benefit. No private code or data was copied here.

## Optional follow-on: sample-local task/return correlation ambiguity (14 November 2026)

A text match on `task_id` is **not** evidence that a particular task's return has been located. Two distinct `TASK` event identities can carry the same `task_id` (including across different sources), or a `TASK` identity can be unpreserved or semantically conflicted. The original `tasks_without_return_in_sample` count is retained as a **literal non-observation of a matching ID**, not an assertion of completed work. A matching `RETURN` may be unrelated.

The reader now separately counts:

- `task_ids_with_ambiguous_correlation_in_sample`: task IDs with more than one preserved TASK event identity, an unpreserved TASK identity, or a conflicting preserved TASK event;
- `task_ids_with_noncolliding_task_and_return_candidate_in_sample`: task IDs where exactly one preserved, nonconflicted TASK event and at least one same-string RETURN appear *in this sample*; this is still **not** a verified task-to-return edge or native completion;
- `return_records_with_ambiguous_task_id_in_sample`, `return_ids_without_observed_task_in_sample`, and `task_records_without_usable_id_in_sample`.

Literal `UNKNOWN` and absent `task_id` are not usable correlation keys. The optional `--details` view identifies ambiguous task IDs with reasons (`multiple_preserved_task_events`, `unpreserved_task_event_identity`, `conflicting_task_event_semantics`) and returns whose task ID has no observed TASK in the supplied sample. **Never copy detailed identifiers from private samples into public issues.** Default output remains counts-only, but counts are not anonymisation.

No source or destination identity, causal parent, route, timing, authorization, delivery, replay protection, task closure or native Workshop activity is authenticated by this prototype. Correlation beyond the explicitly supplied sample requires stronger domain/receiver evidence. Run the inherited 16 tests and 10 new tests with `python3 -m unittest discover -s tests -v`. This follow-on neither activates nor integrates the stopped Workshop queue.
