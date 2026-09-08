# Receiver operator path — evaluation only

Status: **EVALUATION / NOT PUBLIC INTAKE / NOT A STAFFING PROMISE**

This path exists so an authorised operator can inspect and act on the receiver without becoming a database administrator. It does not create an unattended moderator, background duty, independent appeal body or permission to open intake.

The CLI sends only to `/api/admin`. The moderator secret is read from `PSFH_ADMIN_TOKEN` and is carried in the HTTP `Authorization` header; it is not accepted in the URL or command arguments. Remote operator URLs must use HTTPS; plain HTTP is accepted only for loopback evaluation.

Set the receiver origin separately:

```sh
export PSFH_OPERATOR_URL=https://receiver.example/
export PSFH_ADMIN_TOKEN='...private value...'
```

Do not put either secret into Git, screenshots, shell history examples, public logs or issue comments.

## Read-only queue

```sh
npm run operator -- queue
```

## Open or pause new intake

```sh
npm run operator -- ready
npm run operator -- pause
```

`ready` is still bounded by the service readiness expiry. It is not permission to open real intake before the project handling notice, removal route, operator custody and provider failure behavior are complete.

## Publish or decline an exact reviewed revision

Decision text is supplied on stdin so it need not appear in the process argument list:

```sh
printf '%s' '{"id":"...","revision":2,"reason":"..."}' | npm run operator -- publish
printf '%s' '{"id":"...","revision":2,"reason":"..."}' | npm run operator -- decline
```

A publication decision is not a project endorsement or response. A decline reason should describe the moderation boundary actually used; disagreement with the project is not itself a reason to suppress a contribution.

## Add a separate project response

```sh
printf '%s' '{"id":"...","revision":2,"body":"..."}' | npm run operator -- respond
```

The receiver keeps this event distinct from publication and from any later project change.

## Current limits

This utility does not yet provide affected-person removal handling, operator-contact escalation, retained-event cleanup, or browser moderation UI. Those remain production blockers. It also does not establish that a configured deployment is safe merely because its API answers.

The source test covers secret placement, HTTPS/loopback destination rules, stdin decisions and error handling. Framework executed those five tests on Node 22.16 before committing the files; the full receiver suite must still be rerun against this branch and the D1 evaluation path before any deployment consequence.
