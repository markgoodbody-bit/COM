"""Check two finite illustrations, not empirical claims about people.

Run: python coordination/successor_beta_20260923/check_examples.py
Standard library only; no network, input files, output files, or random sampling.
"""

from fractions import Fraction


def access_state(events):
    """Stipulated transitions; counters are events, not units of suffering."""
    access, blocks, benefits = True, 0, 0
    for event in events:
        if event == "block":
            access, blocks = False, blocks + 1
        elif event == "restore":
            access = True
        elif event == "benefit":
            benefits += 1
        else:
            raise ValueError(f"Unknown fixture event: {event}")
    return access, blocks, benefits


def require(condition, message):
    # Unlike assert, these checks remain active under python -O.
    if not condition:
        raise RuntimeError(message)


def main():
    sequences = (
        (("block", "restore"), (True, 1, 0)),
        (("restore", "block"), (False, 1, 0)),
        (("block", "benefit"), (False, 1, 1)),
    )
    for events, expected in sequences:
        actual = access_state(events)
        require(actual == expected, f"Access fixture mismatch: {events}")
        print(f"{', '.join(events)}: access/blocks/benefits = {actual}")
    require(
        sorted(sequences[0][0]) == sorted(sequences[1][0]),
        "The order comparison must use identical event counts",
    )
    require(access_state(()) == (True, 0, 0), "Initial state changed")
    try:
        access_state(("unrecognised",))
    except ValueError:
        pass
    else:
        raise RuntimeError("Unknown event was silently accepted")

    # Hidden state is uniformly 0 or 1. Success means choosing its value.
    # Uninformed policies cannot condition their choice on that hidden state.
    states = (0, 1)
    actions = (0, 1)
    possible = any(a == w for a in actions for w in states)
    statewise = all(any(a == w for a in actions) for w in states)
    robust_uninformed = any(all(a == w for w in states) for a in actions)
    best_uninformed = max(
        sum((Fraction(int(a == w), 2) for w in states), Fraction(0))
        for a in actions
    )
    informed_policy = {0: 0, 1: 1}  # Requires an accurate observation before acting.
    informed = sum(
        (Fraction(int(informed_policy[w] == w), 2) for w in states), Fraction(0)
    )
    require(possible and statewise, "Existential witness missing")
    require(not robust_uninformed, "Information constraint was lost")
    require(best_uninformed == Fraction(1, 2), "Uninformed probability mismatch")
    require(informed == 1, "Informed policy mismatch")
    print(f"Possible={possible}; statewise={statewise}; robust uninformed={robust_uninformed}")
    print(f"Best uninformed success={best_uninformed}; informed matching success={informed}")
    print("PASS: stipulated finite examples only; no empirical validation.")


if __name__ == "__main__":
    main()
