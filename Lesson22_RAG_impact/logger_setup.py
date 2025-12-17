"""Logging setup with ring buffer (20 files × 16MB).

This module configures a rotating file handler that creates a ring buffer of log files.
When the maximum number of files is reached, the oldest file is overwritten.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
import config


def setup_logger(name: str = "context_window_vs_rag") -> logging.Logger:
    """
    Setup ring buffer logger with file and console handlers.

    Creates a logger that writes to 20 rotating log files (16MB each).
    When the 20th file is full, it overwrites the first file, creating
    a ring buffer effect.

    Args:
        name: Logger name (default: "context_window_vs_rag")

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logger()
        >>> logger.info("Processing started")
        >>> logger.warning("High token count detected")
        >>> logger.error("API call failed")
    """
    # Create log directory if it doesn't exist
    os.makedirs(config.LOG_DIR, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # ========================================================================
    # File Handler (Ring Buffer)
    # ========================================================================
    file_handler = RotatingFileHandler(
        filename=os.path.join(config.LOG_DIR, "app.log"),
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(config.LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    # ========================================================================
    # Console Handler
    # ========================================================================
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    # Simpler format for console (no timestamp)
    console_formatter = logging.Formatter(
        "%(levelname)s: %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # ========================================================================
    # Add Handlers to Logger
    # ========================================================================
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log successful initialization
    logger.info(f"Logging initialized - Ring buffer: {config.LOG_BACKUP_COUNT + 1} "
                f"files × {config.LOG_MAX_BYTES // (1024*1024)}MB")

    return logger


def get_logger(name: str = "context_window_vs_rag") -> logging.Logger:
    """
    Get existing logger or create new one.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name) if logging.getLogger(name).handlers else setup_logger(name)
