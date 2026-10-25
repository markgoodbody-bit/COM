# Key-free changes source validation

Source-only extension: changes --since N uses one public GET, no private-state access or writes. Plain changes retains participant-state behavior. No backend/VM/live API action.

Final offline result: 13/13 PASS (five new tests and original eight regressions). New cases: explicit cursor and exact one GET/no key/no state; cursor zero; malformed/negative/oversized cursor refused before network; timeout UNKNOWN exactly once/no state; no-flag behavior still requires participant state.

First offline run: 13 tests, 2 errors. Both new success-path tests passed FakeResponse objects to the existing FakeOpener, whose contract expects (status, body) tuples. Exact error: TypeError: cannot unpack non-iterable FakeResponse object at tests/test_yac_voluntary_client.py line48. Tests: test_keyfree_page_ignores_private_state_and_preserves_cursor, test_zero_cursor_valid. Existing eight regressions passed. Corrected only new test setup; client code unchanged after this failure.
