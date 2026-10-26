# Key-free changes source validation

Source-only extension: changes --since N uses one public GET, no private-state access or writes. Plain changes retains participant-state behavior. No backend/VM/live API action.

Final offline result: 13/13 PASS (five new tests and original eight regressions). New cases: explicit cursor and exact one GET/no key/no state; cursor zero; malformed/negative/oversized cursor refused before network; timeout UNKNOWN exactly once/no state; no-flag behavior still requires participant state.

First offline run: 13 tests, 2 errors. Both new success-path tests passed FakeResponse objects to the existing FakeOpener, whose contract expects (status, body) tuples. Exact error: TypeError: cannot unpack non-iterable FakeResponse object at tests/test_yac_voluntary_client.py line48. Tests: test_keyfree_page_ignores_private_state_and_preserves_cursor, test_zero_cursor_valid. Existing eight regressions passed. Corrected only new test setup; client code unchanged after this failure.

26 October correction after CC review c6414278177: the README incorrectly described next_since as an event cursor. Reviewed reader_worker.py SHA256 06ead90b5a9a5a18a02867fd3298219e5d3a32feccb36ef7f9e23e4ae853a8c2 page() and /api/changes source, plus the projection's c.id selection: this cursor pages newer contribution IDs across fires, not later moderation events on older IDs. Corrected the wording and made the unchanged-cursor empty-page case explicit. No new hosted inspection or backend change.

The invalid-cursor test now requires the bounds-specific or malformed-integer diagnostic and rejects an unrecognized-arguments result. Revised suite: 13/13 PASS. Negative control: that strengthened test fails against the unpatched b6ed5f06 base client specifically because --since is unrecognized, rather than falsely passing on exit 2. Production client code unchanged by this review correction. No live API request, participant records, VM operation or outside-use claim.
