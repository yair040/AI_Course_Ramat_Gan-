# autoencoder/config.py
# Author: Yair Levi
"""
Central configuration and hyperparameters for the AutoEncoder project.
All tuneable values live here. Override via environment variables if needed.
"""

import os
import torch
from pathlib import Path

# ── Paths (all relative to project root) ──────────────────────────────────────
ROOT = Path(__file__).parent.parent          # project root: AutoEncoder/
CATS_RAW        = ROOT / "cats"
DOGS_RAW        = ROOT / "dogs"
CATS_RESIZED    = ROOT / "output" / "cats_resized"
DOGS_RESIZED    = ROOT / "output" / "dogs_resized"
MODELS_DIR      = ROOT / "output" / "models"
PLOTS_DIR       = ROOT / "output" / "plots"
LOG_DIR         = ROOT / "log"

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_MAX_BYTES   = 16 * 1024 * 1024   # 16 MB per file
LOG_BACKUP_COUNT = 19                 # 19 backups + 1 active = 20 files total
LOG_LEVEL       = "INFO"
LOG_FORMAT      = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_FILE        = LOG_DIR / "autoencoder.log"

# ── Reproducibility ───────────────────────────────────────────────────────────
SEED = 42

# ── Device ────────────────────────────────────────────────────────────────────
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Config:
    """Hyperparameter container. Modify defaults here or subclass for experiments."""

    # Image preprocessing
    image_size: tuple[int, int] = (128, 128)   # (H, W) resize target

    # Model architecture
    code_size: int       = 128    # bottleneck / latent dimension
    num_layers: int      = 3      # encoder depth (decoder mirrored)
    nodes_per_layer: int = 64     # base channel count (encoder layer 0)

    # Training
    loss_function: str   = "mse"  # options: "mse" | "bce" | "ssim"
    epochs: int          = 30
    batch_size: int      = 32
    learning_rate: float = 1e-3

    # Multiprocessing
    num_workers: int     = int(os.environ.get("NUM_WORKERS", 4))

    # Visualization
    sample_count: int    = 8

    # Paths (shared from module-level constants)
    cats_raw        = CATS_RAW
    dogs_raw        = DOGS_RAW
    cats_resized    = CATS_RESIZED
    dogs_resized    = DOGS_RESIZED
    models_dir      = MODELS_DIR
    plots_dir       = PLOTS_DIR
    log_dir         = LOG_DIR
    device          = DEVICE
    seed            = SEED

    @classmethod
    def ensure_dirs(cls) -> None:
        """Create all output directories if they don't exist."""
        for d in [cls.cats_resized, cls.dogs_resized,
                  cls.models_dir, cls.plots_dir, cls.log_dir]:
            d.mkdir(parents=True, exist_ok=True)
