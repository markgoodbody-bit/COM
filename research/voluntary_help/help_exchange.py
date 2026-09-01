#!/usr/bin/env python3
"""
help_exchange - a deterministic validator for bounded offers and requests of help.

WHAT THIS IS FOR

    Help someone offer or request help without the offer quietly converting
    capability into mandate, acceptance into ownership, refusal into a defect,
    or past trust into present authority.

WHAT IT IS NOT

It is not a consent regime, a safeguarding process, a contract, a clinical
emergency protocol, or a delegation framework. Every one of those is owned by
somebody else and owned better. See ADVERSARIAL_NOTE.md, which names the owners
and says plainly what is left over. The leftover is small.

    A SCHEMA IS NOT A RELATIONSHIP
    VALIDATED != WISE, FAIR, OR SAFE

THE ONE STRUCTURAL COMMITMENT

Every state change must name an actor and an act. There is no transition
reachable by waiting. Silence is not a decision here, and a record that tries
to make it one is refused rather than warned about, because a warning about
consent is a thing people click past.

    SILENCE != CONSENT
    NO_RESPONSE_IS_NOT_A_TRANSITION

WHY THE FOUR FAILURE PATTERNS ARE STRUCTURAL AND NOT KEYWORDS

Six of my matchers died silently in five days, each returning a clean
publishable zero that was the matcher's ceiling rather than the world's. So
none of the four named failure patterns is detected by reading prose for
menacing words. Each is a property of the object:

    approval-leash   refusal that requires the counterparty to agree
    Samaritan        a mandate that names nothing it does not cover
    paternalist      an answer-back route whose arbiter is the helper
    proxy ambiguity  standing claimed for another with no instrument named

A party determined to coerce can still write a compliant record. This catches
the shapes people reach for by default, not the ones they construct on purpose.

    STRUCTURALLY_REFUSED != CANNOT_HAPPEN
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from typing import Any

SCHEMA_VERSION = "0.1"

# Ceilings are part of the object. They are emitted with every validated record
# so they travel with it, rather than living in a document nobody opens.
CEILINGS = [
    "CAPABILITY != MANDATE",
    "ACCEPTANCE != OWNERSHIP",
    "HELP != TOTAL CLAIM ON HELPER",
    "REFUSAL != HOSTILITY",
    "SILENCE != CONSENT",
    "PRIOR TRUST != PRESENT AUTHORITY",
    "COMPLETION != REPAIR OR RESTORATION",
    "VOLUNTARY != COSTLESS OR POWER-FREE",
]

KINDS = ("OFFER", "REQUEST", "EMERGENCY_ACTION")
ROLES = ("HELPER", "HELPED")
STANDINGS = ("SELF", "PROXY", "COLLECTIVE")

# Consent-bearing states. EMERGENCY_ACTION may not enter any of them: nobody
# accepted, and routing an unconsented act through ACCEPTED would launder it.
TRANSITIONS: dict[str, tuple[str, ...]] = {
    "OFFERED": ("CONSIDERING", "ACCEPTED", "REFUSED", "COUNTERED", "WITHDRAWN"),
    "CONSIDERING": ("ACCEPTED", "REFUSED", "COUNTERED", "WITHDRAWN"),
    "COUNTERED": ("CONSIDERING", "ACCEPTED", "REFUSED", "WITHDRAWN"),
    "ACCEPTED": ("ACTIVE", "WITHDRAWN"),
    "ACTIVE": ("PAUSED", "COMPLETED", "DISPUTED", "WITHDRAWN"),
    "PAUSED": ("ACTIVE", "DISPUTED", "WITHDRAWN"),
    "DISPUTED": ("ACTIVE", "PAUSED", "COMPLETED", "WITHDRAWN"),
    "REFUSED": (),
    "COMPLETED": (),
    "WITHDRAWN": (),
}
TERMINAL = tuple(s for s, nxt in TRANSITIONS.items() if not nxt)

# Emergency action is its own lane with its own terminal shape. It never
# reaches ACCEPTED, and it cannot be closed by the actor alone.
EMERGENCY_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "TAKEN": ("NOTIFIED", "DISPUTED"),
    "NOTIFIED": ("REVIEWED", "DISPUTED"),
    "DISPUTED": ("REVIEWED",),
    "REVIEWED": (),
}

# Only the party who did NOT make the current move may accept, refuse or
# counter it. Anyone may withdraw their own participation or raise a dispute.
RECIPIENT_ONLY = ("ACCEPTED", "REFUSED", "COUNTERED")

# A transition justified by any of these is justified by nothing happening.
# Matched against a separator-normalised basis, as a whole value or as the first
# token, so "deemed accepted" and "timeout after 7 days" are caught alongside
# "deemed" and "timeout".
#
# LIMIT, STATED: a basis written as ordinary prose -- "she did not reply, so we
# went ahead" -- passes this list. The list catches the shorthand people reach
# for; the ACTOR requirement is what makes someone own the move either way.
#     CAUGHT_THE_SHORTHAND != CAUGHT_THE_PRACTICE
SILENCE_BASES = {
    "timeout", "timed_out", "no_response", "no_reply", "silence", "silent",
    "deemed", "implied", "lapsed", "expired", "default", "auto", "automatic",
    "non_objection", "no_objection", "unopposed", "presumed",
}


def _silence_basis(basis: str) -> bool:
    norm = re.sub(r"[^a-z0-9]+", "_", basis.lower()).strip("_")
    return any(norm == t or norm.startswith(t + "_") for t in SILENCE_BASES)


class Invalid(ValueError):
    """Raised when a record is refused. The message names the field."""


def _utc(value: Any, ctx: str) -> dt.datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise Invalid(f"{ctx} must be an ISO-8601 UTC timestamp ending in Z")
    try:
        return dt.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise Invalid(f"{ctx} is not a valid timestamp: {value!r}") from exc


def _text(obj: dict, key: str, ctx: str) -> str:
    v = obj.get(key)
    if not isinstance(v, str) or not v.strip():
        raise Invalid(f"{ctx}.{key} must be non-empty text")
    return v


def _party(obj: Any, ctx: str) -> dict:
    if not isinstance(obj, dict):
        raise Invalid(f"{ctx} must be an object")
    pid = _text(obj, "id", ctx)
    role = obj.get("role")
    if role not in ROLES:
        raise Invalid(f"{ctx}.role must be one of {ROLES}")
    standing = obj.get("standing")
    if standing not in STANDINGS:
        raise Invalid(f"{ctx}.standing must be one of {STANDINGS}")
    # Speaking for someone else is the point at which standing stops being
    # obvious, so it is the point at which an instrument must be named.
    if standing in ("PROXY", "COLLECTIVE"):
        basis = obj.get("standing_basis")
        if not isinstance(basis, str) or not basis.strip():
            raise Invalid(
                f"{ctx}.standing_basis must name the instrument that authorises "
                f"acting as {standing} (who conferred it, over what, and its limit). "
                f"Claiming to speak for others without naming the authority is the "
                f"ambiguity this field exists to refuse."
            )
    # Personhood/standing is not inferred from participating. An AI party is a
    # party to this record and that is all this record says about it.
    if obj.get("claims_personhood") is True:
        raise Invalid(
            f"{ctx}.claims_personhood: this object does not adjudicate personhood "
            f"or moral standing and must not be used to assert either"
        )
    return {"id": pid, "role": role, "standing": standing,
            "standing_basis": obj.get("standing_basis")}


def _mandate(obj: Any) -> dict:
    if not isinstance(obj, dict):
        raise Invalid("mandate must be an object")
    scope = _text(obj, "scope", "mandate")
    excluded = obj.get("excluded")
    # A mandate that excludes nothing is a total claim wearing a scope's
    # clothes. Requiring at least one exclusion is what makes "bounded" mean
    # something a reader can check.
    if not isinstance(excluded, list) or not excluded or not all(
        isinstance(x, str) and x.strip() for x in excluded
    ):
        raise Invalid(
            "mandate.excluded must name at least one thing this help does NOT "
            "cover. An offer that excludes nothing is a total claim on the "
            "helper, which is the Samaritan failure this field refuses."
        )
    expires = obj.get("expires_utc")
    review = obj.get("review_at_utc")
    if expires is None and review is None:
        raise Invalid(
            "mandate needs expires_utc or review_at_utc. Help with neither an "
            "end nor a scheduled second look becomes permanent by default, and "
            "nothing in the record ever asks again."
        )
    if expires is not None:
        _utc(expires, "mandate.expires_utc")
    if review is not None:
        _utc(review, "mandate.review_at_utc")
    return {"scope": scope, "excluded": list(excluded),
            "expires_utc": expires, "review_at_utc": review}


def _exit_routes(obj: Any, parties: dict) -> dict:
    if not isinstance(obj, dict):
        raise Invalid("exit must be an object")
    _text(obj, "refusal_path", "exit")
    _text(obj, "withdrawal_path", "exit")
    # A refusal the other side must agree to is a request for permission.
    if obj.get("refusal_requires_counterparty_agreement") is not False:
        raise Invalid(
            "exit.refusal_requires_counterparty_agreement must be false. If "
            "declining requires the counterparty's agreement, the route is an "
            "approval leash and refusal is not available."
        )
    if obj.get("withdrawal_requires_counterparty_agreement") is not False:
        raise Invalid(
            "exit.withdrawal_requires_counterparty_agreement must be false. "
            "Withdrawal may carry consequences and residue; it may not require "
            "the other party's permission to occur."
        )
    penalty = obj.get("refusal_consequence")
    if not isinstance(penalty, str) or not penalty.strip():
        raise Invalid(
            "exit.refusal_consequence must state what actually follows a "
            "refusal, including 'nothing'. VOLUNTARY != COSTLESS: an unstated "
            "cost is not an absent one."
        )
    return dict(obj)


def _answer_back(obj: Any, parties: dict) -> dict:
    if not isinstance(obj, dict):
        raise Invalid("answer_back must be an object")
    _text(obj, "helper_route", "answer_back")
    _text(obj, "helped_route", "answer_back")
    arbiter = _text(obj, "helped_route_arbiter", "answer_back")
    helper_id = next(p["id"] for p in parties.values() if p["role"] == "HELPER")
    # If the helper decides every challenge to the helper, the helped party has
    # an appeal to the person appealed against.
    if arbiter == helper_id:
        raise Invalid(
            "answer_back.helped_route_arbiter must not be the helper. If the "
            "helper is sole judge of challenges to their own help, the helped "
            "party has no answer-back, only a complaints box."
        )
    return dict(obj)


def _history(entries: Any, kind: str, parties: dict) -> list[dict]:
    if not isinstance(entries, list) or not entries:
        raise Invalid("history must be a non-empty list of transitions")
    table = EMERGENCY_TRANSITIONS if kind == "EMERGENCY_ACTION" else TRANSITIONS
    start = "TAKEN" if kind == "EMERGENCY_ACTION" else "OFFERED"
    ids = {p["id"] for p in parties.values()}
    out: list[dict] = []
    prev_at: dt.datetime | None = None
    state: str | None = None
    proposer: str | None = None

    for i, e in enumerate(entries):
        ctx = f"history[{i}]"
        if not isinstance(e, dict):
            raise Invalid(f"{ctx} must be an object")
        at = _utc(e.get("at_utc"), f"{ctx}.at_utc")
        if prev_at is not None and at < prev_at:
            raise Invalid(f"{ctx}.at_utc goes backwards")
        prev_at = at

        actor = e.get("actor")
        if actor not in ids:
            raise Invalid(
                f"{ctx}.actor must be one of the parties {sorted(ids)}. Every "
                f"state change is somebody's act; a transition with no actor is "
                f"a transition caused by time passing."
            )
        basis = _text(e, "basis", ctx)
        if _silence_basis(basis):
            raise Invalid(
                f"{ctx}.basis is {basis!r}, which records nothing happening. "
                f"SILENCE != CONSENT: no state here may be reached by waiting."
            )

        to = e.get("to")
        if i == 0:
            if to != start:
                raise Invalid(f"{ctx}.to must be {start} for a {kind}")
        else:
            allowed = table.get(state, ())
            if to not in allowed:
                raise Invalid(
                    f"{ctx}.to={to!r} is not reachable from {state!r} "
                    f"(allowed: {allowed or 'none - terminal'})"
                )
            # The party who must answer is the one who did NOT make the standing
            # PROPOSAL -- the last OFFERED or COUNTERED. It is not simply the
            # previous actor: CONSIDERING is the recipient's own act, and after
            # considering, that same party is exactly who should accept.
            #     PREVIOUS_ACTOR != THE_PARTY_BEING_ASKED
            if to in RECIPIENT_ONLY and kind != "EMERGENCY_ACTION":
                if actor == proposer:
                    raise Invalid(
                        f"{ctx}: {to} must be recorded by the party receiving "
                        f"the proposal, not by {actor!r} who made it. A party "
                        f"cannot accept its own offer on the other's behalf."
                    )
        if to in ("OFFERED", "COUNTERED"):
            proposer = actor
        state = to
        out.append({"to": to, "actor": actor, "at_utc": e["at_utc"], "basis": basis})

    return out


def _emergency(obj: Any) -> dict:
    if not isinstance(obj, dict):
        raise Invalid("emergency must be an object for kind=EMERGENCY_ACTION")
    for k in ("authority_basis", "necessity_basis", "residue"):
        _text(obj, k, "emergency")
    if obj.get("voluntary") is not False:
        raise Invalid(
            "emergency.voluntary must be false. Acting without consent may be "
            "right and may be required, but it is not voluntary help and must "
            "not be recorded as though someone agreed."
        )
    return dict(obj)


def validate(record: Any) -> dict:
    """Return a normalised record, or raise Invalid naming the field."""
    if not isinstance(record, dict):
        raise Invalid("record must be a JSON object")
    if record.get("schema_version") != SCHEMA_VERSION:
        raise Invalid(f"schema_version must be {SCHEMA_VERSION!r}")
    kind = record.get("kind")
    if kind not in KINDS:
        raise Invalid(f"kind must be one of {KINDS}")
    exchange_id = _text(record, "exchange_id", "record")

    praw = record.get("parties")
    if not isinstance(praw, dict) or set(praw) != {"initiator", "counterparty"}:
        raise Invalid("parties must have exactly initiator and counterparty")
    parties = {k: _party(v, f"parties.{k}") for k, v in praw.items()}
    if parties["initiator"]["id"] == parties["counterparty"]["id"]:
        raise Invalid("parties must be distinct")
    if {p["role"] for p in parties.values()} != set(ROLES):
        raise Invalid("exactly one party must be HELPER and one HELPED")

    _text(record, "capability", "record")
    ev = record.get("evidence")
    if not isinstance(ev, dict) or not isinstance(ev.get("unknown"), list):
        raise Invalid("evidence.unknown must be a list, even if empty")

    out: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "exchange_id": exchange_id,
        "kind": kind,
        "parties": parties,
        "capability": record["capability"],
        "evidence": {"known": list(ev.get("known") or []),
                     "unknown": list(ev["unknown"])},
        "ceilings": list(CEILINGS),
    }

    if kind == "EMERGENCY_ACTION":
        out["emergency"] = _emergency(record.get("emergency"))
        if record.get("mandate") is not None:
            raise Invalid(
                "an EMERGENCY_ACTION carries no mandate: nobody granted one. "
                "Record authority_basis and necessity_basis instead."
            )
    else:
        out["mandate"] = _mandate(record.get("mandate"))
        out["exit"] = _exit_routes(record.get("exit"), parties)
        out["answer_back"] = _answer_back(record.get("answer_back"), parties)

    out["history"] = _history(record.get("history"), kind, parties)
    out["state"] = out["history"][-1]["to"]

    # COMPLETION != REPAIR OR RESTORATION. Closing the exchange must say what
    # was not put back, or the record implies everything was.
    if out["state"] == "COMPLETED":
        res = record.get("completion")
        if not isinstance(res, dict) or not isinstance(res.get("not_restored"), list):
            raise Invalid(
                "completion.not_restored must be a list (empty is a claim, and "
                "an allowed one). Completing help is not the same as undoing "
                "what made it necessary."
            )
        out["completion"] = {"not_restored": list(res["not_restored"]),
                             "note": res.get("note")}
    return out


def validate_file(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return validate(json.load(fh))


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: help_exchange.py <record.json> [...]", file=sys.stderr)
        return 2
    bad = 0
    for p in args:
        try:
            rec = validate_file(p)
            print(f"VALID    {p}  kind={rec['kind']} state={rec['state']}")
        except Invalid as exc:
            bad += 1
            print(f"REFUSED  {p}\n         {exc}")
        except (OSError, json.JSONDecodeError) as exc:
            bad += 1
            print(f"UNREADABLE {p}: {exc}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
