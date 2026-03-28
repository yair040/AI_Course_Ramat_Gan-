# autoencoder/preprocessing.py
# Author: Yair Levi
"""
Task 1 — Resize all cats and dogs images using multiprocessing.
"""

from __future__ import annotations

import time
from multiprocessing import Pool
from pathlib import Path

from PIL import Image

from autoencoder.config import Config
from autoencoder.logger import get_logger

log = get_logger(__name__)

_IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def _collect_paths(src: Path) -> list[Path]:
    return [p for p in src.iterdir() if p.suffix.lower() in _IMG_EXTENSIONS]


def _resize_one(args: tuple[Path, Path, tuple[int, int]]) -> str:
    """Worker function: resize a single image and save it."""
    src_path, dst_path, size = args
    try:
        with Image.open(src_path) as img:
            img = img.convert("RGB")
            img = img.resize((size[1], size[0]), Image.LANCZOS)  # (W, H)
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(dst_path, "JPEG", quality=95)
        return f"OK: {src_path.name}"
    except Exception as exc:
        return f"ERR: {src_path.name} — {exc}"


def _build_args(
    src_dir: Path,
    dst_dir: Path,
    size: tuple[int, int],
) -> list[tuple[Path, Path, tuple[int, int]]]:
    paths = _collect_paths(src_dir)
    return [(p, dst_dir / (p.stem + ".jpg"), size) for p in paths]


def resize_folder(
    src_dir: Path,
    dst_dir: Path,
    size: tuple[int, int],
    num_workers: int,
) -> None:
    """Resize all images in *src_dir* → *dst_dir* using a multiprocessing Pool."""
    args = _build_args(src_dir, dst_dir, size)
    log.info(f"Resizing {len(args)} images from {src_dir} → {dst_dir} "
             f"(workers={num_workers})")
    errors = 0
    with Pool(processes=num_workers) as pool:
        for i, result in enumerate(pool.imap_unordered(_resize_one, args), 1):
            if result.startswith("ERR"):
                log.warning(result)
                errors += 1
            if i % 100 == 0:
                log.info(f"  Progress: {i}/{len(args)}")
    log.info(f"Resize complete: {len(args) - errors} ok, {errors} errors")


def run(cfg: Config) -> None:
    """Entry point for Task 1."""
    cfg.ensure_dirs()
    t0 = time.perf_counter()
    log.info("=== Task 1: Image Preprocessing START ===")

    resize_folder(cfg.cats_raw, cfg.cats_resized, cfg.image_size, cfg.num_workers)
    resize_folder(cfg.dogs_raw, cfg.dogs_resized, cfg.image_size, cfg.num_workers)

    elapsed = time.perf_counter() - t0
    log.info(f"=== Task 1 DONE — elapsed: {elapsed:.2f}s ===")
    print(f"\n[Task 1] Preprocessing complete in {elapsed:.2f} seconds.\n")
