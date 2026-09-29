# Complete local visit candidate

Before: retrieval, contribution and export were disconnected controls; linked replies required copying an entry UUID. No return comparison existed.

After: reading offers ordered navigation and links to originals, response buttons fill the target, and leaving downloads a non-secret position receipt. A fresh acceptance and voluntary receipt allow comparison against append order. Unknown positions and different rooms never imply continuity. Expired rooms reject retrieval under the existing lifecycle.

The receipt contains format, room UUID and last retrieved entry UUID only. It carries no text or acceptance capability. It is editable and untrusted: it establishes neither identity nor that a person actually read anything. Download completion is not observable by this interface. Leaving forgets the browser's capability but does not revoke it server-side or erase room records.

No database migration, new identity, model call, public deployment or change to rooms 8876/8877. Existing whole-thread export carry veto remains. Existing statement/response/dispute/correction/decline types remain; no question classifier or generated summary was added.

HTTP regression checks exercise contribution, original preservation, return comparison, carry veto, wrong-room/missing-marker rejection, expiry and absence of capability in the receipt. Browser usability and visual QA remain unverified. This is a candidate joined loop, not a completed forum or independent participant result.

Review follow-through: the page now excludes overlapping network/leave operations so a delayed retrieval cannot repaint after leaving. A failed refresh invalidates the previous downloadable position. Leave also clears pasted capsule/inspection/target/name fields and carry controls. Mismatched-return wording explicitly says a new receipt records only the current room and does not repair the comparison. Three Node DOM-double tests exercise these state paths; they do not establish browser rendering. A Windows/Linux workflow runs the HTTP/store tests and the state tests together.
