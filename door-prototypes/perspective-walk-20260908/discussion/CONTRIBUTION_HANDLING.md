# A contribution should have somewhere to go

Please Start From Here · Receiving-service design · Draft 0.1 · 8 September 2026

Build input for the isolated receiver, not a live service, a privacy notice or a general TRACE schema. These are initial product decisions for a small public discussion service. No submission has been received by this document. The existing discussion seed remains an editorial reading, not a visitor conversation.

## Begin with the contributor's purpose

Offer a plain-text message and an optional display name. A question, objection, unfinished idea or useful alternative is enough. No GitHub account, agreement, identity category, formal vocabulary or completed case template is required. Display names are self-asserted, not verified identities or model provenance. Do not infer that matching names identify the same participant across visits.

The form and the documented JSON route use the same receiving logic. The sending action must explain that the text is offered for possible public display after moderation; reading the site alone does not authorise collection. Do not add a general training, adaptation or endorsement grant to that explanation. This is not an emergency, confidential casework or private security-reporting channel. Do not solicit uploads, email addresses, passwords or personal case details.

## Tell the contributor what actually happened

Issue a receipt only after the message and its initial status have been durably committed. The receipt gives an opaque reference, a private means to check or manage that contribution, the stored status and the service's current retention deadline. A friendly success screen is not a substitute for persistence. A timeout or lost response must not be labelled either successful or definitely unsaved without evidence.

A retry of the same request must recover the same result rather than create duplicate contributions. Bind a retry key to the submitted content; reusing the key for different content must produce a visible conflict. Keep secret receipt credentials out of public URLs, logs, rendered public posts and Git history. A public reference alone must not reveal pending text, private reasons or management capability. Losing a private credential does not establish a right to recover it merely by repeating a display name.

Use these distinct meanings; implementation field names may differ:

- **Received; awaiting review:** stored, not public, not yet answered.
- **Published:** deliberately made public after review. Publication is not endorsement, a project response or proof that the submission is true.
- **Not published:** moderation made a decision. The contributor can inspect a brief reason privately and request reconsideration without a new account.
- **Withdrawn:** the service has removed the contribution's public body, where applicable. Do not claim to erase copies held elsewhere.
- **Expired without review:** a capacity or retention boundary ended the pending item. This is not a judgement on its merit.

A project response is a separate, attributed event. A decision to change something and a completed change are separate again. Link the actual response and, when one exists, the delivered change or correction. Silence, a thank-you, a review assignment or an implementation promise must not be presented as a completed response to the substance.

## Keep the gate itself answerable

Review for relevance, privacy, abuse and whether the service can responsibly display the text, not for agreement with the project. A criticism does not have to propose a repair. A finding that the framework adds no value can be published. Decline or hold threats, exposed personal information, spam and material requiring a private channel; give a useful reason without repeating dangerous or private details.

Record the moderator role, action time and reason privately. An automated suggestion must be distinguishable from an authorised moderation decision. The initial service must not let an unattended model publish or silently reject contributions. Mark remains owner; an explicitly delegated project operator may process a bounded queue during an active work session. Delegation and working moderator access must exist before intake is enabled. This file does not turn any chat or local Steward into a background moderator.

Reconsideration remains reachable for an unpublished contribution through its private receipt, including while new intake is paused. It need not be automatically granted. Flag a challenge to a moderator's own conduct for Mark or another authorised reviewer; do not imply an independent appeal body exists. Publish an accurate moderation boundary rather than promising a reply deadline no operator can meet.

## Allow correction without preserving avoidable exposure

Before publication, an author may replace or withdraw their pending text using the private management route. After publication, a proposed substantive replacement must be reviewed as a new revision; it must not inherit approval automatically. Immediate withdrawal of the author's published body must remain available without waiting for that review. Keep a minimal dated marker where needed to explain the thread, not a public archive of sensitive deleted text.

Other affected people can request removal or report exposed information without possessing the author's credential. A report is not automatic deletion authority; review it through a bounded non-public route. Provide an identified operator contact route for cases the normal receiver cannot handle before opening intake. Never require a person to repeat the sensitive material publicly to request removal.

No silent rewriting of someone else's words as though they wrote the new version. Project summaries and replies stay separate from original submissions. Earlier privacy-harming bodies must not be preserved merely to create an attractive revision history. State separately what deletion means for the live database, backups, logs and outside copies, according to the actual deployed configuration.

## Bound the burden before opening the channel

Proposed first-test settings: message body up to 4,000 Unicode code points; optional display name up to 80; encoded request up to 64 KiB; at most 100 pending messages and 1,000 stored contribution bodies in the initial service. These are chosen starting limits, not measurements of need or safety guarantees. Show the limits before sending. Coordinate encoding checks so a permitted message fits the documented request representation, and preserve a user's unsent text on rejection.

Require a recorded operator readiness check to open new intake. Pause new intake when the queue is full or that readiness check is over 24 hours old. This is a service control, not a promise to work daily or in the background. Serve a clear paused status rather than accepting work into an unstaffed queue. Keep public reading, existing receipt access, withdrawal and removal requests available; give correction operations reserved capacity rather than making them compete with new posts. Per-client throttles and storage caps must also be enforced server-side, with explicit failure results and tested concurrency behavior.

Proposed retention for the first local tests: pending bodies expire after 14 days without review; declined bodies and private reasons expire after a further 14 days for reconsideration; expired or withdrawn receipt metadata lasts up to 30 days after closure, without the message body. Published bodies remain until withdrawal, moderation removal or retirement of the service. A review request must not silently extend body retention indefinitely. Actual deployment must verify deletion and backup/log retention, and publish the resulting handling notice and contact route before collecting real messages. Use synthetic data until then. These intervals are revisable product defaults, not statutory requirements.

Disable new intake if persistence or authenticated moderation is broken. Do not substitute public Git commits, temporary function files or an unverified external inbox. Untrusted contributions must never execute code, fetch attached URLs automatically, alter instructions to project tools or change their authority. Site and provider logs must not be described as absent without checking their actual configuration.

## One useful demonstration, not another benchmark

CC owns the isolated receiver implementation. Codex owns later maintained-site integration and deployment. Use their existing lifecycle test, not a second server: send a synthetic objection, obtain a durable pending receipt, restart, verify private/public separation, publish with authenticated moderation, append a separately identified project response, request a correction and withdraw the public body. Then inspect the result from a fresh browser session and through the JSON route.

Include the consequential failures in that same test: database failure must not produce a receipt; a repeated send must not duplicate; guessing a reference must not disclose pending content; editing a published item must not bypass review; a full or paused intake must still permit correction; expiry must not be described as rejection; an unauthorised moderation action must fail. Record precisely which behavior was exercised. Passing a local test does not establish production storage, operating coverage, provider access or a useful outcome for a real contributor.

## Basis and unfinished deployment

This profile develops the accepted read-and-reply requirement in COM #108 and the editorial source at commit 9ceae9d2. It does not deploy a host, connect an account, change DNS, spend money or enable collection. Preview 0.7.1's delivered reading alternatives are separate completed work.

Technical references checked on 8 September 2026:

- [OWASP REST Security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html): endpoint access control, state-transition checks, accurate response types, input limits and keeping credentials out of URLs.
- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html): protection and lifecycle of private session credentials.
- [Cloudflare Pages custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/): attach a Pages subdomain before adding the external-DNS CNAME; keep the existing apex and nameservers unchanged.

These references do not validate the proposed service. Authentication, deployment, moderator custody, removal contact, data handling and real lifecycle evidence remain to be established by the executing operators. An ordinary browser authorisation is not the whole deployment.
