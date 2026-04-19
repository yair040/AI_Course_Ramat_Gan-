"""
logger_setup.py — Ring-buffer rotating logger.
Author: Yair Levi

20 backup files × 16 MB each (~320 MB total).
Log files written to the 'log/' subfolder (relative path).
"""

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "log"
LOG_FILE = os.path.join(LOG_DIR, "lstm_filter.log")
MAX_BYTES = 16 * 1024 * 1024   # 16 MB
BACKUP_COUNT = 19               # 1 active + 19 backups = 20 total files
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str = "lstm_filter") -> logging.Logger:
    """
    Create (or retrieve) a logger with a ring-buffer rotating file handler
    and a console handler, both at INFO level.

    Args:
        name: Logger name (defaults to package root).

    Returns:
        Configured logging.Logger instance.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if called more than once.
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # --- Rotating file handler (ring buffer) ---
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # --- Console handler ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
