"""
Unit tests for the mode-aware exploration–exploitation attention system
introduced in SentientAgent.move_focus().

Uses deterministic seeding / monkeypatching of random.random and
random.choice so every branch is exercised reliably.
"""

import random
import unittest
from unittest.mock import patch

from swarm_cli import AgentRole, CognitionMode, SentientAgent


def _make_agent(curiosity: float = 0.5, mode: CognitionMode = CognitionMode.STABLE) -> SentientAgent:
    """Return a SentientAgent with fixed curiosity and cognition mode."""
    agent = SentientAgent("test_agent", AgentRole.EXECUTOR)
    agent.curiosity = curiosity
    agent.cognition_mode = mode
    # Place focus in the middle so neighbors always exist
    mid = agent.map_size // 2
    agent.focus_point = (mid, mid)
    return agent


class TestMoveFocusGlobalJump(unittest.TestCase):
    """r < global_jump_p → focus teleports anywhere on the map."""

    def test_global_jump_changes_focus(self):
        agent = _make_agent(curiosity=1.0, mode=CognitionMode.EMERGENT_REORGANIZATION)
        # With curiosity=1.0 and EMERGENT_REORGANIZATION, global_jump_p = 0.02*3 = 0.06
        # Patch random.random to return 0.0 (< 0.06) → triggers global jump
        target = (3, 7)
        with patch("random.random", return_value=0.0), \
             patch("random.randint", side_effect=list(target)):
            agent.move_focus()
        self.assertEqual(agent.focus_point, target)

    def test_global_jump_baseline_mode(self):
        """Even in STABLE mode a global jump fires when r < global_jump_p."""
        agent = _make_agent(curiosity=1.0, mode=CognitionMode.STABLE)
        # STABLE: global_jump_p = 0.02*0.5 = 0.01
        target = (1, 2)
        with patch("random.random", return_value=0.005), \
             patch("random.randint", side_effect=list(target)):
            agent.move_focus()
        self.assertEqual(agent.focus_point, target)


class TestMoveFocusLocalExplore(unittest.TestCase):
    """global_jump_p <= r < global_jump_p + local_explore_p → random neighbor step."""

    def test_local_explore_moves_to_neighbor(self):
        agent = _make_agent(curiosity=1.0, mode=CognitionMode.STABLE)
        # STABLE: global_jump_p=0.01, local_explore_p=0.10  →  band [0.01, 0.11)
        mid = agent.map_size // 2
        # choice returns 1 for both dx and dy → focus moves right and down by 1
        with patch("random.random", return_value=0.05), \
             patch("random.choice", return_value=1):
            agent.move_focus()
        self.assertEqual(agent.focus_point, (mid + 1, mid + 1))

    def test_local_explore_clamps_to_map(self):
        """A local-explore step never produces out-of-bounds coordinates."""
        agent = _make_agent(curiosity=1.0, mode=CognitionMode.STABLE)
        agent.focus_point = (0, 0)
        with patch("random.random", return_value=0.05), \
             patch("random.choice", return_value=-1):
            agent.move_focus()
        fx, fy = agent.focus_point
        self.assertGreaterEqual(fx, 0)
        self.assertGreaterEqual(fy, 0)


class TestMoveFocusGreedyAscent(unittest.TestCase):
    """r >= global_jump_p + local_explore_p → greedy ascent toward highest neighbor."""

    def test_greedy_moves_to_highest_neighbor(self):
        agent = _make_agent(curiosity=0.0, mode=CognitionMode.STABLE)
        # curiosity=0 → all probabilities are 0 → always greedy
        mid = agent.map_size // 2
        agent.focus_point = (mid, mid)
        # Plant a spike one step to the right
        agent.surface[mid, mid + 1] = 999.0
        with patch("random.random", return_value=0.99):
            agent.move_focus()
        self.assertEqual(agent.focus_point, (mid + 1, mid))

    def test_greedy_stays_if_already_at_peak(self):
        agent = _make_agent(curiosity=0.0, mode=CognitionMode.STABLE)
        mid = agent.map_size // 2
        agent.focus_point = (mid, mid)
        # Make current cell the highest
        agent.surface[:] = 0.0
        agent.surface[mid, mid] = 100.0
        with patch("random.random", return_value=0.99):
            agent.move_focus()
        self.assertEqual(agent.focus_point, (mid, mid))


