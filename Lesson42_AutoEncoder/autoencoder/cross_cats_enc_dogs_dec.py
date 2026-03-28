# autoencoder/cross_cats_enc_dogs_dec.py
# Author: Yair Levi
"""
Task 4 — Cats Encoder + Dogs Decoder cross-domain inference.

Loads:
  encoder  ← output/models/cats_autoencoder.pth
  decoder  ← output/models/dogs_autoencoder.pth

Runs inference on:
  • dogs images   → shows how dogs look through cats encoder + dogs decoder
  • cats images   → shows how cats look through cats encoder + dogs decoder
"""

from __future__ import annotations

from autoencoder.config import Config
from autoencoder.cross_utils import load_encoder, load_decoder, cross_infer_and_plot
from autoencoder.dataset import make_loader
from autoencoder.logger import get_logger

log = get_logger(__name__)


def run(cfg: Config) -> None:
    """Entry point for Task 4."""
    cfg.ensure_dirs()
    log.info("=== Task 4: Cats Encoder + Dogs Decoder START ===")

    cats_ckpt = cfg.models_dir / "cats_autoencoder.pth"
    dogs_ckpt = cfg.models_dir / "dogs_autoencoder.pth"

    for path in [cats_ckpt, dogs_ckpt]:
        if not path.exists():
            raise FileNotFoundError(
                f"{path} not found. Run Tasks 2 & 3 first."
            )

    encoder = load_encoder(cats_ckpt, cfg)
    decoder = load_decoder(dogs_ckpt, cfg)

    # ── Inference on dogs images ───────────────────────────────────────────────
    dogs_loader = make_loader(cfg.dogs_resized, cfg, shuffle=True)
    cross_infer_and_plot(
        encoder, decoder, dogs_loader, cfg,
        cfg.plots_dir / "task4_dogs_input.png",
        "Task 4: Cats-Enc + Dogs-Dec | Dogs Input",
    )

    # ── Inference on cats images ───────────────────────────────────────────────
    cats_loader = make_loader(cfg.cats_resized, cfg, shuffle=True)
    cross_infer_and_plot(
        encoder, decoder, cats_loader, cfg,
        cfg.plots_dir / "task4_cats_input.png",
        "Task 4: Cats-Enc + Dogs-Dec | Cats Input",
    )

    print(f"\n[Task 4] Cross-domain plots saved to {cfg.plots_dir}\n")
    log.info("=== Task 4 DONE ===")
