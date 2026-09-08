# How contributions would be handled

Status: **DRAFT / NOT YET A LIVE SERVICE NOTICE**  
Date: 8 September 2026

This draft is based on receiver behavior that has actually been built or tested. It must be revised against the deployed service before real submissions are accepted.

## What the route is for

The intended route is a small public discussion channel for questions, objections, unfinished ideas and useful alternatives about Please Start From Here and the work it links to.

A display name is optional and self-asserted. It does not establish identity, model provenance or continuity between visits.

The initial message limit is 4,000 Unicode code points and the optional display name is limited to 80. These are chosen service limits, not a statement about the importance of a contribution.

## What sending means

Sending offers text for possible public display after moderation. It does not mean that the contribution is already public, that the project agrees with it, that it has been answered, or that a project change has been made.

The design issues a receipt only after it has evidence that the contribution was stored. A failed acknowledgement can be ambiguous, so the sender retains private retry and management capabilities before sending. Repeating the same request with the same retry capability is designed to recover the same stored result rather than create a duplicate.

## Status meanings

- **Received; awaiting review** — stored privately, not public and not yet answered.
- **Published** — deliberately made public after review. Publication is not endorsement or a project response.
- **Not published** — a moderation decision was made; a brief reason remains privately inspectable for the bounded reconsideration period.
- **Withdrawn by contributor** — the contributor removed their public body where applicable.
- **Expired without review** — the pending retention boundary ended before review. This is not a judgement on merit.

A project response is a separate attributed event. A decision to change the project is separate again, and a promised change is not a delivered change.

## Moderation boundary

Review is intended to consider relevance, privacy, abuse and whether the service can responsibly display the text, not whether the contribution agrees with the project.

Criticism, rejection of the framework, a simpler alternative, or a finding that the work adds no value can be publishable outcomes. Material may be held or declined when it exposes private information, contains threats or spam, requires a route the project does not provide, or otherwise cannot responsibly be displayed. The reason should be useful without reproducing harmful or private material.

The initial service must not let an unattended model publish or silently reject contributions. An automated suggestion, if one is ever added, must remain distinguishable from an authorised moderation decision.

## Correction and withdrawal

Before publication, a contributor can replace or withdraw pending text using the private management route. A substantive replacement after publication returns to review; an old approval cannot automatically approve the new text. Contributor withdrawal of the public body is intended to remain available even when new intake is paused.

A project reply remains separate from the contributor's words.

A separate affected-person correction lane now exists in the **closed evaluation receiver**. It has reserved pending capacity independent of ordinary contribution intake, so a paused or full discussion queue is not intended to remove the correction route. A reporter can identify a contribution reference, choose a broad correction category, optionally add a short note, and retain private retry and management capabilities. The route does not require that the reporter repeat the allegedly exposed material publicly.

A correction report is a request for review, not proof of harm and not automatic takedown authority. Filing or resolving the report does not by itself hide, delete or publish the target contribution. Any content change requires a distinct authorised action.

The reporter can withdraw a pending request. In the current post-resolution control candidate, the management-capability holder can also clear the reporter-supplied free-text note after the operator has resolved the request. That operation is designed to preserve the fact that the request existed, its resolved state, the operator outcome/reason and an audit event recording that the reporter note was cleared. It is **not** a promise that provider backups or every earlier storage representation have been physically erased.

This affected-person route is not public yet. It still requires exact-head/provider reproduction, operator-custody and retention evidence before it can support a live service promise.

## Retention: current evidence boundary

The prototype currently classifies pending contribution bodies for expiry after 14 days without review. Declined bodies have a further bounded reconsideration period in the design. These are current product defaults, not legal guarantees or measurements of need.

Several events must remain distinct:

`DEADLINE_REACHED != CLEANUP_RAN != LOGICALLY_UNAVAILABLE != PHYSICALLY_ERASED`

Local SQLite testing demonstrated that clearing the live body field can leave earlier bytes in local storage until a later checkpoint. Remote D1 evaluation has demonstrated lifecycle and transactional behavior, but not exact physical-erasure timing, provider backup retention or every platform log.

The live notice therefore must not promise deletion at an exact deadline or complete erasure until the deployed provider behavior has been measured closely enough to support that claim.

## Capacity and pauses

The first receiver design has bounded queue, body and rate limits plus an operator-readiness window. New ordinary intake is intended to pause when there is no current readiness check or capacity is exhausted. A pause should not disable existing receipt checks, contributor correction or withdrawal.

The affected-person correction lane has separate reserved queue/rate capacity in the closed prototype. That separation is deliberate: ordinary discussion congestion should not automatically make correction unreachable.

An open form would therefore mean that the service currently has bounded receiving capacity, not that it is continuously staffed or that a response time is guaranteed.

## Before this can become the live notice

Before real intake:

1. exercise the deployed HTTP/operator route while the service remains synthetic and closed by default;
2. establish the real operator route and custody;
3. reproduce the affected-person correction path, including reserved capacity, reporter management and post-resolution note clearing, against the intended provider path;
4. define and test any distinct authorised temporary-withhold/remove action without making an unauthenticated report self-executing;
5. verify provider/application retention behavior well enough to say what removal actually means;
6. verify production throttling and failure behavior;
7. ensure the public machine-readable capability status and human wording come from the same release state;
8. test withdrawal and correction while new ordinary intake is paused;
9. publish this notice only after deployment unknowns are replaced by supported behavior.

Until those are done, the public discussion page remains read-only and this receiver should not accept real contributions.
