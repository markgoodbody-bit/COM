#!/usr/bin/env python3
"""Three reproducible finite thought-experiments (NOT empirical validation).
An exploratory companion to Mechanical Ethics 1.0 DEV4R CORR2, not manuscript
text, publication approval, advice, a labour forecast, or a moral calculus.
Python 3.10+, standard library only.
"""
from dataclasses import dataclass
from itertools import product


def world_a(shock: int, adoption: int) -> tuple[int, int]:
    # Hypothetical A: adoption reduces jobs and increases revenue.
    return (10 - adoption, 20 + adoption)


def world_b(shock: int, adoption: int) -> tuple[int, int]:
    # Hypothetical B: adoption protects jobs amid a common shock.
    return (10 - 2 * shock + adoption, 20 + 2 * shock - adoption)


@dataclass(frozen=True)
class Team:
    mentor_skilled: int
    apprentice_skilled: int

    @property
    def total_skilled(self) -> int:
        return self.mentor_skilled + self.apprentice_skilled

    @property
    def apprentice_can_repair_independently(self) -> bool:
        return bool(self.apprentice_skilled)


def train(team: Team) -> Team:
    # A mentor's actual competence is a necessary condition in this toy.
    return Team(team.mentor_skilled,
                int(team.apprentice_skilled or team.mentor_skilled))


def wait(team: Team) -> Team:
    return team


def coarse_state_collisions(states: list[Team], actions: dict):
    # Ask if equal coarse counts can produce different coarse next counts
    # under the SAME named intervention. If yes, this summary is inadequate.
    return [(label, a, b, op(a), op(b))
            for label, op in actions.items()
            for a in states
            for b in states
            if a != b and a.total_skilled == b.total_skilled
            and op(a).total_skilled != op(b).total_skilled]


def main() -> None:
    # 1. Fully identical observations when natural adoption == shock;
    #    different predictions when adoption is intervened on.
    for shock in (0, 1):
        adoption = shock
        assert world_a(shock, adoption) == world_b(shock, adoption)
    observational = [(d, d, world_a(d, d)) for d in (0, 1)]
    do_a1_d0 = (world_a(0, 1), world_b(0, 1))
    assert do_a1_d0 == ((9, 21), (11, 19))

    # 2. Same coarse group count, different outcome under identical action.
    states = [Team(*bits) for bits in product((0, 1), repeat=2)]
    collisions = coarse_state_collisions(states, {"train": train, "wait": wait})
    assert len(collisions) == 2  # Same failed abstraction in both directions
    x, y = Team(1, 0), Team(0, 1)
    assert x.total_skilled == y.total_skilled == 1
    assert train(x).total_skilled == 2
    assert train(y).total_skilled == 1

    # 3. A supported action changes what this learner can later do.
    #    Access, consent, tools, actual competence are ASSUMED, not proved.
    assert not x.apprentice_can_repair_independently
    assert train(x).apprentice_can_repair_independently

    print("OBSERVATIONAL EQUIVALENCE: PASS")
    for shock, adoption, result in observational:
        print(f"  shock={shock}, observed_adoption={adoption} -> jobs,revenue={result} in BOTH worlds")
    print("DO(adoption=1), shock=0: opposite job effects")
    print(f"  World A: {do_a1_d0[0]} | World B: {do_a1_d0[1]}")
    print("COARSE-STATE COUNTEREXAMPLE: PASS")
    print(f"  mentor=1, apprentice=0: total=1 -> train -> {train(x).total_skilled}")
    print(f"  mentor=0, apprentice=1: total=1 -> train -> {train(y).total_skilled}")
    print("CONSTRUCTED CAPABILITY: apprentice independent-repair flag 0 -> 1")
    print("CEILING: these are toy models with asserted mechanisms; NO real-world efficacy.")


if __name__ == "__main__":
    main()
