"""
Logger Configuration Module

Sets up logging system with ring buffer rotation.
Logs to ./log/ directory with 20 files of 16 MB each.

Author: Yair Levi
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def setup_logging(
    log_dir: str = "./log",
    level: int = logging.INFO,
    max_bytes: int = 16 * 1024 * 1024,  # 16 MB
    backup_count: int = 19  # Total 20 files (main + 19 backups)
) -> logging.Logger:
    """
    Configure logging with ring buffer rotation.

    Creates a rotating file handler that maintains a ring buffer of log files.
    When the buffer is full, the oldest file is overwritten.

    Args:
        log_dir: Directory for log files
        level: Logging level (default: INFO)
        max_bytes: Maximum size per log file in bytes
        backup_count: Number of backup files (total files = backup_count + 1)

    Returns:
        Configured logger instance
    """
    # Create log directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Create rotating file handler
    log_file = log_path / "app.log"
    handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    for existing_handler in root_logger.handlers[:]:
        root_logger.removeHandler(existing_handler)

    # Add our handler
    root_logger.addHandler(handler)

    # Also add console handler for real-time feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    root_logger.info("Logging system initialized")
    root_logger.info(f"Log directory: {log_path.resolve()}")
    root_logger.info(
        f"Ring buffer: {backup_count + 1} files × "
        f"{max_bytes / (1024 * 1024):.1f} MB = "
        f"{(backup_count + 1) * max_bytes / (1024 * 1024):.0f} MB total"
    )

    return root_logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
