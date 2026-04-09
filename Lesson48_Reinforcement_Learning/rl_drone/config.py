# rl_drone/config.py
# Author: Yair Levi
# All configuration constants for the RL Drone simulator

import os

# --- Grid ---
GRID_ROWS = 12
GRID_COLS = 12
START_CELL = (0, 0)
TARGET_CELL = (GRID_ROWS - 1, GRID_COLS - 1)
MAX_STEPS_PER_EPISODE = 200   # raised from 60 — needed for 12x12 with obstacles

# --- Actions ---
ACTION_UP    = 0
ACTION_DOWN  = 1
ACTION_LEFT  = 2
ACTION_RIGHT = 3
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]
ACTION_DELTAS = {
    ACTION_UP:    (-1,  0),
    ACTION_DOWN:  ( 1,  0),
    ACTION_LEFT:  ( 0, -1),
    ACTION_RIGHT: ( 0,  1),
}

# --- Reward values ---
REWARD_STEP        = -1      # every step
REWARD_TARGET      = 100     # reaching the goal
REWARD_BORDER      = -100    # out-of-bound direction
REWARD_BUILDING    = -80     # entering a building
REWARD_TRAP        = -40     # entering a trap
REWARD_WIND        = -10     # entering a wind cell

# --- Structure types ---
STRUCT_NONE     = 0
STRUCT_BUILDING = 1
STRUCT_TRAP     = 2
STRUCT_WIND     = 3

STRUCT_REWARDS = {
    STRUCT_BUILDING: REWARD_BUILDING,
    STRUCT_TRAP:     REWARD_TRAP,
    STRUCT_WIND:     REWARD_WIND,
}

# --- Q-Learning hyper-params ---
ALPHA         = 0.1    # learning rate
GAMMA         = 0.95   # discount factor
EPSILON_START = 1.0
EPSILON_MIN   = 0.01
EPSILON_DECAY = 0.998  # slower decay — more exploration before exploitation
ARROW_THRESHOLD  = 0.5    # |V - maxQ| < threshold → draw arrow
REVISIT_PENALTY  = -3.0   # extra penalty for revisiting a cell in the same episode

# --- Algorithm improvements ---
# 1. Eligibility traces Q(λ): propagates reward backward through full episode path
LAMBDA           = 0.8    # trace decay: 0=pure TD, 1=Monte Carlo

# 2. Reward shaping: Manhattan-distance bonus steers agent toward target from step 1
SHAPING_SCALE    = 0.4    # weight of distance-improvement bonus

# 3. Optimistic initialisation: non-border Q-values seeded positive so all cells
#    look promising and get visited before epsilon decays
Q_OPTIMISTIC     = 10.0   # initial Q value for free (non-border) cells

# 4. Double Q-Learning: use two Q-tables to eliminate max-Q overestimation bias
USE_DOUBLE_Q     = True

# --- GUI ---
CELL_SIZE     = 68    # pixels per cell
CELL_PAD      = 2
CANVAS_W      = GRID_COLS * CELL_SIZE
CANVAS_H      = GRID_ROWS * CELL_SIZE
DRONE_IMG_SIZE = CELL_SIZE - 6   # resize target

# --- Best-path highlight ---
TARGETS_TO_STOP      = 5              # stop training after this many successful arrivals
PATH_HIGHLIGHT_COLOR = "#0e6655"      # deep teal — distinct from green/red/purple/amber/slate

# --- Speed ---
SPEED_MIN  = 0.0    # seconds sleep between steps
SPEED_MAX  = 0.5
SPEED_DEFAULT = 0.05

# --- Paths (relative) ---
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
LOG_DIR    = os.path.join(BASE_DIR, "log")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
DRONE_IMG_ORIG   = os.path.join(IMAGES_DIR, "drone.png")
DRONE_IMG_SMALL  = os.path.join(IMAGES_DIR, "drone_small.png")

# --- Logging ---
LOG_FILE       = os.path.join(LOG_DIR, "rl_drone.log")
LOG_MAX_BYTES  = 16 * 1024 * 1024   # 16 MB
LOG_BACKUP_COUNT = 19               # 1 active + 19 backups = 20 files total
