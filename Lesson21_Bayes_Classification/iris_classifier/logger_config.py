"""
Logging Configuration Module

Implements ring buffer logging with 20 rotating files of 16MB each.
Logs are stored in the 'log/' directory relative to project root.

Author: Yair Levi
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name='iris_classifier', level=logging.INFO):
    """
    Setup logger with ring buffer file rotation.

    Args:
        name: Logger name
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    # Get project root (parent of iris_classifier package)
    project_root = Path(__file__).parent.parent
    log_dir = project_root / 'log'

    # Create log directory if it doesn't exist
    log_dir.mkdir(exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger

    # Configure rotating file handler
    # 20 files total: 1 main + 19 backups
    log_file = log_dir / f'{name}.log'
    handler = RotatingFileHandler(
        log_file,
        maxBytes=16 * 1024 * 1024,  # 16MB per file
        backupCount=19  # Total 20 files (1 main + 19 backups)
    )

    # Set formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    # Also log to console for user feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info(f"Logger initialized. Log directory: {log_dir}")

    return logger
