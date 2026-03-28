# autoencoder/model.py
# Author: Yair Levi
"""
Convolutional AutoEncoder with configurable depth and width.

Architecture:
  Encoder: num_layers Conv2d blocks (ReLU + MaxPool2d), then flatten + Linear
  Decoder: Linear + reshape, then num_layers ConvTranspose2d blocks (ReLU)
  Final decoder output: Tanh activation (matches [-1,1] normalised images)
"""

from __future__ import annotations

import torch
import torch.nn as nn

from autoencoder.config import Config
from autoencoder.logger import get_logger

log = get_logger(__name__)


def _encoder_channels(cfg: Config) -> list[int]:
    """Return channel progression: [3, base, base*2, base*4, ...]"""
    channels = [3]
    c = cfg.nodes_per_layer
    for _ in range(cfg.num_layers):
        channels.append(c)
        c *= 2
    return channels


class Encoder(nn.Module):
    def __init__(self, cfg: Config) -> None:
        super().__init__()
        channels = _encoder_channels(cfg)
        layers: list[nn.Module] = []
        for i in range(len(channels) - 1):
            layers += [
                nn.Conv2d(channels[i], channels[i + 1], 3, padding=1),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(2),
            ]
        self.conv = nn.Sequential(*layers)
        # Compute flattened size after pooling
        h = cfg.image_size[0] // (2 ** cfg.num_layers)
        w = cfg.image_size[1] // (2 ** cfg.num_layers)
        self.flat_dim = channels[-1] * h * w
        self.fc = nn.Linear(self.flat_dim, cfg.code_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)


class Decoder(nn.Module):
    def __init__(self, cfg: Config) -> None:
        super().__init__()
        channels = _encoder_channels(cfg)
        self.channels = channels
        self.cfg = cfg
        h = cfg.image_size[0] // (2 ** cfg.num_layers)
        w = cfg.image_size[1] // (2 ** cfg.num_layers)
        self.h, self.w = h, w
        self.fc = nn.Linear(cfg.code_size, channels[-1] * h * w)
        layers: list[nn.Module] = []
        rev = list(reversed(channels))          # [deepest … 3]
        for i in range(len(rev) - 1):
            is_last = (i == len(rev) - 2)
            layers += [
                nn.ConvTranspose2d(rev[i], rev[i + 1], 4, stride=2, padding=1),
                nn.Tanh() if is_last else nn.ReLU(inplace=True),
            ]
        self.deconv = nn.Sequential(*layers)

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        x = self.fc(z)
        x = x.view(x.size(0), self.channels[-1], self.h, self.w)
        return self.deconv(x)


class AutoEncoder(nn.Module):
    def __init__(self, cfg: Config) -> None:
        super().__init__()
        self.encoder = Encoder(cfg)
        self.decoder = Decoder(cfg)
        log.info(
            f"AutoEncoder: layers={cfg.num_layers}, "
            f"nodes={cfg.nodes_per_layer}, code={cfg.code_size}"
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.decoder(self.encoder(x))

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        return self.encoder(x)

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        return self.decoder(z)
