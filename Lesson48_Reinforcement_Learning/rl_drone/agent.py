# rl_drone/agent.py
# Author: Yair Levi
# Q-Learning agent — improvements:
#   1. Eligibility Traces Q(λ)  — reward propagates through whole episode path
#   2. Reward Shaping            — Manhattan-distance bonus from step 1
#   3. Optimistic Initialisation — seeds Q positive so all cells are explored
#   4. Double Q-Learning         — eliminates max-Q overestimation bias

import numpy as np
import random
from .config import (
    GRID_ROWS, GRID_COLS, ACTIONS, TARGET_CELL, START_CELL,
    ALPHA, GAMMA, EPSILON_START, EPSILON_MIN, EPSILON_DECAY,
    ARROW_THRESHOLD, MAX_STEPS_PER_EPISODE,
    TARGETS_TO_STOP, ACTION_DELTAS, REVISIT_PENALTY,
    LAMBDA, SHAPING_SCALE, Q_OPTIMISTIC, USE_DOUBLE_Q,
)
from .environment import Environment
from .logger_setup import setup_logger

log = setup_logger("agent")

_TR, _TC = TARGET_CELL


def _manhattan(r, c):
    return abs(r - _TR) + abs(c - _TC)


class Agent:
    def __init__(self, env: Environment):
        self.env = env
        self.n_actions = len(ACTIONS)
        self.Q  = np.zeros((GRID_ROWS, GRID_COLS, self.n_actions), dtype=float)
        self.Q2 = np.zeros((GRID_ROWS, GRID_COLS, self.n_actions), dtype=float)
        self.V  = np.zeros((GRID_ROWS, GRID_COLS), dtype=float)
        self.epsilon         = EPSILON_START
        self.episode         = 0
        self.total_steps     = 0
        self.target_arrivals = 0
        self.best_path       = []
        self._episode_rewards = []
        self._init_tables()
        log.info("Agent initialised (Double-Q=%s, lambda=%.2f)", USE_DOUBLE_Q, LAMBDA)

    # ------------------------------------------------------------------
    def _init_tables(self):
        """Seed both Q-tables: border/structure directions negative, free directions optimistic."""
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                for a in ACTIONS:
                    penalty = self.env.get_initial_q_penalty(r, c, a)
                    val = penalty if penalty < 0 else Q_OPTIMISTIC
                    self.Q[r, c, a]  = val
                    self.Q2[r, c, a] = val

    def soft_reset(self):
        self.Q  = np.zeros((GRID_ROWS, GRID_COLS, self.n_actions), dtype=float)
        self.Q2 = np.zeros((GRID_ROWS, GRID_COLS, self.n_actions), dtype=float)
        self.V  = np.zeros((GRID_ROWS, GRID_COLS), dtype=float)
        self.epsilon          = EPSILON_START
        self.episode          = 0
        self.total_steps      = 0
        self.target_arrivals  = 0
        self.best_path        = []
        self._episode_rewards = []
        self._init_tables()
        self.env.reset_drone()
        log.info("Soft reset complete")

    def hard_reset(self):
        self.env.clear_structures()
        self.soft_reset()
        log.info("Hard reset complete")

    # ------------------------------------------------------------------
    def choose_action(self, row: int, col: int) -> int:
        if random.random() < self.epsilon:
            return random.choice(ACTIONS)
        q_avg = self.Q[row, col] + (self.Q2[row, col] if USE_DOUBLE_Q else 0)
        return int(np.argmax(q_avg))

    # ------------------------------------------------------------------
    def _q_update(self, row, col, action, reward, nr, nc, done):
        """One-step TD update. Returns delta for eligibility trace propagation."""
        if USE_DOUBLE_Q and random.random() < 0.5:
            best_a   = int(np.argmax(self.Q[nr, nc]))   if not done else 0
            next_val = float(self.Q2[nr, nc, best_a])    if not done else 0.0
            old_q    = self.Q2[row, col, action]
            delta    = reward + GAMMA * next_val - old_q
            self.Q2[row, col, action] = old_q + ALPHA * delta
        else:
            if USE_DOUBLE_Q:
                best_a   = int(np.argmax(self.Q2[nr, nc])) if not done else 0
                next_val = float(self.Q[nr, nc, best_a])    if not done else 0.0
            else:
                next_val = float(np.max(self.Q[nr, nc]))    if not done else 0.0
            old_q = self.Q[row, col, action]
            delta = reward + GAMMA * next_val - old_q
            self.Q[row, col, action] = old_q + ALPHA * delta

        self.V[row, col] = float(np.max(self.Q[row, col]))
        return delta

    # ------------------------------------------------------------------
    def _validate_path(self, path: list) -> bool:
        """
        Check that argmax Q at every path cell (except target) points exactly
        to the next cell in the path. If any cell's best action disagrees,
        the Q-table hasn't converged there — reject the path and keep training.
        Also checks no two consecutive cells point at each other (deadlock).
        """
        if not path or path[-1] != TARGET_CELL:
            return False
        q_avg = self.Q + (self.Q2 if USE_DOUBLE_Q else 0)
        for i in range(len(path) - 1):
            r,  c  = path[i]
            nr, nc = path[i + 1]
            # What does argmax Q say is the best action from this cell?
            best_action = int(np.argmax(q_avg[r, c]))
            dr, dc = ACTION_DELTAS[best_action]
            # The best action must lead exactly to the next path cell
            if (r + dr, c + dc) != (nr, nc):
                log.info("Path validation failed at step %d (%d,%d): "
                         "argmax points to (%d,%d) but path goes to (%d,%d)",
                         i, r, c, r+dr, c+dc, nr, nc)
                return False
        return True

    # ------------------------------------------------------------------
    def trace_best_path(self) -> list:
        """
        Trace the optimal path by following argmax(Q+Q2) greedily.
        Q(s,a) encodes discounted future rewards so argmax IS the Bellman-
        optimal action — no Dijkstra summation needed.

        Returns [] if a cycle is detected (Q not yet converged).
        The returned path is always validated: every cell's argmax must point
        to the next step, guaranteeing arrows and path agree perfectly.
        """
        q_avg   = self.Q + (self.Q2 if USE_DOUBLE_Q else 0)
        path    = []
        seen    = {}
        r, c    = START_CELL

        for step in range(GRID_ROWS * GRID_COLS + 5):
            if (r, c) in seen:
                log.warning("trace_best_path: cycle detected at (%d,%d) — Q not converged", r, c)
                return []
            seen[(r, c)] = step
            path.append((r, c))

            if (r, c) == TARGET_CELL:
                log.info("Path traced: %d cells — validating...", len(path))
                if self._validate_path(path):
                    log.info("Path validated OK")
                    return path
                log.info("Path failed validation — Q not fully converged")
                return []

            best_action = int(np.argmax(q_avg[r, c]))
            dr, dc = ACTION_DELTAS[best_action]
            r, c   = r + dr, c + dc

        log.warning("trace_best_path: exceeded max steps")
        return []

    # ------------------------------------------------------------------
    def run_episode(self, speed_getter, paused_getter, cmd_handler):
        import time
        self.env.reset_drone()
        row, col     = self.env.drone_pos
        total_reward = 0.0
        steps        = 0
        self.episode += 1
        visited_this_episode = set()
        E = np.zeros((GRID_ROWS, GRID_COLS, self.n_actions), dtype=float)  # eligibility traces

        for _ in range(MAX_STEPS_PER_EPISODE):
            cmd_handler()
            while paused_getter():
                time.sleep(0.05)
                cmd_handler()

            action = self.choose_action(row, col)
            nr, nc, reward, done = self.env.step(row, col, action)

            # Reward shaping: potential-based Manhattan bonus
            if not done:
                reward += SHAPING_SCALE * (_manhattan(row, col) - _manhattan(nr, nc))

            # Revisit penalty
            if (nr, nc) in visited_this_episode and not done:
                reward += REVISIT_PENALTY
            visited_this_episode.add((row, col))

            # Eligibility traces: decay all, accumulate at current (s,a)
            E *= GAMMA * LAMBDA
            E[row, col, action] += 1.0

            # TD error (standard or Double-Q one-step)
            delta = self._q_update(row, col, action, reward, nr, nc, done)

            # Propagate TD error to ALL previously visited (s,a) via traces
            self.Q += ALPHA * delta * E
            if USE_DOUBLE_Q:
                self.Q2 += ALPHA * delta * E

            # Update V for cells with non-trivial traces
            active = E.max(axis=2) > 1e-6
            self.V[active] = np.max(self.Q[active], axis=1)

            total_reward     += reward
            self.total_steps += 1
            steps            += 1

            if done:
                self.target_arrivals += 1

            yield {
                "episode":       self.episode,
                "step":          steps,
                "total_steps":   self.total_steps,
                "drone_pos":     (nr, nc),
                "reward":        total_reward,
                "epsilon":       self.epsilon,
                "Q":             self.Q + (self.Q2 if USE_DOUBLE_Q else 0),  # combined — what display and decisions use
                "V":             self.V.copy(),
                "arrows":        self._compute_arrows(self.best_path),
                "done":          done,
                "training_done": False,
                "best_path":     [],
                "ep_rewards":    list(self._episode_rewards),
            }

            row, col = nr, nc
            sleep_t = speed_getter()
            if sleep_t > 0:
                time.sleep(sleep_t)
            if done:
                break

        # Post-episode: record reward, decay epsilon
        self._episode_rewards.append(total_reward)
        self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)
        log.debug("Ep %d  reward=%.1f  eps=%.4f  arrivals=%d",
                  self.episode, total_reward, self.epsilon, self.target_arrivals)

        training_done = self.target_arrivals >= TARGETS_TO_STOP
        if training_done and not self.best_path:
            self.best_path = self.trace_best_path()
            if not self.best_path:
                # Target genuinely unreachable (fully walled off) — keep training
                self.target_arrivals = TARGETS_TO_STOP - 1
                training_done = False
                log.warning("Target unreachable — check for complete wall")

        if training_done:
            yield {
                "episode":       self.episode,
                "step":          steps,
                "total_steps":   self.total_steps,
                "drone_pos":     TARGET_CELL,
                "reward":        total_reward,
                "epsilon":       self.epsilon,
                "Q":             self.Q + (self.Q2 if USE_DOUBLE_Q else 0),
                "V":             self.V.copy(),
                "arrows":        self._compute_arrows(self.best_path),
                "done":          True,
                "training_done": True,
                "best_path":     list(self.best_path),
                "ep_rewards":    list(self._episode_rewards),
            }

    # ------------------------------------------------------------------
    def _compute_arrows(self, best_path: list = None) -> dict:
        """
        Compute arrow directions using q_combined (Q+Q2).
        For path cells, the arrow is derived from the path step itself
        (cell[i] → cell[i+1]), guaranteeing perfect agreement with the path.
        For non-path cells, argmax q_combined is used with a convergence gate.
        """
        arrows     = {}
        q_combined = self.Q + (self.Q2 if USE_DOUBLE_Q else 0)
        opt_seed   = Q_OPTIMISTIC * (2 if USE_DOUBLE_Q else 1)

        # Build path-step action map: cell → action that leads to next path cell
        path_actions = {}
        if best_path:
            for i in range(len(best_path) - 1):
                r,  c  = best_path[i]
                nr, nc = best_path[i + 1]
                for a in ACTIONS:
                    dr, dc = ACTION_DELTAS[a]
                    if r + dr == nr and c + dc == nc:
                        path_actions[(r, c)] = a
                        break

        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                if (r, c) == TARGET_CELL:
                    continue

                # Path cells: arrow = exact path direction (guaranteed consistent)
                if (r, c) in path_actions:
                    arrows[(r, c)] = path_actions[(r, c)]
                    continue

                # Non-path cells: skip if never trained
                q_cell = q_combined[r, c]
                v      = self.V[r, c]
                never_updated = (v == 0.0 and float(np.max(q_cell)) >= opt_seed)
                if never_updated:
                    continue

                # Convergence check
                if abs(v - float(np.max(self.Q[r, c]))) < ARROW_THRESHOLD:
                    arrows[(r, c)] = int(np.argmax(q_cell))

        return arrows
