# autoencoder/train_utils.py
# Author: Yair Levi
"""
Shared training helpers: loss selection, train loop, and sample visualization.
"""

from __future__ import annotations

import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm  # progress bar per epoch

from autoencoder.config import Config
from autoencoder.logger import get_logger

log = get_logger(__name__)


def get_loss_fn(name: str) -> nn.Module:
    """Return a loss function by name ('mse', 'bce')."""
    name = name.lower()
    if name == "mse":
        return nn.MSELoss()
    if name == "bce":
        return nn.BCEWithLogitsLoss()
    log.warning(f"Unknown loss '{name}', falling back to MSE")
    return nn.MSELoss()


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    loss_fn: nn.Module,
    device: torch.device,
) -> float:
    model.train()
    total = 0.0
    for batch in loader:
        batch = batch.to(device)
        optimizer.zero_grad()
        recon = model(batch)
        loss = loss_fn(recon, batch)
        loss.backward()
        optimizer.step()
        total += loss.item() * batch.size(0)
    return total / len(loader.dataset)


def train_loop(
    model: nn.Module,
    loader: DataLoader,
    cfg: Config,
) -> float:
    """Full training loop. Returns wall-clock seconds."""
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.learning_rate)
    loss_fn = get_loss_fn(cfg.loss_function)
    model.to(cfg.device)
    t0 = time.perf_counter()
    pbar = tqdm(range(1, cfg.epochs + 1), desc="Training", unit="epoch")
    for epoch in pbar:
        avg_loss = train_one_epoch(model, loader, optimizer, loss_fn, cfg.device)
        pbar.set_postfix(loss=f"{avg_loss:.6f}")
        log.info(f"Epoch [{epoch:>3}/{cfg.epochs}]  loss={avg_loss:.6f}")
    return time.perf_counter() - t0


def save_reconstructions(
    model: nn.Module,
    loader: DataLoader,
    cfg: Config,
    save_path: Path,
    title: str = "Reconstructions",
) -> None:
    """Save a matplotlib figure with input vs reconstruction samples."""
    model.eval()
    model.to(cfg.device)
    batch = next(iter(loader))[:cfg.sample_count].to(cfg.device)
    with torch.no_grad():
        recon = model(batch)
    _plot_pairs(batch.cpu(), recon.cpu(), save_path, title)
    log.info(f"Saved reconstruction plot → {save_path}")


def _denorm(t: torch.Tensor) -> torch.Tensor:
    return (t * 0.5 + 0.5).clamp(0, 1)


def _plot_pairs(
    inputs: torch.Tensor,
    outputs: torch.Tensor,
    save_path: Path,
    title: str,
) -> None:
    n = inputs.size(0)
    fig, axes = plt.subplots(2, n, figsize=(n * 2, 4))
    fig.suptitle(title, fontsize=12)
    for i in range(n):
        img_in  = _denorm(inputs[i]).permute(1, 2, 0).numpy()
        img_out = _denorm(outputs[i]).permute(1, 2, 0).numpy()
        axes[0, i].imshow(img_in);  axes[0, i].axis("off")
        axes[1, i].imshow(img_out); axes[1, i].axis("off")
    axes[0, 0].set_ylabel("Input",  fontsize=9)
    axes[1, 0].set_ylabel("Output", fontsize=9)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=120)
    plt.close(fig)
