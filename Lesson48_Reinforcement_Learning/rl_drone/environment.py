# rl_drone/environment.py
# Author: Yair Levi
# Grid environment: structures, reward calculation, state transitions

import numpy as np
from .config import (
    GRID_ROWS, GRID_COLS, START_CELL, TARGET_CELL,
    ACTIONS, ACTION_DELTAS,
    REWARD_STEP, REWARD_TARGET, REWARD_BORDER, REWARD_BUILDING,
    STRUCT_NONE, STRUCT_BUILDING, STRUCT_TRAP, STRUCT_WIND, STRUCT_REWARDS,
    ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT,
)
from .logger_setup import setup_logger

log = setup_logger("environment")


class Environment:
    def __init__(self):
        self.grid = np.zeros((GRID_ROWS, GRID_COLS), dtype=int)  # structure map
        self.drone_pos = START_CELL
        log.info("Environment initialised  (%dx%d grid)", GRID_ROWS, GRID_COLS)

    # ------------------------------------------------------------------
    def reset_drone(self):
        self.drone_pos = START_CELL

    def set_structure(self, row: int, col: int, stype: int):
        if (row, col) in (START_CELL, TARGET_CELL):
            return  # protect start/target
        self.grid[row, col] = stype
        log.info("Structure %d set at (%d,%d)", stype, row, col)

    def remove_structure(self, row: int, col: int):
        self.grid[row, col] = STRUCT_NONE

    def clear_structures(self):
        self.grid[:] = STRUCT_NONE
        log.info("All structures cleared")

    # ------------------------------------------------------------------
    def get_initial_q_penalty(self, row: int, col: int, action: int) -> float:
        """Return a very negative Q seed for illegal/blocked directions."""
        dr, dc = ACTION_DELTAS[action]
        nr, nc = row + dr, col + dc
        # Out-of-bounds
        if not (0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS):
            return REWARD_BORDER
        # Adjacent structure
        stype = self.grid[nr, nc]
        if stype != STRUCT_NONE:
            return STRUCT_REWARDS[stype]
        return 0.0

    # ------------------------------------------------------------------
    def step(self, row: int, col: int, action: int):
        """
        Execute one step from (row, col) with given action.
        Returns: (new_row, new_col, reward, done)
        Buildings are impassable — drone stays in place and gets a heavy penalty.
        """
        dr, dc = ACTION_DELTAS[action]
        nr, nc = row + dr, col + dc

        # Boundary check
        if not (0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS):
            return row, col, REWARD_BORDER, False

        stype = self.grid[nr, nc]

        # Buildings are impassable — block movement entirely
        if stype == STRUCT_BUILDING:
            return row, col, REWARD_BUILDING, False

        reward = REWARD_STEP
        if stype != STRUCT_NONE:
            reward += STRUCT_REWARDS[stype]   # trap / wind penalty

        done = (nr, nc) == TARGET_CELL
        if done:
            reward += REWARD_TARGET

        self.drone_pos = (nr, nc)
        return nr, nc, reward, done

    # ------------------------------------------------------------------
    def get_grid_copy(self) -> np.ndarray:
        return self.grid.copy()

    def is_border_action(self, row: int, col: int, action: int) -> bool:
        dr, dc = ACTION_DELTAS[action]
        nr, nc = row + dr, col + dc
        return not (0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS)
