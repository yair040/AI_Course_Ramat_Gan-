# autoencoder/cross_dogs_enc_cats_dec.py
# Author: Yair Levi
"""
Task 5 — Dogs Encoder + Cats Decoder cross-domain inference.

Loads:
  encoder  ← output/models/dogs_autoencoder.pth
  decoder  ← output/models/cats_autoencoder.pth

Runs inference on:
  • cats images   → shows how cats look through dogs encoder + cats decoder
  • dogs images   → shows how dogs look through dogs encoder + cats decoder
"""

from __future__ import annotations

from autoencoder.config import Config
from autoencoder.cross_utils import load_encoder, load_decoder, cross_infer_and_plot
from autoencoder.dataset import make_loader
from autoencoder.logger import get_logger

log = get_logger(__name__)


def run(cfg: Config) -> None:
    """Entry point for Task 5."""
    cfg.ensure_dirs()
    log.info("=== Task 5: Dogs Encoder + Cats Decoder START ===")

    cats_ckpt = cfg.models_dir / "cats_autoencoder.pth"
    dogs_ckpt = cfg.models_dir / "dogs_autoencoder.pth"

    for path in [cats_ckpt, dogs_ckpt]:
        if not path.exists():
            raise FileNotFoundError(
                f"{path} not found. Run Tasks 2 & 3 first."
            )

    encoder = load_encoder(dogs_ckpt, cfg)
    decoder = load_decoder(cats_ckpt, cfg)

    # ── Inference on cats images ───────────────────────────────────────────────
    cats_loader = make_loader(cfg.cats_resized, cfg, shuffle=True)
    cross_infer_and_plot(
        encoder, decoder, cats_loader, cfg,
        cfg.plots_dir / "task5_cats_input.png",
        "Task 5: Dogs-Enc + Cats-Dec | Cats Input",
    )

    # ── Inference on dogs images ───────────────────────────────────────────────
    dogs_loader = make_loader(cfg.dogs_resized, cfg, shuffle=True)
    cross_infer_and_plot(
        encoder, decoder, dogs_loader, cfg,
        cfg.plots_dir / "task5_dogs_input.png",
        "Task 5: Dogs-Enc + Cats-Dec | Dogs Input",
    )

    print(f"\n[Task 5] Cross-domain plots saved to {cfg.plots_dir}\n")
    log.info("=== Task 5 DONE ===")
