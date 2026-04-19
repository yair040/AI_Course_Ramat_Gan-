"""
visualise.py — Task 14: Loss curves, metrics, and sample predictions.
Author: Yair Levi
"""

import logging
import os
import time
from typing import Dict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)
PLOT_DIR = "plots"


def plot_loss_curve(history: Dict[str, list], save_name: str = "task14_loss.png") -> None:
    """Plot training and validation loss over epochs."""
    t_start = time.perf_counter()
    logger.info("Task 14 — Plotting loss curve ...")

    epochs = range(1, len(history["train"]) + 1)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(epochs, history["train"], label="Train Loss", linewidth=1.5)
    ax.plot(epochs, history["val"], label="Val Loss", linewidth=1.5, linestyle="--")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("MSE Loss")
    ax.set_title("Training vs Validation Loss")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    os.makedirs(PLOT_DIR, exist_ok=True)
    path = os.path.join(PLOT_DIR, save_name)
    fig.savefig(path, dpi=120)
    plt.close(fig)

    elapsed = time.perf_counter() - t_start
    logger.info("Loss curve saved to %s (%.4f s)", path, elapsed)


def print_metrics(metrics: Dict[str, float]) -> None:
    """Print evaluation metrics as a formatted table."""
    print("\n" + "=" * 40)
    print("  TEST SET EVALUATION METRICS")
    print("=" * 40)
    for k, v in metrics.items():
        print(f"  {k:<8}: {v:.6f}")
    print("=" * 40 + "\n")


def plot_samples(
    te_noisy: np.ndarray,
    predictions: np.ndarray,
    te_labels: np.ndarray,
    n_samples: int = 5,
    save_name: str = "task14_samples.png",
) -> None:
    """
    Plot n_samples randomly chosen test examples.
    Each panel shows: noisy input / model prediction / clean label.

    Args:
        te_noisy:    (N, window) noisy composite windows.
        predictions: (N, window) model output.
        te_labels:   (N, window) clean signal labels.
        n_samples:   Number of panels to draw.
        save_name:   PNG filename inside plots/.
    """
    t_start = time.perf_counter()
    logger.info("Task 14 — Plotting %d sample predictions ...", n_samples)

    rng = np.random.default_rng(0)
    indices = rng.choice(len(te_noisy), size=min(n_samples, len(te_noisy)), replace=False)
    x_axis = np.arange(te_noisy.shape[1])

    fig, axes = plt.subplots(n_samples, 1, figsize=(10, 2.5 * n_samples), sharex=True)
    if n_samples == 1:
        axes = [axes]

    fig.suptitle("Sample Predictions: Noisy Input / Predicted / Clean", fontsize=12)

    for ax, idx in zip(axes, indices):
        ax.plot(x_axis, te_noisy[idx], label="Noisy Composite", alpha=0.6, linewidth=1)
        ax.plot(x_axis, predictions[idx], label="Predicted", linewidth=1.5, linestyle="--")
        ax.plot(x_axis, te_labels[idx], label="Clean Label", linewidth=1.5, linestyle=":")
        ax.set_ylabel(f"Row {idx}")
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel("Sample index within window")
    plt.tight_layout()

    os.makedirs(PLOT_DIR, exist_ok=True)
    path = os.path.join(PLOT_DIR, save_name)
    fig.savefig(path, dpi=120)
    plt.close(fig)

    elapsed = time.perf_counter() - t_start
    logger.info("Sample plot saved to %s (%.4f s)", path, elapsed)
