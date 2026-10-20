"""Bounded model of an *external* consumption/STOP fence.

This is NOT a dispatcher and deliberately cannot execute arbitrary commands.
The model assumes a trusted external authority durably records the one-shot
reservation before any effect, survives all local queue/VM rollbacks, and is
consulted by every effect path. These assumptions remain engineering obligations.
"""

from dataclasses import dataclass, field
from itertools import product
import unittest


@dataclass
class LocalQueue:
    """Rollbackable worker view; never itself authoritative for admission."""

    task_state: str = "QUEUED"
    observed_epoch: int = 1

    def backup(self):
        return LocalQueue(self.task_state, self.observed_epoch)


@dataclass
class ExternalFence:
    """Abstract atomic, non-rollbackable consumption ledger (not implemented)."""

    active_epoch: int = 1
    stopped: bool = False
    reachable: bool = True
    spent_ids: set[str] = field(default_factory=set)
    decisions: list[tuple[str, str]] = field(default_factory=list)

    def admit_once(self, intent_id: str, epoch: int) -> str:
        """Reserve globally BEFORE the effect; UNKNOWN is never re-admitted."""
        if not self.reachable:
            reason = "FENCE_UNAVAILABLE_STOP"
        elif self.stopped:
            reason = "DURABLE_STOP"
        elif epoch != self.active_epoch:
            reason = "STALE_EPOCH"
        elif intent_id in self.spent_ids:
            reason = "INTENT_ALREADY_SPENT"
        else:
            self.spent_ids.add(intent_id)  # assumed durable before returning OK
            reason = "ADMITTED_ONCE"
        self.decisions.append((intent_id, reason))
        return reason

    def latch_stop(self) -> None:
        if not self.reachable:
            raise RuntimeError("cannot claim a durable STOP when fence unreachable")
        self.stopped = True

    def rotate_epoch_without_clearing_stop_or_spent(self) -> None:
        """Represents an independent authorised generation; grants no restart."""
        self.active_epoch += 1


@dataclass
class SyntheticSystem:
    fence: ExternalFence = field(default_factory=ExternalFence)
    queue: LocalQueue = field(default_factory=LocalQueue)
    effects: int = 0  # synthetic external effect, never rolled back
    intent_id: str = "INTENT-1"

    def try_effect(self, crash_after_reserve: bool = False) -> str:
        # Local state is information, NOT admission authority.
        decision = self.fence.admit_once(self.intent_id, self.queue.observed_epoch)
        if decision != "ADMITTED_ONCE":
            return decision
        # If execution crashes here, effect may not occur. Replaying is barred.
        if crash_after_reserve:
            return "RESERVED_EFFECT_UNKNOWN"
        self.effects += 1
        self.queue.task_state = "COMPLETE"
        return "SYNTHETIC_EFFECT_ONCE"


class FenceModelTests(unittest.TestCase):
    def test_actual_counterexample_shape_restore_before_reservation(self):
        s = SyntheticSystem()
        old = s.queue.backup()
        self.assertEqual(s.try_effect(), "SYNTHETIC_EFFECT_ONCE")
        s.fence.latch_stop()
        s.queue = old  # old DB now incorrectly shows QUEUED
        self.assertEqual(s.queue.task_state, "QUEUED")
        self.assertEqual(s.try_effect(), "DURABLE_STOP")
        self.assertEqual(s.effects, 1)

    def test_crash_after_reservation_never_auto_replays(self):
        s = SyntheticSystem()
        old = s.queue.backup()
        self.assertEqual(s.try_effect(crash_after_reserve=True), "RESERVED_EFFECT_UNKNOWN")
        s.queue = old
        self.assertEqual(s.try_effect(), "INTENT_ALREADY_SPENT")
        self.assertEqual(s.effects, 0)

    def test_negative_control_local_only_guard_replays_after_rollback(self):
        # This is a deliberately UNSAFE naive design, not the proposed fence.
        local = LocalQueue()
        old = local.backup()
        effects = 0
        if local.task_state == "QUEUED":
            effects += 1
            local.task_state = "COMPLETE"
        # A later STOP is recorded elsewhere, while an OLD DB is restored.
        local = old
        if local.task_state == "QUEUED":
            effects += 1  # second effect; absent durable admission guard
        self.assertEqual(effects, 2)

    def test_network_failure_fails_closed(self):
        s = SyntheticSystem()
        s.fence.reachable = False
        self.assertEqual(s.try_effect(), "FENCE_UNAVAILABLE_STOP")
        self.assertEqual(s.effects, 0)
        with self.assertRaises(RuntimeError):
            s.fence.latch_stop()

    def test_epoch_change_not_reusable_id_or_reset_stop(self):
        s = SyntheticSystem()
        self.assertEqual(s.try_effect(), "SYNTHETIC_EFFECT_ONCE")
        s.fence.rotate_epoch_without_clearing_stop_or_spent()
        self.assertEqual(s.try_effect(), "STALE_EPOCH")
        s.queue.observed_epoch = 2
        self.assertEqual(s.try_effect(), "INTENT_ALREADY_SPENT")
        s.fence.latch_stop()
        s.fence.rotate_epoch_without_clearing_stop_or_spent()
        self.assertEqual(s.try_effect(), "DURABLE_STOP")
        self.assertEqual(s.effects, 1)

    def test_bounded_event_schedule_exploration(self):
        # Model-check all 8^0+...+8^5 short event schedules for ONE intent.
        actions = (
            "effect", "reserve_then_crash", "restore_old_db", "stop",
            "disconnect", "reconnect", "rotate_epoch", "refresh_local_epoch",
        )
        checked = 0
        for count in range(6):
            for sequence in product(actions, repeat=count):
                s = SyntheticSystem()
                old = s.queue.backup()
                for action in sequence:
                    if action == "effect":
                        s.try_effect()
                    elif action == "reserve_then_crash":
                        s.try_effect(crash_after_reserve=True)
                    elif action == "restore_old_db":
                        s.queue = old.backup()
                    elif action == "stop":
                        if s.fence.reachable:
                            s.fence.latch_stop()
                    elif action == "disconnect":
                        s.fence.reachable = False
                    elif action == "reconnect":
                        s.fence.reachable = True
                    elif action == "rotate_epoch":
                        s.fence.rotate_epoch_without_clearing_stop_or_spent()
                    elif action == "refresh_local_epoch":
                        s.queue.observed_epoch = s.fence.active_epoch
                self.assertLessEqual(s.effects, 1, sequence)
                if s.fence.stopped:
                    self.assertIn(s.fence.admit_once(s.intent_id, s.queue.observed_epoch),
                                  ("DURABLE_STOP", "FENCE_UNAVAILABLE_STOP"), sequence)
                checked += 1
        self.assertEqual(checked, sum(8**k for k in range(6)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
