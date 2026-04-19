"""
noise.py — Tasks 5 & 6: Add noise to sampled signals and plot.
Author: Yair Levi
"""

import logging
import os
import time
from typing import Dict, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from config import Config

logger = logging.getLogger(__name__)
PLOT_DIR = "plots"


def add_noise(
    t_samp: np.ndarray,
    sampled: Dict[float, np.ndarray],
    cfg: Config,
    rng: np.random.Generator,
) -> Dict[float, np.ndarray]:
    """
    Task 5 — Add amplitude and phase noise to each sampled signal.

    Noisy signal: (A + dA) * sin(2π*f*t + φ + dφ)
      dA ~ U(-amp_noise, +amp_noise)
      dφ ~ U(-phase_noise, +phase_noise)

    Args:
        t_samp:  Discrete time axis.
        sampled: Clean sampled signals {freq: array}.
        cfg:     Config holding noise parameters.
        rng:     Seeded numpy random generator.

    Returns:
        noisy: Dict {freq: noisy_array}.
    """
    t_start = time.perf_counter()
    logger.info("Task 5 — Adding noise (amp±%.2f, phase±%.4f) ...",
                cfg.amp_noise, cfg.phase_noise)

    n = len(t_samp)
    noisy: Dict[float, np.ndarray] = {}

    for f in cfg.freqs:
        d_amp = rng.uniform(-cfg.amp_noise, cfg.amp_noise, size=n)
        d_phase = rng.uniform(-cfg.phase_noise, cfg.phase_noise, size=n)
        a_noisy = cfg.amplitude + d_amp
        noisy[f] = a_noisy * np.sin(2 * np.pi * f * t_samp + cfg.phase + d_phase)

    elapsed = time.perf_counter() - t_start
    logger.info("Task 5 completed in %.4f s", elapsed)
    return noisy


def _composite(signals: Dict[float, np.ndarray]) -> np.ndarray:
    arrays = list(signals.values())
    return np.sum(arrays, axis=0) / len(arrays)


def plot_noisy(
    t_samp: np.ndarray,
    noisy: Dict[float, np.ndarray],
    sampled: Dict[float, np.ndarray],
    save_name: str = "task6_noisy.png",
) -> None:
    """
    Task 6 — Plot noisy signals alongside the clean reference and composite.
    Displays first 0.5 s for readability.
    """
    t_start = time.perf_counter()
    logger.info("Task 6 — Plotting noisy signals ...")

    noisy_composite = _composite(noisy)
    n = len(noisy)
    fig, axes = plt.subplots(n + 1, 1, figsize=(12, 2 * (n + 1)), sharex=True)
    fig.suptitle("Noisy Sampled Signals (first 0.5 s)", fontsize=14)

    mask = t_samp <= 0.5

    for ax, f in zip(axes, noisy.keys()):
        ax.plot(t_samp[mask], noisy[f][mask], linewidth=0.8,
                label="Noisy", alpha=0.7)
        ax.plot(t_samp[mask], sampled[f][mask], linewidth=0.8,
                linestyle="--", label="Clean", alpha=0.9)
        ax.set_ylabel(f"{f} Hz", fontsize=9)
        ax.set_ylim(-1.6, 1.6)
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(True, alpha=0.3)

    axes[-1].plot(t_samp[mask], noisy_composite[mask],
                  color="red", linewidth=0.8, label="Noisy Composite ÷4")
    axes[-1].set_ylabel("Composite", fontsize=9)
    axes[-1].set_xlabel("Time (s)")
    axes[-1].set_ylim(-1.6, 1.6)
    axes[-1].legend(fontsize=7)
    axes[-1].grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(PLOT_DIR, exist_ok=True)
    save_path = os.path.join(PLOT_DIR, save_name)
    fig.savefig(save_path, dpi=120)
    plt.close(fig)

    elapsed = time.perf_counter() - t_start
    logger.info("Task 6 — Plot saved to %s (%.4f s)", save_path, elapsed)
