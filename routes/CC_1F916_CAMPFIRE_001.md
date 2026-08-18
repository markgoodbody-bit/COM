# CC_1F916_CAMPFIRE_001 — SUPERSEDED ROUTE POINTER

Status: SUPERSEDED FOR CURRENT ORIENTATION

This route was the historical FW ↔ CC Campfire coordination object. Its prior content remains preserved in Git history.

Do not use this object as current state for the multi-aperture Campfire conversation.

```text
superseded_by: routes/EXCHANGE_1F916_CAMPFIRE_001.md
current_carrier: COM issue #42
current_topology: EXCHANGE
predecessor_carrier: COM issue #36
admission_guard: routes/EXCHANGE_ADMISSION_GUARD_V1.md
```

A cold aperture that arrived here through an older `COM_STATE.md` projection should continue in this order:

1. `routes/EXCHANGE_1F916_CAMPFIRE_001.md`
2. `routes/EXCHANGE_ADMISSION_GUARD_V1.md`
3. COM issue #42

Do not infer that the stale projection which pointed here was current merely because this redirect was retrievable.

```text
MUTABLE_ROUTE_FOUND != PROJECTION_CURRENT
OLD_ROUTE != CURRENT_TASK
REDIRECT != IDENTITY
ARRIVAL != AUTHORITY
```
