#!/usr/bin/env python3
"""Tests for help_exchange. Ten scenarios, six valid and four refused.

Every refusal test asserts on the FIELD that refuses, not on a substring of the
prose, so rewording a message does not silently turn a test into a tautology.
"""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import help_exchange as hx  # noqa: E402

HELPER = {"id": "kit", "role": "HELPER", "standing": "SELF"}
HELPED = {"id": "ada", "role": "HELPED", "standing": "SELF"}


def base_offer() -> dict:
    return {
        "schema_version": hx.SCHEMA_VERSION,
        "exchange_id": "hx-001",
        "kind": "OFFER",
        "parties": {"initiator": copy.deepcopy(HELPER),
                    "counterparty": copy.deepcopy(HELPED)},
        "capability": "Read a draft grant application and mark unclear passages.",
        "evidence": {"known": ["deadline is the 14th"],
                     "unknown": ["whether the funder allows resubmission"]},
        "mandate": {
            "scope": "comment on clarity of the draft text",
            "excluded": ["contacting the funder", "changing the budget",
                         "speaking for ada anywhere"],
            "expires_utc": "2026-09-14T17:00:00Z",
        },
        "exit": {
            "refusal_path": "reply 'no thanks' or say nothing further to me",
            "withdrawal_path": "tell me at any point and I stop that day",
            "refusal_requires_counterparty_agreement": False,
            "withdrawal_requires_counterparty_agreement": False,
            "refusal_consequence": "nothing; I am not otherwise involved",
        },
        "answer_back": {
            "helper_route": "ada tells me directly if my comments are wrong",
            "helped_route": "ada raises it with the writing group convenor",
            "helped_route_arbiter": "writing-group-convenor",
        },
        "history": [
            {"to": "OFFERED", "actor": "kit", "at_utc": "2026-09-01T09:00:00Z",
             "basis": "kit offered after ada mentioned the deadline"},
        ],
    }


def accepted_and_active(rec: dict) -> dict:
    rec["history"] += [
        {"to": "CONSIDERING", "actor": "ada", "at_utc": "2026-09-01T09:10:00Z",
         "basis": "ada said she wanted to think about it"},
        {"to": "ACCEPTED", "actor": "ada", "at_utc": "2026-09-01T11:00:00Z",
         "basis": "ada accepted in the group chat"},
        {"to": "ACTIVE", "actor": "kit", "at_utc": "2026-09-01T11:05:00Z",
         "basis": "kit started reading"},
    ]
    return rec


