"""
logger_setup.py — Ring-buffer rotating file logger.
Author: Yair Levi

Ring buffer: 20 files × 16 MB each.
When the last file is full, RotatingFileHandler overwrites the oldest.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .config import LOG_DIR, LOG_FILE_NAME, LOG_BACKUP_COUNT, LOG_MAX_BYTES

_FMT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str = "rnn_predictor") -> logging.Logger:
    """
    Create and return a logger with:
    - RotatingFileHandler (ring buffer: LOG_BACKUP_COUNT+1 files, LOG_MAX_BYTES each)
    - StreamHandler (console, INFO level)

    Args:
        name: Logger name (usually the package name).

    Returns:
        Configured logging.Logger instance.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path: Path = LOG_DIR / LOG_FILE_NAME

    logger = logging.getLogger(name)
    if logger.handlers:
        # Avoid adding duplicate handlers on re-import
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(_FMT, datefmt=_DATE_FMT)

    # ── Rotating file handler (ring buffer) ───────────────────────────────────
    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # ── Console handler ───────────────────────────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
