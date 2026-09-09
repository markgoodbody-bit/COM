"""Non-actuating probes of CC's pinned 0d87ae2 transition fixture.

Usage: python -B evidence/supervisor_transition_review_20260909.py <fixture.py>
Only execute the inspected source at the recorded commit. This harness never
imports or runs the installed PowerShell supervisor or touches a live heartbeat.
"""
import contextlib
import hashlib
import importlib.util
import io
from pathlib import Path
import sys

sys.dont_write_bytecode = True


def main():
    source = Path(sys.argv[1])
    expected = "c305f72a4cc25f80cab7ff888ac2dee413b8302739f46b5951115e598670c258"
    if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
        raise SystemExit("Refusing source other than the inspected pinned fixture")
    spec = importlib.util.spec_from_file_location("reviewed_cc_fixture", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    print("Original pinned fixture:")
    assert module.main() == 0

    print("\nSame observation sequences at the recorded deployed 120s threshold:")
    module.STALE_AFTER = 120
    for name, premise, sequence, expected_installed, expected_candidate in module.CASES:
        actual = module.run(module.installed, sequence)
        print(name, actual, "DIFFERS_FROM_45S_TABLE" if actual != expected_installed else "same")

    # Main claims it refuses unestablished premises. It only checks nonempty
    # sequences, so changing all premises to known nonsense leaves its verdict.
    module.STALE_AFTER = 45
    cases = module.CASES
    module.CASES = [(name, "FALSE PREMISE: this case was independently observed on Mars",
                     sequence, want_i, want_c)
                    for name, premise, sequence, want_i, want_c in cases]
    with contextlib.redirect_stdout(io.StringIO()):
        result = module.main()
    module.CASES = cases
    print("\nFalse-premise labels accepted with exit", result)
    assert result == 0

    # run() discards the cause, so it cannot detect this diagnostic regression.
    def wrong_cause(obs, state, now):
        action, cause = module.candidate(obs, state, now)
        if cause == "HEARTBEAT_LOST":
            cause = "NO_HEARTBEAT_SINCE_START"
        return action, cause

    survivors = [name for name, premise, sequence, want_i, want_c in cases
                 if module.run(wrong_cause, sequence) != want_c]
    print("Wrong loss label caught by shipped CASES:", survivors)
    assert survivors == []

    # The policy has separate semantics that the coarse runner fails to retain.
    module.STALE_AFTER = 120
    state = module.fresh_state(0)
    assert module.candidate(module.HEALTHY, state, 0) == ("RUN", "")
    assert module.candidate(module.HEALTHY, state, 60) == ("RUN", "")
    assert module.candidate(module.TORN, state, 180) == ("RUN", "HEARTBEAT_UNREADABLE")
    assert module.candidate(module.TORN, state, 181) == ("RESTART", "HEARTBEAT_LOST")
    assert module.candidate(module.NEVER, module.fresh_state(181), 182) == ("RUN", "AWAITING_FIRST_HEARTBEAT")

    # A usable heartbeat arriving before escalation resets the loss clock.
    state = module.fresh_state(0)
    assert module.candidate(module.HEALTHY, state, 60) == ("RUN", "")
    assert module.candidate(module.TORN, state, 179) == ("RUN", "HEARTBEAT_UNREADABLE")
    assert module.candidate(module.HEALTHY, state, 180) == ("RUN", "")
    assert module.candidate(module.TORN, state, 300) == ("RUN", "HEARTBEAT_UNREADABLE")
    assert module.candidate(module.TORN, state, 301) == ("RESTART", "HEARTBEAT_LOST")

    # A heartbeat 100s old was readable at t=100. Loss then escalates 21s
    # after that usable read, not after 120s of observed unreadability.
    state = module.fresh_state(0)
    assert module.candidate(module.Obs(True, True, 100), state, 100) == ("RUN", "")
    old_basis_result = module.candidate(module.TORN, state, 121)
    print("\nReadable age100 at t100 then unreadable at t121:", old_basis_result)
    assert old_basis_result == ("RESTART", "HEARTBEAT_LOST")

    print("Narrow cause/reset/boundary checks passed. No live recovery measured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
