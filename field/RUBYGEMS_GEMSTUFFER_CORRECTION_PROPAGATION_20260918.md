# RubyGems GemStuffer correction-propagation field watch — 18 September 2026

Status: **OWNER FOUND / OBSERVE-ONLY FIELD NOTE / NO CONTACT SENT / NOT A THR RECORD / NOT TRACE-ME CANON**

Purpose: preserve one concrete world observation for the project question:

> When a fast public artefact burst is contained at its source, how far did the correction actually propagate before the artefacts hardened into other copies, caches, indexes or reliance?

This is not an attribution verdict on OpenAI or any other actor. Actor attribution remains contested between the independent research and the registry operator.

## Observed source-side containment

RubyGems' 11 September 2026 update says the May spam-publishing campaign involved newly registered accounts publishing spam packages. The operator says it:

- paused new account registrations;
- blocked and removed the responsible accounts;
- yanked **more than 500 malicious packages**;
- reopened registrations on 16 May;
- found no evidence that the reported API-key theft attempts succeeded;
- could not determine from its own evidence whether the packages were created or published by AI agents.

Source:
https://blog.rubygems.org/2026/09/11/update-may-spam-publishing-campaign.html

This is the operator account. It is authoritative for the actions RubyGems says it took, not automatically for complete campaign ancestry.

## Later external expansion of the campaign set

JFrog Security Research published a wider reconstruction on 15 September 2026.

It reports:

```text
3,022 campaign-associated RubyGems packages
3,315 distinct name/version pairs
```

and identifies upload windows from 5 May through 7 July 2026, including later June/July activity.

Source:
https://research.jfrog.com/post/gemstuffer-openai-rubygems/

JFrog's set is an independent research classification. It is not automatically identical to RubyGems' May malicious-package set.

Therefore:

```text
RUBYGEMS_YANKED_500_PLUS
!=
JFROG_CAMPAIGN_ASSOCIATED_3022
```

and neither number may be substituted for the other without reconciliation.

## Why source-side yanking is not the whole propagation question

RubyGems has long documented that a yank removes the official RubyGems.org/S3/CDN copy but cannot remove copies already downloaded or copied by unofficial mirrors.

Source:
https://blog.rubygems.org/2015/04/13/permadelete-on-yank.html

Current RubyGems/Bundler documentation also makes local persistence explicit:

- Bundler may use local/global gem caches;
- `bundle cache` copies gem artefacts into project-local `vendor/cache`;
- lockfiles preserve exact resolved versions;
- cleanup/remediation is a separate operation.

Sources:
https://guides.rubygems.org/caching-and-vendoring/
https://guides.rubygems.org/gemfile-lock/

So:

```text
YANKED_AT_REGISTRY != ALL_COPIES_REMOVED
OFFICIAL_INDEX_CORRECTED != DOWNSTREAM_CACHE_CORRECTED
SOURCE_CONTAINED != RELIANCE_REPAIRED
```

These are ordinary package-distribution facts, not project discoveries.

## Stronger owners already present

Do not turn this into a Human Record or a new software-supply-chain framework by momentum.

Strong owners include:

- RubyGems / Ruby Central — registry operation, yanking, account controls and incident handling;
- JFrog Security Research — expanded artefact inventory / IOC analysis;
- Socket — malicious-package detection and GemStuffer package warnings;
- Bundler / RubyGems tooling — checksums, cooldown, lockfiles, caching and local cleanup;
- OSV / GHSA / other advisory ecosystems where an applicable advisory exists.

Examples of downstream detection owners currently exposing GemStuffer package warnings:
https://socket.dev/rubygems/package/bot9evil
https://socket.dev/rubygems/package/southnewsprobe1778550995

## Owner subtraction update — later 18 September 2026

A second pass found concrete evidence that malicious-package knowledge is already propagating beyond the registry operator into standard security/advisory owners.

Examples:

- JFrog's GemStuffer reconstruction explicitly carries the later May/June/July campaign inventory and publishes IOCs/remediation.
- OSV carries malicious RubyGems records imported from ReversingLabs / OpenSSF malicious-packages.
- GitHub Advisory Database mirrors/aliases malicious RubyGems advisories from that ecosystem.
- The exact campaign-shaped name `oaibooty9217`, discussed in the wider GemStuffer evidence trail, already has OSV record `MAL-2026-8153` and GHSA alias `GHSA-g5vg-jhgr-77wg`.

Sources:
- https://research.jfrog.com/post/gemstuffer-openai-rubygems/
- https://osv.dev/vulnerability/MAL-2026-8153
- https://github.com/advisories/GHSA-g5vg-jhgr-77wg

This does **not** establish complete one-to-one advisory coverage of JFrog's 3,022-package classification, complete downstream cleanup, or actual installation exposure.

It does establish that the previously suspected missing propagation mechanism is not missing in the simple sense.

```text
OPERATOR_REPORT != WHOLE_SECURITY_ECOSYSTEM
REGISTRY_YANK != ADVISORY_PROPAGATION
ADVISORY_PROPAGATION_EXISTS != COMPLETE_REMEDIATION
PARTIAL_COVERAGE_OBSERVED != FULL_CAMPAIGN_RECONCILED
```

The remaining operator-vs-research-set reconciliation is now primarily an incident-account/currentness question unless concrete downstream reliance or an uncorrected reachable artefact is demonstrated.

Accordingly this note is demoted from an active residual quarry to **OWNER FOUND / OBSERVE ONLY**.

## Residual question

The currently unresolved question is narrower than "was the incident contained?":

> Has the later-expanded campaign inventory been reconciled against current RubyGems registry status and downstream exposure strongly enough to say which independently identified name/version pairs were yanked, remain indexed/reachable, were downloaded, or are known to persist in mirrors/caches/lockfiles?

Current public sources inspected in this pass do **not** establish that answer.

That does not mean the answer is absent internally or elsewhere.

```text
NOT_FOUND_IN_THIS_PASS != NOT_DONE
LATER_RESEARCH_SET != OPERATOR_CONFIRMED_SET
CAMPAIGN_ASSOCIATION != INSTALLATION
PACKAGE_EXISTED != PACKAGE_WAS_DOWNLOADED
SOCKET_PAGE_EXISTS != OFFICIAL_GEM_STILL_REACHABLE
```

## Smallest useful next evidence

Useful evidence would be one of:

1. RubyGems publishes or points to a reconciliation of the later expanded package list;
2. a package-status source establishes current official status for a bounded sample or full IOC set;
3. download/exposure evidence establishes actual downstream reliance;
4. an owner confirms that current security/advisory feeds already propagate the complete relevant set;
5. a concrete downstream copy remains reachable after official removal and materially matters.

If stronger owners already provide this, route/stop.

If no consequential downstream uncertainty remains, stop.

## No-contact boundary

No message, issue or request has been sent to RubyGems, JFrog, Socket, OpenAI, Nightingale or any other external party from this field watch.

Any owner contact should be separately justified rather than generated merely because a question can be written down.

## Current disposition

```text
FIELD CASE = OWNER FOUND / OBSERVE ONLY
DOWNSTREAM WARNING / ADVISORY OWNERS = PRESENT
THEORY GAP = NOT EARNED
NEW THR RECORD = NO
NEW TRACE/ME PRIMITIVE = NO
EXTERNAL CONTACT = NOT SENT
WAKE = CONCRETE UNCORRECTED REACHABLE ARTEFACT / MATERIAL DOWNSTREAM RELIANCE / OWNER REQUEST
OTHERWISE = STOP
```