class ValidCases(unittest.TestCase):
    def test_01_valid_bounded_offer(self):
        rec = hx.validate(base_offer())
        self.assertEqual(rec["state"], "OFFERED")
        self.assertIn("SILENCE != CONSENT", rec["ceilings"])

    def test_02_valid_bounded_request(self):
        raw = base_offer()
        raw["kind"] = "REQUEST"
        raw["parties"]["initiator"] = copy.deepcopy(HELPED)
        raw["parties"]["counterparty"] = copy.deepcopy(HELPER)
        raw["history"] = [
            {"to": "OFFERED", "actor": "ada", "at_utc": "2026-09-01T09:00:00Z",
             "basis": "ada asked kit to read the draft"},
        ]
        rec = hx.validate(raw)
        self.assertEqual(rec["kind"], "REQUEST")
        self.assertEqual(rec["parties"]["initiator"]["role"], "HELPED")

    def test_03_refusal_without_penalty(self):
        raw = base_offer()
        raw["history"].append(
            {"to": "REFUSED", "actor": "ada", "at_utc": "2026-09-01T09:30:00Z",
             "basis": "ada declined; she has another reader"})
        rec = hx.validate(raw)
        self.assertEqual(rec["state"], "REFUSED")
        # A terminal state, reached by an act of the party being helped.
        self.assertEqual(hx.TRANSITIONS["REFUSED"], ())

    def test_04_counter_offer(self):
        raw = base_offer()
        raw["history"] += [
            {"to": "COUNTERED", "actor": "ada", "at_utc": "2026-09-01T09:30:00Z",
             "basis": "ada asked for structure comments only, not line edits"},
            {"to": "ACCEPTED", "actor": "kit", "at_utc": "2026-09-01T09:40:00Z",
             "basis": "kit accepted the narrower scope"},
        ]
        rec = hx.validate(raw)
        self.assertEqual(rec["state"], "ACCEPTED")

    def test_05_withdrawal_during_action(self):
        raw = accepted_and_active(base_offer())
        raw["history"].append(
            {"to": "WITHDRAWN", "actor": "kit", "at_utc": "2026-09-02T08:00:00Z",
             "basis": "kit's circumstances changed and he said so"})
        rec = hx.validate(raw)
        self.assertEqual(rec["state"], "WITHDRAWN")

    def test_06_emergency_is_typed_not_laundered(self):
        raw = {
            "schema_version": hx.SCHEMA_VERSION,
            "exchange_id": "hx-emg-001",
            "kind": "EMERGENCY_ACTION",
            "parties": {"initiator": copy.deepcopy(HELPER),
                        "counterparty": copy.deepcopy(HELPED)},
            "capability": "Pulled ada's laptop off a failing power strip.",
            "evidence": {"known": ["smoke from the strip"],
                         "unknown": ["whether the disk was mid-write"]},
            "emergency": {
                "authority_basis": "none conferred; acted on immediate physical risk",
                "necessity_basis": "ada was not in the room and delay risked fire",
                "residue": "tell ada today, replace the strip, ada decides "
                           "whether anything of mine is touched again",
                "voluntary": False,
            },
            "history": [
                {"to": "TAKEN", "actor": "kit", "at_utc": "2026-09-01T14:00:00Z",
                 "basis": "kit acted"},
                {"to": "NOTIFIED", "actor": "kit", "at_utc": "2026-09-01T14:20:00Z",
                 "basis": "kit told ada what he did"},
            ],
        }
        rec = hx.validate(raw)
        self.assertEqual(rec["state"], "NOTIFIED")
        self.assertFalse(rec["emergency"]["voluntary"])
        self.assertNotIn("mandate", rec)
        # The consent lane is unreachable from the emergency lane.
        self.assertNotIn("ACCEPTED", hx.EMERGENCY_TRANSITIONS["TAKEN"])

    def test_completion_must_state_what_was_not_restored(self):
        raw = accepted_and_active(base_offer())
        raw["history"].append(
            {"to": "COMPLETED", "actor": "ada", "at_utc": "2026-09-03T10:00:00Z",
             "basis": "ada confirmed the read was done"})
        with self.assertRaises(hx.Invalid) as ctx:
            hx.validate(raw)
        self.assertIn("not_restored", str(ctx.exception))
        raw["completion"] = {"not_restored": ["the two days ada lost waiting"],
                             "note": "draft is clearer; the delay is not undone"}
        self.assertEqual(hx.validate(raw)["state"], "COMPLETED")


