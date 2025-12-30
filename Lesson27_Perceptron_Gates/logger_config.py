"""
Logging Configuration Module

Author: Yair Levi
Date: 2025-12-30

Configures ring buffer logging system with 20 rotating files of 16MB each.
"""

import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler


# Constants
MAX_LOG_FILES = 20
MAX_BYTES_PER_FILE = 16 * 1024 * 1024  # 16 MB
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name=None, log_dir="log", level=logging.INFO):
    """
    Setup logger with rotating file handler (ring buffer).

    Args:
        name: Logger name (None for root logger)
        log_dir: Directory for log files (relative path)
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    # Get project root and create log directory
    project_root = Path(__file__).parent
    log_path = project_root / log_dir
    log_path.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create rotating file handler
    log_file = log_path / "perceptron_gates.log"
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=MAX_BYTES_PER_FILE,
        backupCount=MAX_LOG_FILES - 1  # Total files = 1 current + (n-1) backups
    )

    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(file_handler)

    # Also add console handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    # Test the logger
    test_logger = setup_logger("test")
    test_logger.info("Logger test - INFO level")
    test_logger.warning("Logger test - WARNING level")
    test_logger.error("Logger test - ERROR level")
    print(f"Log file created successfully at: {Path(__file__).parent / 'log'}")
