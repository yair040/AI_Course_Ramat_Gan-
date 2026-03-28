# autoencoder/__init__.py
# Author: Yair Levi
"""
AutoEncoder package for cats & dogs image reconstruction
and cross-domain encoder/decoder experiments.
"""

from autoencoder.config import Config
from autoencoder.logger import get_logger
from autoencoder.model import AutoEncoder, Encoder, Decoder
from autoencoder.dataset import make_loader

__all__ = [
    "Config",
    "get_logger",
    "AutoEncoder",
    "Encoder",
    "Decoder",
    "make_loader",
]

__version__ = "1.0.0"
__author__ = "Yair Levi"
