# autoencoder/dataset.py
# Author: Yair Levi
"""
Dataset utilities: image listing, PyTorch Dataset, and DataLoader factory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

from autoencoder.config import Config
from autoencoder.logger import get_logger

log = get_logger(__name__)

_IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def list_images(folder: Path) -> list[Path]:
    """Return sorted list of image paths in *folder* (non-recursive)."""
    paths = sorted(
        p for p in folder.iterdir()
        if p.suffix.lower() in _IMG_EXTENSIONS
    )
    log.info(f"Found {len(paths)} images in {folder}")
    return paths


class ImageDataset(Dataset):
    """Minimal image dataset that returns normalized tensors."""

    def __init__(
        self,
        folder: Path,
        image_size: tuple[int, int],
        transform: Optional[transforms.Compose] = None,
    ) -> None:
        self.paths = list_images(folder)
        if not self.paths:
            raise FileNotFoundError(f"No images found in {folder}")

        self.transform = transform or transforms.Compose([
            transforms.Resize(image_size),
            transforms.ToTensor(),                   # [0,1]
            transforms.Normalize((0.5, 0.5, 0.5),   # → [-1,1]
                                  (0.5, 0.5, 0.5)),
        ])

    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, idx: int) -> torch.Tensor:
        img = Image.open(self.paths[idx]).convert("RGB")
        return self.transform(img)


def make_loader(
    folder: Path,
    cfg: Config,
    shuffle: bool = True,
) -> DataLoader:
    """Build and return a DataLoader for *folder*."""
    dataset = ImageDataset(folder, cfg.image_size)
    loader = DataLoader(
        dataset,
        batch_size=cfg.batch_size,
        shuffle=shuffle,
        num_workers=min(cfg.num_workers, 4),
        pin_memory=(str(cfg.device) != "cpu"),
        drop_last=False,
    )
    log.info(
        f"DataLoader ready: {len(dataset)} images, "
        f"batch={cfg.batch_size}, workers={cfg.num_workers}"
    )
    return loader
