# autoencoder/cross_utils.py
# Author: Yair Levi
"""
Shared helpers for cross-domain encoder/decoder experiments (Tasks 4 & 5).
"""

from __future__ import annotations

from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from autoencoder.config import Config
from autoencoder.dataset import make_loader
from autoencoder.logger import get_logger
from autoencoder.model import AutoEncoder, Encoder, Decoder
from autoencoder.train_utils import _plot_pairs, _denorm

log = get_logger(__name__)


def load_encoder(checkpoint_path: Path, cfg: Config) -> Encoder:
    """Load only the encoder weights from a saved checkpoint."""
    ckpt = torch.load(checkpoint_path, map_location=cfg.device)
    model = AutoEncoder(cfg)
    model.encoder.load_state_dict(ckpt["encoder"])
    log.info(f"Encoder loaded from {checkpoint_path}")
    return model.encoder


def load_decoder(checkpoint_path: Path, cfg: Config) -> Decoder:
    """Load only the decoder weights from a saved checkpoint."""
    ckpt = torch.load(checkpoint_path, map_location=cfg.device)
    model = AutoEncoder(cfg)
    model.decoder.load_state_dict(ckpt["decoder"])
    log.info(f"Decoder loaded from {checkpoint_path}")
    return model.decoder


def cross_infer_and_plot(
    encoder: nn.Module,
    decoder: nn.Module,
    loader: DataLoader,
    cfg: Config,
    save_path: Path,
    title: str,
) -> None:
    """Run encoder → decoder on a batch and save input/output plot."""
    encoder.eval()
    decoder.eval()
    encoder.to(cfg.device)
    decoder.to(cfg.device)

    batch = next(iter(loader))[:cfg.sample_count].to(cfg.device)
    with torch.no_grad():
        z = encoder(batch)
        recon = decoder(z)

    _plot_pairs(batch.cpu(), recon.cpu(), save_path, title)
    log.info(f"Cross-domain plot saved → {save_path}")
