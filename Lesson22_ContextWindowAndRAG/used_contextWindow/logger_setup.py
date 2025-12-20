"""
Logger Setup Module

Configures logging with a ring buffer system (20 files × 16MB each).
When the last file is full, the first file will be overwritten.

Author: Yair Levi
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import config


def setup_logger(name: str = "context_window_test") -> logging.Logger:
    """
    Set up a logger with rotating file handler and console output.

    The logger uses a ring buffer system:
    - 20 log files maximum (app.log, app.log.1, app.log.2, ..., app.log.19)
    - Each file can be up to 16MB
    - When app.log.19 is full, app.log starts being overwritten

    Args:
        name: Name of the logger (default: "context_window_test")

    Returns:
        Configured logger instance
    """
    # Create log directory if it doesn't exist
    log_path = Path(config.LOG_DIR)
    log_path.mkdir(exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    # Create rotating file handler
    log_file = log_path / config.LOG_FILENAME
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=config.LOG_FILE_SIZE,
        backupCount=config.LOG_FILE_COUNT - 1  # 19 backups + 1 main = 20 total
    )

    # Create formatter
    formatter = logging.Formatter(config.LOG_FORMAT)
    file_handler.setFormatter(formatter)

    # Add file handler to logger
    logger.addHandler(file_handler)

    # Also add console handler for user feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Log initialization
    logger.info("="*70)
    logger.info("Logging system initialized successfully")
    logger.info(f"Log directory: {log_path.resolve()}")
    logger.info(f"Ring buffer: {config.LOG_FILE_COUNT} files × {config.LOG_FILE_SIZE / (1024*1024):.0f}MB each")
    logger.info("="*70)

    return logger


def get_logger(name: str = "context_window_test") -> logging.Logger:
    """
    Get an existing logger or create a new one if it doesn't exist.

    Args:
        name: Name of the logger (default: "context_window_test")

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)

    # If logger doesn't have handlers, set it up
    if not logger.handlers:
        return setup_logger(name)

    return logger
