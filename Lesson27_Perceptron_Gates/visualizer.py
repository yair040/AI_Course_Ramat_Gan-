"""
Visualization Module

Author: Yair Levi
Date: 2025-12-30

Creates visualizations for network architecture, data points, and training history.
"""

import logging
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from tensorflow import keras

logger = logging.getLogger(__name__)


def plot_network_architecture(
    model: keras.Model,
    gate_type: str,
    output_dir: Path = None
) -> Path:
    """Plot neural network architecture diagram with perceptron details."""
    if output_dir is None:
        output_dir = Path(__file__).parent / "visualizations"
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis("off")

    # Get layer info and weights
    layers = [{"name": "input", "units": model.input_shape[1], "act": None}]
    for layer in model.layers:
        if hasattr(layer, "units"):
            layers.append({
                "name": layer.name,
                "units": layer.units,
                "act": layer.activation.__name__
            })

    # Draw layers with proper labels
    positions = {}
    spacing = 0.7 / (len(layers) - 1) if len(layers) > 1 else 0

    for i, layer in enumerate(layers):
        x = 0.15 + i * spacing
        n_neurons = layer["units"]
        y_space = 0.5 / max(n_neurons, 1)
        y_start = 0.5 - (n_neurons - 1) * y_space / 2
        positions[i] = []

        for j in range(n_neurons):
            y = y_start + j * y_space
            positions[i].append((x, y))

            # Draw neuron
            if i == 0:  # Input layer
                circle = plt.Circle((x, y), 0.025, color="lightgreen", ec="black", lw=2, zorder=3)
                ax.text(x - 0.08, y, f"x{j+1}", ha="right", va="center", fontsize=11, weight="bold")
            else:  # Hidden/output layers
                circle = plt.Circle((x, y), 0.025, color="steelblue", ec="black", lw=2, zorder=3)
            ax.add_patch(circle)

            # Label output neuron
            if i == len(layers) - 1:
                ax.text(x + 0.08, y, "output", ha="left", va="center", fontsize=11, weight="bold")

        # Draw connections with weights
        if i > 0:
            try:
                weights, bias = model.layers[i - 1].get_weights()
                for src_idx, (px, py) in enumerate(positions[i - 1]):
                    for dst_idx, (cx, cy) in enumerate(positions[i]):
                        weight = weights[src_idx][dst_idx]
                        # Color by weight: red=negative, blue=positive
                        color = "red" if weight < 0 else "blue"
                        alpha = min(abs(weight), 1.0)
                        linewidth = 1 + abs(weight) * 2
                        ax.plot([px, cx], [py, cy], color=color, alpha=alpha,
                               lw=linewidth, zorder=1)
                        # Display weight value
                        mid_x, mid_y = (px + cx) / 2, (py + cy) / 2
                        ax.text(mid_x, mid_y, f"{weight:.2f}", fontsize=7,
                               ha="center", bbox=dict(boxstyle="round,pad=0.2",
                               facecolor="white", alpha=0.8))

                # Display bias
                for dst_idx, (cx, cy) in enumerate(positions[i]):
                    if dst_idx < len(bias):
                        ax.text(cx, cy - 0.05, f"b={bias[dst_idx]:.2f}",
                               fontsize=8, ha="center", style="italic")
            except Exception as e:
                logger.warning(f"Could not extract weights: {e}")

        # Layer label with activation
        label = f"{layer['name']}"
        if layer["act"]:
            label += f"\n{layer['act']}"
        ax.text(x, 0.85, label, ha="center", va="top", fontsize=10, weight="bold")

    ax.set_title(f"{gate_type.upper()} Gate - Perceptron Network Architecture",
                fontsize=14, weight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    output_path = output_dir / f"{gate_type}_network.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Network diagram saved: {output_path}")
    return output_path


def plot_data_points(X: np.ndarray, y: np.ndarray, gate_type: str, output_dir: Path = None) -> Path:
    """Plot data points as scatter plot colored by output."""
    if output_dir is None:
        output_dir = Path(__file__).parent / "visualizations"
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 8))
    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm",
                         alpha=0.6, edgecolors="black", linewidth=0.5, s=50)
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Output", rotation=270, labelpad=20)
    ax.set_xlabel("Input x1", fontsize=12)
    ax.set_ylabel("Input x2", fontsize=12)
    ax.set_title(f"{gate_type.upper()} Gate Data (n={len(X)})", fontsize=14, weight="bold")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)

    output_path = output_dir / f"{gate_type}_data.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Data plot saved: {output_path}")
    return output_path


def plot_training_history(
    history: keras.callbacks.History,
    gate_type: str,
    output_dir: Path = None
) -> Path:
    """Plot training history (loss and accuracy curves)."""
    if output_dir is None:
        output_dir = Path(__file__).parent / "visualizations"
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Loss
    ax1.plot(history.history["loss"], label="Training Loss", lw=2)
    ax1.plot(history.history["val_loss"], label="Validation Loss", lw=2)
    ax1.set_xlabel("Epoch", fontsize=12)
    ax1.set_ylabel("Loss (MSE)", fontsize=12)
    ax1.set_title(f"{gate_type.upper()} - Loss", fontsize=13, weight="bold")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Accuracy
    ax2.plot(history.history["accuracy"], label="Training Accuracy", lw=2)
    ax2.plot(history.history["val_accuracy"], label="Validation Accuracy", lw=2)
    ax2.set_xlabel("Epoch", fontsize=12)
    ax2.set_ylabel("Accuracy", fontsize=12)
    ax2.set_title(f"{gate_type.upper()} - Accuracy", fontsize=13, weight="bold")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    output_path = output_dir / f"{gate_type}_training.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Training history saved: {output_path}")
    return output_path