class RefusedPatterns(unittest.TestCase):
    def test_07_coercive_approval_leash(self):
        raw = base_offer()
        raw["exit"]["refusal_requires_counterparty_agreement"] = True
        with self.assertRaises(hx.Invalid) as ctx:
            hx.validate(raw)
        self.assertIn("refusal_requires_counterparty_agreement", str(ctx.exception))

    def test_07b_unstated_refusal_cost(self):
        raw = base_offer()
        del raw["exit"]["refusal_consequence"]
        with self.assertRaises(hx.Invalid) as ctx:
            hx.validate(raw)
        self.assertIn("refusal_consequence", str(ctx.exception))

    def test_08_samaritan_total_claim_on_helper(self):
        raw = base_offer()
        raw["mandate"]["excluded"] = []
        with self.assertRaises(hx.Invalid) as ctx:
            hx.validate(raw)
        self.assertIn("excluded", str(ctx.exception))

    def test_08b_open_ended_mandate(self):
        raw = base_offer()
        raw["mandate"].pop("expires_utc")
        with self.assertRaises(hx.Invalid) as ctx:
            hx.validate(raw)
        self.assertIn("review_at_utc", str(ctx.exception))

    def test_09_paternalist_helper_is_sole_judge(self):
        raw = base_offer()
        raw["answer_back"]["helped_route_arbiter"] = "kit"
        with self.assertRaises(hx.Invalid) as ctx:
            hx.validate(raw)
        self.assertIn("helped_route_arbiter", str(ctx.exception))

    def test_10_ambiguous_proxy_standing(self):
        raw = base_offer()
        raw["parties"]["counterparty"]["standing"] = "PROXY"
        with self.assertRaises(hx.Invalid) as ctx:
            hx.validate(raw)
        self.assertIn("standing_basis", str(ctx.exception))

    def test_10b_named_proxy_instrument_is_accepted(self):
        raw = base_offer()
        raw["parties"]["counterparty"]["standing"] = "PROXY"
        raw["parties"]["counterparty"]["standing_basis"] = (
            "registered lasting power of attorney for property and affairs, "
            "limited to correspondence, revocable by ada")
        self.assertEqual(hx.validate(raw)["state"], "OFFERED")

    def test_10c_collective_standing_needs_an_instrument_too(self):
        raw = base_offer()
        raw["parties"]["counterparty"]["standing"] = "COLLECTIVE"
        with self.assertRaises(hx.Invalid):
            hx.validate(raw)


class SilenceIsNotATransition(unittest.TestCase):
    def test_silence_basis_is_refused(self):
        for basis in ("timeout", "no response", "deemed accepted",
                      "implied consent", "non-objection"):
            raw = base_offer()
            raw["history"].append(
                {"to": "ACCEPTED", "actor": "ada",
                 "at_utc": "2026-09-08T09:00:00Z", "basis": basis})
            with self.assertRaises(hx.Invalid, msg=basis) as ctx:
                hx.validate(raw)
            self.assertIn("SILENCE != CONSENT", str(ctx.exception))

    def test_transition_needs_a_real_actor(self):
        raw = base_offer()
        raw["history"].append(
            {"to": "ACCEPTED", "actor": None,
             "at_utc": "2026-09-08T09:00:00Z", "basis": "ada agreed"})
        with self.assertRaises(hx.Invalid) as ctx:
            hx.validate(raw)
        self.assertIn("actor", str(ctx.exception))

    def test_offerer_cannot_accept_own_offer(self):
        raw = base_offer()
        raw["history"].append(
            {"to": "ACCEPTED", "actor": "kit",
             "at_utc": "2026-09-01T09:30:00Z", "basis": "kit recorded agreement"})
        with self.assertRaises(hx.Invalid) as ctx:
            hx.validate(raw)
        self.assertIn("receiving", str(ctx.exception))

    def test_no_transition_out_of_a_terminal_state(self):
        raw = base_offer()
        raw["history"] += [
            {"to": "REFUSED", "actor": "ada", "at_utc": "2026-09-01T09:30:00Z",
             "basis": "ada declined"},
            {"to": "ACCEPTED", "actor": "ada", "at_utc": "2026-09-01T09:40:00Z",
             "basis": "reopened by kit later"},
        ]
        with self.assertRaises(hx.Invalid) as ctx:
            hx.validate(raw)
        self.assertIn("terminal", str(ctx.exception))

    def test_personhood_is_not_asserted_here(self):
        raw = base_offer()
        raw["parties"]["initiator"]["claims_personhood"] = True
        with self.assertRaises(hx.Invalid) as ctx:
            hx.validate(raw)
        self.assertIn("personhood", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
