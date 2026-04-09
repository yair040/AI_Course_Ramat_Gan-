# tasks.md — Implementation Tasks

## Phase 1: Setup
- [x] Create directory structure
- [x] Write CLAUDE.md
- [x] Write planning.md
- [x] Write tasks.md
- [x] Write requirements.txt
- [x] Create package `rl_drone/__init__.py`

## Phase 2: Core Modules
- [x] `rl_drone/config.py` — constants and reward values
- [x] `rl_drone/logger_setup.py` — ring-buffer logging
- [x] `rl_drone/environment.py` — grid, structures, rewards
- [x] `rl_drone/agent.py` — Q-table, epsilon, learning step

## Phase 3: GUI
- [x] `rl_drone/gui.py` — main window, toolbar buttons, layout
- [x] `rl_drone/grid_widget.py` — canvas grid, drone image, arrows, heatmap
- [x] `rl_drone/stats_panel.py` — episode stats, epsilon graph, V/Q graph, legend

## Phase 4: Integration
- [x] `main.py` — wire multiprocessing, launch GUI + worker

## Phase 5: Assets
- [x] Resize drone.png to fit cell dimensions and save

## Acceptance Criteria
- [ ] GUI loads without error
- [ ] Drone starts at (0,0), reaches (11,11) after training
- [ ] All buttons functional (pause/resume, editor, heatmap, speed, arrows, Q&V, soft reset, hard reset)
- [ ] Arrows appear correctly after cells converge
- [ ] Heatmap toggles between structure view and V-value view
- [ ] Graphs update dynamically
- [ ] Log files appear in `rl_drone/log/`
