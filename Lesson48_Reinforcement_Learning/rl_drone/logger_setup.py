# rl_drone/logger_setup.py
# Author: Yair Levi
# Ring-buffer rotating log: 20 files × 16 MB

import logging
import os
from logging.handlers import RotatingFileHandler
from .config import LOG_DIR, LOG_FILE, LOG_MAX_BYTES, LOG_BACKUP_COUNT


def setup_logger(name: str = "rl_drone") -> logging.Logger:
    """
    Returns a logger with a rotating file handler (ring buffer)
    and a console handler, both at INFO level.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured (multiprocessing re-entry guard)

    logger.setLevel(logging.INFO)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Rotating file handler — ring buffer of 20 files × 16 MB
    fh = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger


# Module-level default logger
log = setup_logger()
