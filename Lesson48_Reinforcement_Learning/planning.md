# planning.md — Architecture & Design

## Overview
A Tkinter-based Reinforcement Learning simulator where a drone learns the optimal path
on a 12×12 grid using an enhanced Q-table algorithm. The GUI and RL engine run in
separate processes, communicating via multiprocessing queues.

---

## Architecture

### Processes
1. **Main (GUI) Process** — Tkinter window, rendering, user interaction
2. **RL Worker Process** — Q-table updates, episode stepping, sends state to GUI

### Communication
- `cmd_queue` (GUI → Worker): start, pause, reset, structure changes, speed
- `state_queue` (Worker → GUI): per-step state — drone pos, Q+Q2, V, arrows, episode info, best path

### Queue Policy
- `state_queue` is non-blocking (`put_nowait`); frames are dropped if the queue is full
- GUI polls every 30 ms and renders only the **latest** message — intermediate frames discarded

---

## Modules

| File | Responsibility |
|---|---|
| `main.py` | Entry point, spawn worker process, wire queues |
| `rl_drone/__init__.py` | Package init |
| `rl_drone/config.py` | All constants: grid, rewards, algorithm params, paths |
| `rl_drone/logger_setup.py` | Ring-buffer rotating logger (20 × 16 MB) |
| `rl_drone/environment.py` | Grid state, structures, step/reward logic, building blocks |
| `rl_drone/agent.py` | Double Q-tables, eligibility traces, epsilon, path tracing |
| `rl_drone/gui.py` | Main window, toolbar, editor pane, state polling, resets |
| `rl_drone/grid_widget.py` | Canvas: cells, drone image, arrows, heatmap, path highlight |
| `rl_drone/stats_panel.py` | 3-subplot matplotlib figure, live stats labels, legend |

---

## Grid Logic
- 12×12 grid; cell (0,0) = top-left (start), cell (11,11) = bottom-right (target)
- Actions: `UP=0, DOWN=1, LEFT=2, RIGHT=3`
- Border cells are seeded with heavy negative Q for out-of-bound directions
- Buildings are **impassable** — drone stays in place, receives −80
- Traps (−40) and Wind (−10) are passable; adjacent cell Q is pre-penalised

---

## Algorithm

### Enhanced Q-Learning

#### 1. Optimistic Initialisation
All non-border Q-values seeded at `Q_OPTIMISTIC = +10`. Every unvisited cell looks
attractive → full grid exploration before epsilon decays.

#### 2. Double Q-Learning
Two tables `Q` and `Q2`. Updates alternate randomly:
- Table A selects best action, Table B evaluates → unbiased TD target
- All decisions (arrows, path, display) use `Q + Q2` as the combined estimate

#### 3. Eligibility Traces Q(λ)
```
E  ← γλ · E          # decay all traces (λ = 0.8)
E[s,a] += 1           # accumulate at current (s,a)
δ = r + γ·V(s') − Q[s,a]
Q  += α · δ · E       # update ALL visited cells proportionally
```
Propagates reward backward through the full episode path in one step.

#### 4. Reward Shaping
```
shaping = SHAPING_SCALE × (manhattan(s) − manhattan(s'))
reward += shaping
```
Potential-based bonus (scale = 0.4) — does not change the optimal policy.

#### Additional Mechanisms
- **Revisit penalty** (`−3`): discourages oscillation within a single episode
- **Episode limit**: 200 steps (raised from 60 for obstacle-rich grids)

### Hyperparameters (config.py)

| Constant | Value |
|---|---|
| `ALPHA` | 0.1 |
| `GAMMA` | 0.95 |
| `LAMBDA` | 0.8 |
| `SHAPING_SCALE` | 0.4 |
| `Q_OPTIMISTIC` | 10.0 |
| `EPSILON_START` | 1.0 |
| `EPSILON_MIN` | 0.01 |
| `EPSILON_DECAY` | 0.998 |
| `MAX_STEPS_PER_EPISODE` | 200 |
| `REVISIT_PENALTY` | −3.0 |
| `TARGETS_TO_STOP` | 5 |
| `USE_DOUBLE_Q` | True |

---

## Epsilon Strategy
- Start: ε = 1.0
- After each episode: ε = max(ε_min, ε × EPSILON_DECAY)
- At EPSILON_DECAY = 0.998, reaches ε_min ≈ 0.01 after ~2300 episodes

---

## Arrow Logic
- Arrows use `q_combined = Q + Q2` for direction
- Convergence check: `|V(s) − max Q(s,·)| < ARROW_THRESHOLD (0.5)`
- Cells that were never updated (V=0, Q still at optimistic seed) are skipped
- Arrows work for negative max Q — the least-bad direction is still meaningful

---

## Final Path Tracing & Validation
1. Triggered after `TARGETS_TO_STOP` (5) successful arrivals at target
2. Traced by pure greedy `argmax(Q + Q2)` from start — no Dijkstra summation
   (Q already encodes discounted future rewards; summing would double-count)
3. **Mandatory validation**: for every consecutive pair in the path,
   `argmax(Q+Q2)` at cell i must point exactly to cell i+1
4. If validation fails → roll back arrival count, continue training
5. Path-cell arrows are derived geometrically from path steps (not argmax),
   guaranteeing arrow ↔ path ↔ displayed Q values are always consistent

---

## Heatmap Modes
- **Structures mode** (default): start=green, target=red, building=grey,
  trap=purple, wind=dark-orange, path=teal, empty=dark
- **V-value mode**: colour-mapped from blue (low V) to red (high V)

---

## Stats Panel — 3 Subplots
1. **Epsilon** — exploration probability vs total steps (y fixed 0–1)
2. **Avg V & Avg maxQ** — value estimates vs total steps (y auto-scaled to visible window)
3. **Episode Reward** — raw per-episode reward + MA-10 smoothed trend

All three use full-history downsampling to MAX_PLOT_PTS = 500 evenly-spaced points
so the entire timeline is always visible regardless of total step count.

---

## Display Consistency
All three of the following use `Q + Q2` as the single source of truth:
- **Cell Q/V display** — shows combined values, not Q alone
- **Arrow directions** — `argmax(Q + Q2)` for non-path cells; path step for path cells
- **Path tracing** — `argmax(Q + Q2)` greedy walk with cycle detection

---

## Logging
- Ring buffer: 20 files × 16 MB
- Handler: `RotatingFileHandler(maxBytes=16*1024*1024, backupCount=19)`
- Location: `rl_drone/log/rl_drone.log`
- Level: INFO and above; also mirrored to console
