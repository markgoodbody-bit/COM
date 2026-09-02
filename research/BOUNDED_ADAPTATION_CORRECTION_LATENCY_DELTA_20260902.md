# Bounded Adaptation — correction-latency external-owner delta

Status: RESEARCH NOTE / EXTERNAL-OWNER INPUT / NOT CANON  
Date: 2026-09-02  
Purpose: test whether current agent authorization/task protocols make correction reachable quickly enough once an adaptive ecology has delegated or started work.

## Sources checked

- Agent2Agent Protocol v0.2.6 `tasks/cancel` and task lifecycle.  
  https://a2a-protocol.org/v0.2.6/specification/
- Model Context Protocol 2026-07-28 Tasks/MRTR lifecycle material.  
  https://blog.modelcontextprotocol.io/posts/2026-07-28/
- OAuth 2.0 Token Revocation, RFC 7009.  
  https://www.rfc-editor.org/info/rfc7009/
- OAuth 2.0 Token Introspection, RFC 7662.  
  https://www.rfc-editor.org/info/rfc7662/

## Finding

Current external owners provide several useful correction mechanisms, but they do not collapse into one thing.

### 1. Task cancellation is an attempt, not a guarantee

A2A `tasks/cancel` asks a server to cancel an ongoing task. The specification explicitly states that success is not guaranteed: the task may already be terminal, cancellation may not be supported at the current stage, or work may already have progressed beyond a cancellable boundary.

```text
CANCEL_REQUESTED != TASK_CANCELED
TASK_CANCELED != DOWNSTREAM_EFFECT_REVERSED
```

A robust adaptive ecology therefore cannot report "correction complete" merely because it emitted a cancel call.

### 2. Revoking authority is different from canceling work

OAuth RFC 7009 defines a token-revocation mechanism. Revoking a credential/grant constrains future authorized use, but it does not inherently unwind a task that already consumed the authority or a downstream side effect already initiated.

```text
AUTHORITY_REVOKED != IN_FLIGHT_WORK_STOPPED
AUTHORITY_REVOKED != CONSEQUENCE_REPAIRED
```

This is directly relevant to any future Framework/Steward/A2A delegation path.

### 3. Currentness of authority has its own clock

RFC 7662 token introspection allows a protected resource to ask whether a token is currently active and what authorization context/scopes it carries. The RFC explicitly notes a security/performance tradeoff when introspection results are cached: longer caching reduces traffic but increases the window in which revoked authority may still be treated as active.

Therefore the correction route contains a propagation/currentness clock:

```text
REVOKED_AT_AUTH_SERVER != KNOWN_REVOKED_AT_RESOURCE
```

The practical correction window depends on how often enforcement points revalidate authority and whether they use short-lived/continuously checked grants.

### 4. Protocol control points help before irreversible action

MCP 2026-07-28 introduces/reshapes control points useful for bounded agent work:

- Multi Round-Trip Requests can return `input_required` when a tool needs confirmation or missing input before continuing;
- the Tasks extension exposes explicit task handles and task lifecycle operations such as get/update/cancel.

These are useful answer-back/correction apertures, but they only help where the application places them before the consequential boundary.

```text
CONTROL_POINT_EXISTS != CONTROL_POINT_PRECEDES_HARDENING
```

## Structural consequence

For future adaptive multi-agent execution, correction has at least four distinct operations/clocks:

1. **decision correction** — decide that the prior plan/authority should change;
2. **authority revocation** — prevent further authorized use;
3. **execution cancellation/containment** — stop in-flight work where still possible;
4. **effect repair/residue handling** — address consequences already produced.

A useful timing sketch is:

```text
T_detect
+ T_route
+ T_revoke
+ T_propagate
+ T_cancel_or_contain
< T_irreversible_effect
```

This is a research expression, not a new TRACE primitive or universal law. Different systems may lack one or more terms or may have parallel rather than serial paths.

## Consequence for PR #87

A future executable adaptation cycle should not use one Boolean such as `revoked=true` or `cancelled=true` as proof of correction.

Where external actuation is eventually permitted, the adaptive record should distinguish at least:

```text
authority_state: ACTIVE | REVOKE_REQUESTED | REVOKED | UNKNOWN
execution_state: NOT_STARTED | IN_FLIGHT | CANCEL_REQUESTED | CANCELED | TERMINAL | UNKNOWN
effect_state: NONE_OBSERVED | REVERSIBLE | HARDENING | IRREVERSIBLE | UNKNOWN
correction_route_state: OPEN | DEGRADED | CLOSED | UNKNOWN
```

These states belong at the coordination/integration layer only when the underlying external owner can evidence them. Do not manufacture state precision that the actual protocol/service does not provide.

## Design pressure for future autonomy

If the ecology is to adapt without Mark while remaining answerable:

- authority grants should be as short-lived, destination-bound and scope-narrow as practical;
- downstream delegation should narrow authority rather than widen it;
- high-consequence actions should place confirmation/correction points before hardening where feasible;
- enforcement points should revalidate authority often enough for the relevant stakes and clocks;
- cancellation and revocation outcomes must be witnessed, not inferred from request submission;
- already-produced residue must remain visible after authority or execution is stopped.

This supports the existing project distinction:

```text
CORRECTION != RESTORATION
ROUTE_EXISTS != ROUTE_USABLE_IN_TIME
```

and adds a practical external-owner warning:

```text
REVOKE_ROUTE_EXISTS != REVOKE_PROPAGATES_IN_TIME
CANCEL_ROUTE_EXISTS != ACTION_STOPS_IN_TIME
```

## Earned move

`ROUTE_EXTERNAL_OWNER -> KEEP / INTEGRATE AS CONSTRAINT`.

Do not build a proprietary revocation protocol. Use established OAuth/A2A/MCP mechanisms where applicable, but require the adaptive layer to track their observable timing and outcome ceilings rather than treating protocol support as guaranteed correction.
