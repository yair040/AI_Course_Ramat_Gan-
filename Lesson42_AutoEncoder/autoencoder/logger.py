# autoencoder/logger.py
# Author: Yair Levi
"""
Ring-buffer rotating file logger.
- 20 files maximum (1 active + 19 backups)
- Each file up to 16 MB
- When the last backup is full, Python's RotatingFileHandler
  overwrites the oldest — achieving a ring-buffer effect.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from autoencoder.config import (
    LOG_DIR, LOG_FILE, LOG_MAX_BYTES,
    LOG_BACKUP_COUNT, LOG_LEVEL, LOG_FORMAT,
)

_initialized: bool = False


def _setup_root_logger() -> None:
    """Configure the root logger once per process."""
    global _initialized
    if _initialized:
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    formatter = logging.Formatter(LOG_FORMAT)

    # ── Rotating file handler (ring buffer) ───────────────────────────────────
    fh = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    fh.setFormatter(formatter)
    root.addHandler(fh)

    # ── Console handler ───────────────────────────────────────────────────────
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    root.addHandler(ch)

    _initialized = True


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger.  Configures root handlers on first call.

    Usage:
        log = get_logger(__name__)
        log.info("Hello, world!")
    """
    _setup_root_logger()
    return logging.getLogger(name)
