"""
sampling.py — Tasks 3 & 4: Sample signals at 1 kHz and plot.
Author: Yair Levi
"""

import logging
import os
import time
from multiprocessing import Pool, cpu_count
from typing import Dict, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from config import Config

logger = logging.getLogger(__name__)
PLOT_DIR = "plots"


def _sample_one(args: Tuple) -> Tuple[float, np.ndarray]:
    """Worker: sample a single sine signal at the given sample rate."""
    f, amplitude, phase, sample_rate, duration = args
    t = np.arange(0, duration, 1.0 / sample_rate)
    sig = amplitude * np.sin(2 * np.pi * f * t + phase)
    return f, sig


def sample_signals(cfg: Config) -> Tuple[np.ndarray, Dict[float, np.ndarray]]:
    """
    Task 3 — Sample all sine signals in parallel.

    Uses multiprocessing.Pool so each signal is computed in a separate process.

    Returns:
        t_samp:   Discrete time axis.
        sampled:  Dict {freq: sampled_array}.
    """
    t_start = time.perf_counter()
    logger.info(
        "Task 3 — Sampling %d signals at %d Hz for %d s ...",
        cfg.n_signals, cfg.sample_rate, cfg.duration,
    )

    t_samp = np.arange(0, cfg.duration, 1.0 / cfg.sample_rate)

    worker_args = [
        (f, cfg.amplitude, cfg.phase, cfg.sample_rate, cfg.duration)
        for f in cfg.freqs
    ]

    n_workers = min(cfg.n_signals, max(1, cpu_count() - 1))
    with Pool(processes=n_workers) as pool:
        results = pool.map(_sample_one, worker_args)

    sampled = {f: sig for f, sig in results}

    elapsed = time.perf_counter() - t_start
    logger.info("Task 3 completed in %.4f s (%d samples/signal)", elapsed, cfg.n_samples)
    return t_samp, sampled


def _composite(signals: Dict[float, np.ndarray]) -> np.ndarray:
    arrays = list(signals.values())
    return np.sum(arrays, axis=0) / len(arrays)


def plot_sampled(
    t_samp: np.ndarray,
    sampled: Dict[float, np.ndarray],
    title_prefix: str = "Sampled",
    save_name: str = "task4_sampled.png",
) -> None:
    """
    Task 4 — Plot sampled signals and their normalised composite.
    Displays only the first 0.5 s to keep the stem plot readable.
    """
    t_start = time.perf_counter()
    logger.info("Task 4 — Plotting %s signals ...", title_prefix)

    composite = _composite(sampled)
    n = len(sampled)
    fig, axes = plt.subplots(n + 1, 1, figsize=(12, 2 * (n + 1)), sharex=True)
    fig.suptitle(f"{title_prefix} Signals (first 0.5 s)", fontsize=14)

    # Show only first 0.5 s for readability
    mask = t_samp <= 0.5

    for ax, (f, sig) in zip(axes, sampled.items()):
        ax.stem(t_samp[mask], sig[mask], markerfmt="C0.", linefmt="C0-",
                basefmt="k-")
        ax.set_ylabel(f"{f} Hz", fontsize=9)
        ax.set_ylim(-1.4, 1.4)
        ax.grid(True, alpha=0.3)

    axes[-1].stem(t_samp[mask], composite[mask], markerfmt="r.", linefmt="r-",
                  basefmt="k-")
    axes[-1].set_ylabel("Composite", fontsize=9)
    axes[-1].set_xlabel("Time (s)")
    axes[-1].set_ylim(-1.4, 1.4)
    axes[-1].grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(PLOT_DIR, exist_ok=True)
    save_path = os.path.join(PLOT_DIR, save_name)
    fig.savefig(save_path, dpi=120)
    plt.close(fig)

    elapsed = time.perf_counter() - t_start
    logger.info("Task 4 — Plot saved to %s (%.4f s)", save_path, elapsed)
