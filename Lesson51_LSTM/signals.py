"""
signals.py — Tasks 1 & 2: Generate and plot pure sine signals.
Author: Yair Levi
"""

import logging
import os
import time
from typing import Dict, Tuple

import matplotlib
matplotlib.use("Agg")          # Non-interactive backend (safe on WSL)
import matplotlib.pyplot as plt
import numpy as np

from config import Config

logger = logging.getLogger(__name__)
PLOT_DIR = "plots"


def generate_signals(cfg: Config) -> Tuple[np.ndarray, Dict[float, np.ndarray]]:
    """
    Task 1 — Generate 4 pure sine signals over a continuous time axis.

    y(t) = A * sin(2π*f*t + φ)

    Returns:
        t:       Time array [0, duration] with 10 000 points.
        signals: Dict mapping frequency → signal array.
    """
    t_start = time.perf_counter()
    logger.info("Task 1 — Generating %d sine signals ...", cfg.n_signals)

    t = np.linspace(0, cfg.duration, cfg.sample_rate * cfg.duration, endpoint=False)
    signals: Dict[float, np.ndarray] = {}

    for f in cfg.freqs:
        signals[f] = cfg.amplitude * np.sin(2 * np.pi * f * t + cfg.phase)

    elapsed = time.perf_counter() - t_start
    logger.info("Task 1 completed in %.4f s", elapsed)
    return t, signals


def _composite(signals: Dict[float, np.ndarray]) -> np.ndarray:
    """Return the normalised sum of all signals (divided by number of signals)."""
    arrays = list(signals.values())
    return np.sum(arrays, axis=0) / len(arrays)


def plot_signals(
    t: np.ndarray,
    signals: Dict[float, np.ndarray],
    title_prefix: str = "Continuous",
    save_name: str = "task2_continuous.png",
) -> None:
    """
    Task 2 — Plot all signals and their normalised composite.

    Args:
        t:           Time axis.
        signals:     Dict {freq: array}.
        title_prefix: Used in figure title.
        save_name:   PNG filename inside plots/.
    """
    t_start = time.perf_counter()
    logger.info("Task 2 — Plotting %s signals ...", title_prefix)

    composite = _composite(signals)
    n = len(signals)
    fig, axes = plt.subplots(n + 1, 1, figsize=(12, 2 * (n + 1)), sharex=True)
    fig.suptitle(f"{title_prefix} Signals (10 s window)", fontsize=14)

    for ax, (f, sig) in zip(axes, signals.items()):
        ax.plot(t, sig, linewidth=0.8)
        ax.set_ylabel(f"{f} Hz", fontsize=9)
        ax.set_ylim(-1.4, 1.4)
        ax.grid(True, alpha=0.3)

    axes[-1].plot(t, composite, color="red", linewidth=0.8, label="Composite ÷ 4")
    axes[-1].set_ylabel("Composite", fontsize=9)
    axes[-1].set_xlabel("Time (s)")
    axes[-1].set_ylim(-1.4, 1.4)
    axes[-1].grid(True, alpha=0.3)
    axes[-1].legend(fontsize=8)

    plt.tight_layout()
    os.makedirs(PLOT_DIR, exist_ok=True)
    save_path = os.path.join(PLOT_DIR, save_name)
    fig.savefig(save_path, dpi=120)
    plt.close(fig)

    elapsed = time.perf_counter() - t_start
    logger.info("Task 2 — Plot saved to %s (%.4f s)", save_path, elapsed)
