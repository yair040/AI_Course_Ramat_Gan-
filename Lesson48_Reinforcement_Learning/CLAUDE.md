# CLAUDE.md — Project Context

## Author
Yair Levi

## Project
Reinforcement Learning Q-Table Drone Simulation

## Environment
- OS: WSL (Windows Subsystem for Linux)
- Python virtual environment: located at `../../venv` relative to the project root
- Package: `rl_drone` (includes `__init__.py`)

## Structure
```
Reinforcement_Learning/
├── CLAUDE.md
├── planning.md
├── tasks.md
├── requirements.txt
├── main.py
└── rl_drone/
    ├── __init__.py
    ├── config.py
    ├── agent.py
    ├── environment.py
    ├── gui.py
    ├── grid_widget.py
    ├── stats_panel.py
    ├── logger_setup.py
    └── images/
        └── drone.png
    └── log/
```

## Conventions
- All paths are relative (never absolute)
- Each Python file ≤ 150 lines
- Logging: INFO level, ring buffer of 20 files × 16 MB, stored in `rl_drone/log/`
- Multiprocessing used where possible (RL computation vs GUI)
- GUI: Tkinter

## Run
```bash
source ../../venv/bin/activate
python main.py
```
