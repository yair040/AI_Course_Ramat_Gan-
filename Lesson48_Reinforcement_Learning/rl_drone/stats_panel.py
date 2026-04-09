# rl_drone/stats_panel.py
# Author: Yair Levi
# Right-side stats panel: live stats, 3-subplot graph, legend

import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from .config import PATH_HIGHLIGHT_COLOR
from .logger_setup import setup_logger

log = setup_logger("stats_panel")

# All legend colors must be visually distinct from each other AND from
# the background (#0d1117 near-black) and PATH_HIGHLIGHT_COLOR (teal #0e6655)
LEGEND_ITEMS = [
    ("Start",      "#27ae60"),   # vivid green
    ("Target",     "#e74c3c"),   # vivid red
    ("Building",   "#4a5568"),   # steel grey
    ("Trap",       "#8e44ad"),   # purple
    ("Wind",       "#e67e22"),   # dark orange  (was amber #f39c12 — too close to wind arrows)
    ("Final Path", PATH_HIGHLIGHT_COLOR),  # deep teal
]

GRAPH_REDRAW_EVERY = 20
MAX_PLOT_PTS       = 500

# Rolling window for episode-reward smoothing (shows trend, not raw noise)
REWARD_SMOOTH = 10


class StatsPanel(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#0d1117", **kwargs)
        self._steps_history   = []
        self._eps_history     = []
        self._v_history       = []
        self._q_history       = []
        self._ep_nums         = []   # episode indices for reward graph
        self._ep_rewards      = []   # raw episode rewards
        self._graph_counter   = 0
        self._build_info_section()
        self._build_graphs()
        self._build_legend()
        log.info("StatsPanel created")

    # ------------------------------------------------------------------
    def _label(self, parent, text, fg="#c9d1d9", font=("Courier", 10)):
        return tk.Label(parent, text=text, bg="#0d1117", fg=fg, font=font)

    def _build_info_section(self):
        frame = tk.Frame(self, bg="#0d1117")
        frame.pack(fill=tk.X, padx=8, pady=(10, 4))
        tk.Label(frame, text="LIVE STATS", bg="#0d1117", fg="#00d4ff",
                 font=("Courier", 12, "bold")).pack(anchor="w")
        self._lbl_episode = self._label(frame, "Episode: 0");  self._lbl_episode.pack(anchor="w")
        self._lbl_reward  = self._label(frame, "Reward:  0");  self._lbl_reward.pack(anchor="w")
        self._lbl_epsilon = self._label(frame, "Epsilon: 1.000"); self._lbl_epsilon.pack(anchor="w")
        self._lbl_step    = self._label(frame, "Step:    0");  self._lbl_step.pack(anchor="w")

    def _build_graphs(self):
        # 3 subplots stacked vertically in one figure
        fig = Figure(figsize=(3.5, 6.0), facecolor="#0d1117", layout="constrained")
        self._ax_eps = fig.add_subplot(311)   # Epsilon
        self._ax_vq  = fig.add_subplot(312)   # Avg V & Avg maxQ
        self._ax_rew = fig.add_subplot(313)   # Episode reward (smoothed)

        for ax in (self._ax_eps, self._ax_vq, self._ax_rew):
            ax.set_facecolor("#161b22")
            ax.tick_params(colors="#c9d1d9", labelsize=7)
            for spine in ax.spines.values():
                spine.set_edgecolor("#30363d")

        self._ax_eps.set_title("Epsilon",            color="#00d4ff", fontsize=8)
        self._ax_vq.set_title("Avg V & Avg maxQ",    color="#00d4ff", fontsize=8)
        self._ax_rew.set_title("Episode Reward",     color="#00d4ff", fontsize=8)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=6, pady=4)
        self._fig = fig
        self._canvas_fig = canvas

    def _build_legend(self):
        frame = tk.Frame(self, bg="#0d1117")
        frame.pack(fill=tk.X, padx=8, pady=6)
        tk.Label(frame, text="LEGEND", bg="#0d1117", fg="#00d4ff",
                 font=("Courier", 11, "bold")).pack(anchor="w")
        for name, color in LEGEND_ITEMS:
            row = tk.Frame(frame, bg="#0d1117")
            row.pack(anchor="w", pady=1)
            tk.Label(row, bg=color, width=3).pack(side=tk.LEFT, padx=(0, 6))
            tk.Label(row, text=name, bg="#0d1117", fg="#c9d1d9",
                     font=("Courier", 9)).pack(side=tk.LEFT)

    # ------------------------------------------------------------------
    def update_stats(self, episode, reward, epsilon, step):
        self._lbl_episode.config(text=f"Episode: {episode}")
        self._lbl_reward.config( text=f"Reward:  {reward:.1f}")
        self._lbl_epsilon.config(text=f"Epsilon: {epsilon:.4f}")
        self._lbl_step.config(   text=f"Step:    {step}")

    def update_graphs(self, total_steps, epsilon, V, Q, ep_rewards=None):
        from .config import USE_DOUBLE_Q
        # Q received is Q+Q2 (combined). Normalise to per-table scale for display.
        Q_norm = Q / 2.0 if USE_DOUBLE_Q else Q
        # --- Accumulate step-level data ---
        self._steps_history.append(total_steps)
        self._eps_history.append(epsilon)
        self._v_history.append(float(np.mean(V)))
        self._q_history.append(float(np.mean(np.max(Q_norm, axis=2))))

        # --- Accumulate episode-level reward data ---
        if ep_rewards is not None and len(ep_rewards) > len(self._ep_rewards):
            new_eps = ep_rewards[len(self._ep_rewards):]
            for r in new_eps:
                self._ep_nums.append(len(self._ep_rewards) + 1)
                self._ep_rewards.append(r)

        self._graph_counter += 1
        if self._graph_counter % GRAPH_REDRAW_EVERY != 0:
            return

        # --- Downsample full history to MAX_PLOT_PTS for rendering ---
        n     = len(self._steps_history)
        x_max = self._steps_history[-1] if n else 1
        if n <= MAX_PLOT_PTS:
            idx = range(n)
        else:
            idx = [int(round(i * (n - 1) / (MAX_PLOT_PTS - 1))) for i in range(MAX_PLOT_PTS)]

        xs    = [self._steps_history[i] for i in idx]
        eps_y = [self._eps_history[i]   for i in idx]
        v_y   = [self._v_history[i]     for i in idx]
        q_y   = [self._q_history[i]     for i in idx]

        # --- Plot 1: Epsilon (fixed 0–1) ---
        self._ax_eps.cla()
        self._ax_eps.set_facecolor("#161b22")
        self._ax_eps.plot(xs, eps_y, color="#00d4ff", linewidth=1)
        self._ax_eps.set_title("Epsilon", color="#00d4ff", fontsize=8)
        self._ax_eps.tick_params(colors="#c9d1d9", labelsize=7)
        self._ax_eps.set_xlim(0, max(x_max, 1))
        self._ax_eps.set_ylim(0, 1.05)

        # --- Plot 2: Avg V & Avg maxQ ---
        y_lo, y_hi = self._ylim(v_y + q_y)
        self._ax_vq.cla()
        self._ax_vq.set_facecolor("#161b22")
        self._ax_vq.plot(xs, v_y, color="#f39c12", linewidth=2,
                         linestyle="--", label="Avg V")
        self._ax_vq.plot(xs, q_y, color="#2ecc71", linewidth=1.5,
                         linestyle="-",  label="Avg maxQ")
        self._ax_vq.set_title("Avg V & Avg maxQ", color="#00d4ff", fontsize=8)
        self._ax_vq.tick_params(colors="#c9d1d9", labelsize=7)
        self._ax_vq.set_xlim(0, max(x_max, 1))
        self._ax_vq.set_ylim(y_lo, y_hi)
        self._ax_vq.legend(fontsize=7, facecolor="#21262d", labelcolor="#c9d1d9",
                            loc="lower right")

        # --- Plot 3: Episode reward (raw + smoothed trend) ---
        self._ax_rew.cla()
        self._ax_rew.set_facecolor("#161b22")
        if self._ep_rewards:
            m  = len(self._ep_nums)
            ep_idx = list(range(m))
            if m <= MAX_PLOT_PTS:
                didx = ep_idx
            else:
                didx = [int(round(i * (m - 1) / (MAX_PLOT_PTS - 1))) for i in range(MAX_PLOT_PTS)]
            ex = [self._ep_nums[i]    for i in didx]
            ey = [self._ep_rewards[i] for i in didx]

            # Raw (faint)
            self._ax_rew.plot(ex, ey, color="#5d6d7e", linewidth=0.8, alpha=0.5)
            # Smoothed trend
            k = min(REWARD_SMOOTH, len(ey))
            smooth = np.convolve(ey, np.ones(k) / k, mode="valid")
            sx = ex[k - 1:]
            self._ax_rew.plot(sx, smooth, color="#e74c3c", linewidth=1.5, label=f"MA-{k}")
            self._ax_rew.legend(fontsize=7, facecolor="#21262d", labelcolor="#c9d1d9",
                                loc="lower right")
            rl, rh = self._ylim(ey)
            self._ax_rew.set_ylim(rl, rh)
            self._ax_rew.set_xlim(1, max(self._ep_nums[-1], 2))

        self._ax_rew.set_title("Episode Reward", color="#00d4ff", fontsize=8)
        self._ax_rew.tick_params(colors="#c9d1d9", labelsize=7)

        self._canvas_fig.draw_idle()

    # ------------------------------------------------------------------
    @staticmethod
    def _ylim(vals):
        """Return (lo, hi) with 5% padding; minimum span of 1.0."""
        lo, hi = min(vals), max(vals)
        span   = hi - lo
        if span < 1.0:
            mid = (lo + hi) / 2.0
            lo, hi, span = mid - 0.5, mid + 0.5, 1.0
        pad = span * 0.05
        return lo - pad, hi + pad

    # ------------------------------------------------------------------
    def reset_graphs(self):
        self._steps_history.clear()
        self._eps_history.clear()
        self._v_history.clear()
        self._q_history.clear()
        self._ep_nums.clear()
        self._ep_rewards.clear()
        self._graph_counter = 0