class TestProbabilityClamping(unittest.TestCase):
    """Ensure clamping prevents invalid probability sums regardless of curiosity / mode."""

    def _compute_probs(self, curiosity: float, mode: CognitionMode):
        """Replicate the probability computation from move_focus() and return (g, l)."""
        local_explore_p = curiosity * 0.20
        global_jump_p   = curiosity * 0.02

        if mode == CognitionMode.CONFLICT_NOISE:
            global_jump_p   *= 2.0
            local_explore_p *= 1.25
        elif mode == CognitionMode.EMERGENT_REORGANIZATION:
            global_jump_p   *= 3.0
            local_explore_p *= 1.5
        elif mode == CognitionMode.STABLE:
            global_jump_p   *= 0.5
            local_explore_p *= 0.5

        global_jump_p   = max(0.0, min(1.0, global_jump_p))
        local_explore_p = max(0.0, min(1.0 - global_jump_p, local_explore_p))
        return global_jump_p, local_explore_p

    def test_sum_never_exceeds_one(self):
        for curiosity in [0.0, 0.5, 1.0, 1.5]:  # include out-of-range curiosity
            for mode in CognitionMode:
                g, l = self._compute_probs(curiosity, mode)
                self.assertLessEqual(g + l, 1.0 + 1e-9,
                                     msg=f"curiosity={curiosity}, mode={mode}: g+l={g+l}")

    def test_probabilities_non_negative(self):
        for curiosity in [0.0, 0.5, 1.0]:
            for mode in CognitionMode:
                g, l = self._compute_probs(curiosity, mode)
                self.assertGreaterEqual(g, 0.0)
                self.assertGreaterEqual(l, 0.0)


class TestModeModulation(unittest.TestCase):
    """Mode-aware multipliers produce the expected ordering of probabilities."""

    def _global_jump_p(self, mode: CognitionMode, curiosity: float = 1.0) -> float:
        gj = curiosity * 0.02
        if mode == CognitionMode.CONFLICT_NOISE:
            gj *= 2.0
        elif mode == CognitionMode.EMERGENT_REORGANIZATION:
            gj *= 3.0
        elif mode == CognitionMode.STABLE:
            gj *= 0.5
        return max(0.0, min(1.0, gj))

    def test_emergent_reorg_highest_global_jump(self):
        self.assertGreater(
            self._global_jump_p(CognitionMode.EMERGENT_REORGANIZATION),
            self._global_jump_p(CognitionMode.CONFLICT_NOISE)
        )

    def test_stable_lowest_global_jump(self):
        self.assertLess(
            self._global_jump_p(CognitionMode.STABLE),
            self._global_jump_p(CognitionMode.LEARNING_SHIFT)
        )


class TestUpdateCognitionOrdersMode(unittest.TestCase):
    """update_cognition() classifies the mode BEFORE calling move_focus(),
    so move_focus() always sees the current tick's mode."""

    def test_move_focus_sees_current_mode(self):
        """The cognition_mode passed to move_focus() matches what update_cognition()
        classifies from the current surface drift."""
        agent = _make_agent(curiosity=0.5, mode=CognitionMode.STABLE)
        # Baseline is locked on first call; manipulate surface to force STABLE drift.
        agent.baseline_locked = False  # allow re-lock on first call

        captured_modes = []

        original_move_focus = agent.move_focus.__func__

        def spy_move_focus(self_inner):
            captured_modes.append(self_inner.cognition_mode)
            original_move_focus(self_inner)

        # Patch move_focus on the instance to spy on cognition_mode at call time
        import types
        agent.move_focus = types.MethodType(spy_move_focus, agent)

        agent.update_cognition()

        self.assertEqual(len(captured_modes), 1)
        # With a freshly locked baseline, drift ≈ 0 → STABLE
        self.assertEqual(captured_modes[0], CognitionMode.STABLE)


if __name__ == "__main__":
    unittest.main()
