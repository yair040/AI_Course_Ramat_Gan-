# autoencoder/train_dogs.py
# Author: Yair Levi
"""
Task 3 — Train AutoEncoder on dogs images.
"""

from __future__ import annotations

import random
import torch
import numpy as np

from autoencoder.config import Config
from autoencoder.dataset import make_loader
from autoencoder.logger import get_logger
from autoencoder.model import AutoEncoder
from autoencoder.train_utils import train_loop, save_reconstructions

log = get_logger(__name__)


def _set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def run(cfg: Config) -> None:
    """Entry point for Task 3: train dogs AutoEncoder."""
    cfg.ensure_dirs()
    _set_seed(cfg.seed)

    log.info("=== Task 3: Train Dogs AutoEncoder START ===")
    log.info(f"Device: {cfg.device} | Epochs: {cfg.epochs} | "
             f"LR: {cfg.learning_rate} | Loss: {cfg.loss_function}")

    # ── Data ──────────────────────────────────────────────────────────────────
    loader = make_loader(cfg.dogs_resized, cfg)

    # ── Model ─────────────────────────────────────────────────────────────────
    model = AutoEncoder(cfg)

    # ── Train ─────────────────────────────────────────────────────────────────
    elapsed = train_loop(model, loader, cfg)
    log.info(f"Training complete in {elapsed:.2f}s")

    # ── Save weights ──────────────────────────────────────────────────────────
    save_path = cfg.models_dir / "dogs_autoencoder.pth"
    torch.save({
        "encoder": model.encoder.state_dict(),
        "decoder": model.decoder.state_dict(),
        "config": {
            "code_size": cfg.code_size,
            "num_layers": cfg.num_layers,
            "nodes_per_layer": cfg.nodes_per_layer,
            "image_size": cfg.image_size,
        },
    }, save_path)
    log.info(f"Model saved → {save_path}")

    # ── Visualise ─────────────────────────────────────────────────────────────
    plot_loader = make_loader(cfg.dogs_resized, cfg, shuffle=True)
    save_reconstructions(
        model, plot_loader, cfg,
        cfg.plots_dir / "dogs_reconstruction.png",
        "Dogs AutoEncoder — Input vs Reconstruction",
    )

    print(f"\n[Task 3] Dogs AutoEncoder training done in {elapsed:.2f}s.")
    print(f"         Model  → {save_path}")
    print(f"         Plot   → {cfg.plots_dir / 'dogs_reconstruction.png'}\n")
    log.info("=== Task 3 DONE ===")
