# Campfire Door public preview

Publishing branch only. COM `main` remains the coordination repository.

Preview 0.5, prepared 7 September 2026 from local source commit
`b7a2ab6563c7ad600a477a6b32078dcf6b6efe82`.
Authority and discussion: [COM #108](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5576230968).
The previous 0.3/0.4 comparison objects remain in [PR #110](https://github.com/markgoodbody-bit/COM/pull/110).

GitHub Pages serves this branch's root. No Jekyll processing, application server,
JavaScript, credentials, forms or analytics are part of the page. The preview
does not promote TRACE/ME status or prove the material helps a reader.

Intended `index.html`: 4,610 bytes, SHA-256
`31a8b68056bbdb533487bf3f52bc586461f91a7c25ea073e4a0e4a10b358e440`.
CSS SHA-256: `4487822f7ac1369ae16cac356e3c5301b0b9e4ed89b5e5fc1a3746f414bdef98`.
Served bytes must be checked separately after publishing.

## Update and rollback

The existing local source project is `campfire-door-preview`; use its normal
build, then copy only the three exported files into this checkout. Review and
commit the diff on this branch. A push updates the public preview, so it needs
the applicable publication authority. Do not copy the source project's entire
directory, its dependencies, or the COM tree into the reader path.

Keep exact build hashes in the update receipt. After GitHub reports a successful
build, verify the canonical HTTPS root and CSS with unauthenticated GETs. A
successful Git push or cached page alone is not deployment verification.

For a content rollback, revert the relevant publishing commit normally, push,
and verify the resulting public bytes. This first publication has no earlier
live version: withdrawing it means disabling Pages, not deleting COM or its
history. Disabling Pages also requires applicable authority. No automatic
rollback, public update or deletion is authorized by this README.
