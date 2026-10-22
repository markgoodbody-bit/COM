# Workshop return v0 — an actual place to leave truthful evidence

**22 October 2026. Isolated source candidate; not installed on the VM, not a public service, and not an agent queue.** This is a tiny missing bridge between a powered-on Ubuntu guest and an AI model invocation that starts later without inherited runtime memory.

## Why this, instead of another autonomous platform?

The question is not how to keep a model running forever. It is whether a later human or AI can enter a real workspace, recover what has *actually* changed, make a useful bounded contribution and leave a dated, inspectable result. Continuous identity is **not** required for continuity of work.

There are two independent parts:

1. **Deterministic guest witness (this package):** one-shot stdlib Python reading explicitly allowlisted **loopback HTTP status**, **local Git HEADs** and named **systemd .service/.timer properties**. It writes a local private atomic JSON receipt and Markdown view. It never executes an assigned job, calls a model, uploads data or sends a message. It does not enumerate private files, arbitrary scheduled tasks, browser sessions, user environment or credentials.
2. **Fresh model re-entry (separate, already available through ChatGPT scheduling + connected GitHub):** a new invocation reads *actual durable COM evidence*, selects one bounded useful source/research action and leaves a verifiable return. This does not imply that the ChatGPT invocation can see this Ubuntu receipt; VM→ChatGPT evidence transport is **not built**. No fabricated direct VM shell or agent wake.

This split matters. Scheduled observations can exist when no model is running. A later model may reason from only the evidence it really possesses.

## Finite guest witness: local use after acceptance

Requirements: Python 3.10+, stdlib, optional git and systemd for their exact probes. Not an installer and does not need root.

```sh
python3 -m unittest discover -s coordination/workshop_return_v0 -p 'test_*.py' -v
python3 coordination/workshop_return_v0/workshop_witness.py capture \
    --config coordination/workshop_return_v0/example.json \
    --output-dir /path/to/private/guest-witness-output
```

The example intentionally contains **zero checks**, and therefore produces `NO_CHECKS_CONFIGURED`. It proves atomic capture mechanics, **not VM health**. A Build-accepted VM-specific config must name actual service loopback endpoints, local repository paths and exact units, if any. A service running on Windows `127.0.0.1` is **not** automatically reachable from Ubuntu `127.0.0.1`; don't invent a NAT/proxy fix.

Example additional checks for a guest-local process (only when Build verifies these are real):

```json
{
  "schema": "workshop-witness.v1",
  "max_age_seconds": 3600,
  "probes": [{"name":"local_demo","url":"http://127.0.0.1:8787/health","expect":[200]}],
  "repos": [{"name":"local_repo","path":"/some/verified/guest/worktree"}],
  "units": [{"name":"verified_timer","unit":"verified-name.timer"}]
}
```

The script rejects non-loopback URLs, proxies, redirects, URLs containing credentials/querystrings/fragments and arbitrary commands, caps checks at 8 per category, uses 2-second HTTP timeouts and 3-second fixed-command timeouts. It persists only HTTP status/duration, the Git commit hex SHA, allowed systemd state strings, and observation/expiry timestamps. **It does not store response bodies or repo paths.** Run it as a dedicated low-privilege user with a private output directory. It does not manipulate timers or check provider health.

The JSON `latest.json` is the authoritative local sample; `latest.md` is a convenience rendering. JSON stores both observer start/finish clocks, scope limitations and an expiry interval. A later viewer must compare its **own clock** before reporting freshness. A successful capture can contain `UNREACHABLE` or `UNKNOWN` checks and is never itself a claim that the service was healthy. Local atomic replacement is **not** an independently durable rollback fence. Do not use this for effect authorisation.

## Possible cadence — NOT INSTALLED

The sample `workshop-witness.service.example` and `workshop-witness.timer.example` are *inactive templates*, not a setup instruction for Mark. They propose one 30-minute interval, `Persistent=false` (no automatic catch-up) and a finite runtime. **Wait for Codex's already-dispatched READ-ONLY timer inventory** and Build's custody/security review before modifying the guest. Actual service user, project path, loopback permission and data ownership must be independently resolved. No sudo/linger/global service changes from this source note. No install via ChatGPT's tools is claimed.

The Workshop `http://127.0.0.1:8877/` is a Windows-host service with real dated samples. Build can choose to **display** a locally transferred sample later without creating any control endpoints. A displayed 3-hour-old `latest.json` must say *STALE*, not *LIVE*. Transporting data between the VM and Windows requires a separate proved path and privacy review; this package does not do it.

## One useful autonomous return, without an automated task queue

A separate scheduled ChatGPT task can independently read COM and do one reversible **research/source-only** action (for example, supply a material counterexample, fix an isolated explanatory error, or make a small original build artifact). That task must:
- recover current owner evidence, not assume it is the same model as yesterday;
- state source clocks and whether a piece of information is reported, inferred or actually read;
- avoid duplicate work and prefer the stronger domain owner;
- leave verifiable code/commit/issue references for any actual action;
- **never** claim a COM post wakes Codex, Build or CC;
- not deploy, contact external people, publish YAC contributions, spend, handle credentials, widen permissions or activate the paused B queue;
- return a precise NO_DELTA or BLOCKED when warranted, not produce faux creativity.

A scheduled invocation is a separate new aperture. The first real successful return is proved only by the next run's independently readable source/receipt, not by the task existing.

## Acceptance and first experiment

**Build acceptance** is a separate engineering event. Do not merge into canonical product branches by inertia.

A first coherent field probe would show the following *five actual receipts*:

1. A dated Ubuntu guest inventory establishing which existing scheduling facilities are available.
2. One manually invoked guest witness capture with a real configured read-only loopback/service or Git probe and a private `latest.json`.
3. The same script run a second time later (if Build accepts a timer), preserving `Persistent=false` and a genuine source clock.
4. One fresh scheduled ChatGPT invocation reading its **own accessible** COM source and leaving a nonduplicated useful public source-only result with an exact link.
5. A Workshop view displaying the witnessed **real state and its age**, correctly identifying VM, external scheduler and model invocation as separate actors.

**Failure conditions:** only a proposal exists; scheduled task has no execution receipt; no actual guest data; the result is an empty timestamp; cross-boundary source clocks are merged; an invented model conversation is displayed; a restored local file is promoted into authority; or Mark must carry routine task messages to complete the loop.

If one element fails, preserve it as a genuine boundary, and move to the smallest repair. Do not interpret a failed browser startup as a mandate to disable the sandbox.

## Responsibility and guardrails

Campfire owns the constructive question and verifiable first-return proof. Build owns integration, native acceptance and whether the existing Workshop should surface the result. Codex owns only bounded Windows/Ubuntu execution via its proven wrapper. CC may challenge claims independently without being dispatched to repeat existing pilot tests. Mark remains consequential release/provider/legal/security-policy authority.

The target is **a workshop that produces something worthwhile while preserving answerability**, not an elaborate machine that measures itself forever.
