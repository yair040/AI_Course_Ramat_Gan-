# rl_drone/gui.py
# Author: Yair Levi
# Main GUI window: toolbar buttons, layout, state management

import tkinter as tk
from tkinter import ttk
import multiprocessing as mp
import queue as q_mod
import time

from .config import (
    STRUCT_BUILDING, STRUCT_TRAP, STRUCT_WIND, STRUCT_NONE,
    SPEED_MIN, SPEED_MAX, SPEED_DEFAULT,
)
from .grid_widget import GridWidget
from .stats_panel import StatsPanel
from .logger_setup import setup_logger

log = setup_logger("gui")

BTN_STYLE = dict(bg="#21262d", fg="#c9d1d9", activebackground="#30363d",
                 activeforeground="#ffffff", relief=tk.FLAT,
                 font=("Courier", 9, "bold"), padx=6, pady=4, cursor="hand2")


class App(tk.Tk):
    def __init__(self, cmd_q: mp.Queue, state_q: mp.Queue):
        super().__init__()
        self.title("RL Drone — Q-Table")
        self.configure(bg="#0d1117")
        self.resizable(False, False)
        self._cmd_q = cmd_q
        self._state_q = state_q
        self._paused = True
        self._editor_on = False
        self._heatmap_mode = False   # False=structures, True=V heatmap
        self._show_arrows = True
        self._show_qv = False
        self._speed = SPEED_DEFAULT
        self._editor_struct = STRUCT_BUILDING
        self._speed_visible = False
        self._build_layout()
        self.after(50, self._poll_state)
        log.info("GUI App ready")

    # ------------------------------------------------------------------
    def _btn(self, parent, text, cmd, **kw):
        b = tk.Button(parent, text=text, command=cmd, **{**BTN_STYLE, **kw})
        b.pack(side=tk.LEFT, padx=3)
        return b

    def _build_layout(self):
        # Toolbar
        toolbar = tk.Frame(self, bg="#161b22", pady=4)
        toolbar.pack(fill=tk.X)
        self._btn_run = self._btn(toolbar, "▶ Start/Pause", self._toggle_run)
        self._btn_editor = self._btn(toolbar, "✏ Editor", self._toggle_editor)
        self._btn_heatmap = self._btn(toolbar, "🔥 Heatmap", self._toggle_heatmap)
        self._btn_speed = self._btn(toolbar, "⏩ Speed", self._toggle_speed)
        self._btn_arrows = self._btn(toolbar, "↗ Arrows", self._toggle_arrows)
        self._btn_qv = self._btn(toolbar, "Q/V", self._toggle_qv)
        self._btn_soft = self._btn(toolbar, "↺ Soft Reset", self._soft_reset)
        self._btn_hard = self._btn(toolbar, "⚡ Hard Reset", self._hard_reset)

        # Speed slider (hidden initially)
        self._speed_frame = tk.Frame(self, bg="#161b22")
        tk.Label(self._speed_frame, text="Speed delay (s):", bg="#161b22",
                 fg="#c9d1d9", font=("Courier", 9)).pack(side=tk.LEFT, padx=4)
        self._speed_var = tk.DoubleVar(value=self._speed)
        self._speed_slider = ttk.Scale(self._speed_frame, from_=SPEED_MIN, to=SPEED_MAX,
                                       orient=tk.HORIZONTAL, length=180,
                                       variable=self._speed_var,
                                       command=self._on_speed_change)
        self._speed_slider.pack(side=tk.LEFT, padx=4)

        # Editor pane (hidden initially)
        self._editor_frame = tk.Frame(self, bg="#21262d", pady=6)
        tk.Label(self._editor_frame, text="Add/Remove:", bg="#21262d",
                 fg="#00d4ff", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=6)
        self._struct_var = tk.IntVar(value=STRUCT_BUILDING)
        for label, val in [("Building", STRUCT_BUILDING), ("Trap", STRUCT_TRAP),
                            ("Wind", STRUCT_WIND), ("Erase", STRUCT_NONE)]:
            tk.Radiobutton(self._editor_frame, text=label, variable=self._struct_var,
                           value=val, bg="#21262d", fg="#c9d1d9", selectcolor="#0d1117",
                           activebackground="#21262d", font=("Courier", 9),
                           command=self._on_struct_select).pack(side=tk.LEFT, padx=4)

        # Main content area
        content = tk.Frame(self, bg="#0d1117")
        content.pack(fill=tk.BOTH, expand=True)

        self._grid = GridWidget(content, on_cell_click=self._on_cell_click)
        self._grid.pack(side=tk.LEFT, padx=4, pady=4)

        self._stats = StatsPanel(content)
        self._stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)

    # ------------------------------------------------------------------
    def _toggle_run(self):
        self._paused = not self._paused
        self._cmd_q.put({"type": "pause" if self._paused else "resume"})
        self._btn_run.config(text="▶ Resume" if self._paused else "⏸ Pause")
        log.info("Run toggled → paused=%s", self._paused)

    def _toggle_editor(self):
        self._editor_on = not self._editor_on
        self._btn_editor.config(relief=tk.SUNKEN if self._editor_on else tk.FLAT)
        if self._editor_on:
            self._editor_frame.pack(fill=tk.X, after=self._editor_frame.master.winfo_children()[0])
        else:
            self._editor_frame.pack_forget()

    def _toggle_heatmap(self):
        self._heatmap_mode = not self._heatmap_mode
        self._grid.show_heatmap = self._heatmap_mode
        self._btn_heatmap.config(relief=tk.SUNKEN if self._heatmap_mode else tk.FLAT)

    def _toggle_speed(self):
        self._speed_visible = not self._speed_visible
        if self._speed_visible:
            self._speed_frame.pack(fill=tk.X)
        else:
            self._speed_frame.pack_forget()

    def _on_speed_change(self, _val):
        self._speed = self._speed_var.get()
        self._cmd_q.put({"type": "speed", "value": self._speed})

    def _toggle_arrows(self):
        self._show_arrows = not self._show_arrows
        self._grid.show_arrows = self._show_arrows

    def _toggle_qv(self):
        self._show_qv = not self._show_qv
        self._grid.show_qv = self._show_qv

    def _on_struct_select(self):
        self._editor_struct = self._struct_var.get()

    def _on_cell_click(self, r, c):
        if not self._editor_on:
            return
        stype = self._editor_struct
        # Update local grid immediately so the cell redraws without waiting
        # for a state message back from the worker (which won't come when paused)
        self._grid._grid_data[r, c] = stype
        self._grid._draw_grid()
        # Also tell the worker so Q-table is reset with new structure
        self._cmd_q.put({"type": "set_struct", "row": r, "col": c, "stype": stype})

    def _soft_reset(self):
        self._cmd_q.put({"type": "soft_reset"})
        self._stats.reset_graphs()
        self._training_done_shown = False
        self._btn_run.config(text="▶ Start/Pause", bg="#21262d")
        # Reset drone visually to start position immediately
        self._grid._drone_pos = (0, 0)
        self._grid._best_path = set()
        self._grid._draw_grid()

    def _hard_reset(self):
        self._cmd_q.put({"type": "hard_reset"})
        self._stats.reset_graphs()
        self._training_done_shown = False
        self._btn_run.config(text="▶ Start/Pause", bg="#21262d")
        # Reset drone visually and clear all structures from local grid
        self._grid._drone_pos = (0, 0)
        self._grid._best_path = set()
        self._grid._grid_data[:] = 0   # clear structures locally too
        self._grid._arrows = {}
        self._grid._Q = None
        self._grid._V = None
        self._grid._draw_grid()

    # ------------------------------------------------------------------
    def _poll_state(self):
        last_state = None
        try:
            while True:
                last_state = self._state_q.get_nowait()
        except Exception:
            pass
        if last_state is not None:
            self._apply_state(last_state)
        self.after(30, self._poll_state)

    def _apply_state(self, state):
        best_path = state.get("best_path") or []
        self._grid.update_state(
            state["grid"], state["Q"], state["V"],
            state["arrows"], state["drone_pos"],
            best_path=best_path if best_path else None,
        )
        self._stats.update_stats(
            state["episode"], state["reward"], state["epsilon"], state["step"]
        )
        self._stats.update_graphs(
            state["total_steps"], state["epsilon"], state["V"], state["Q"],
            ep_rewards=state.get("ep_rewards"),
        )
        if state.get("training_done") and not getattr(self, "_training_done_shown", False):
            self._training_done_shown = True
            self._btn_run.config(text="✔ Done", bg="#27ae60")
