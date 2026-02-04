"""
Logging utilities with ring buffer implementation.

This module provides a configured logger with rotating file handler
that implements a ring buffer (20 files, 16MB each).

Author: Yair Levi
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

from ..config import (
    LOG_FILENAME,
    LOG_MAX_BYTES,
    LOG_BACKUP_COUNT,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    LOG_LEVEL
)

# Global logger instance
_logger = None


def setup_logger(name: str = "video_processing") -> logging.Logger:
    """
    Setup and configure the ring buffer logger.
    
    This creates a logger with a RotatingFileHandler that maintains
    a ring buffer of 20 log files, each up to 16MB in size.
    
    Args:
        name: Logger name (default: "video_processing")
    
    Returns:
        logging.Logger: Configured logger instance
    """
    global _logger
    
    if _logger is not None:
        return _logger
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create rotating file handler (ring buffer)
    file_handler = RotatingFileHandler(
        filename=str(LOG_FILENAME),
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    _logger = logger
    logger.info("Logger initialized successfully")
    logger.info(f"Log file: {LOG_FILENAME}")
    logger.info(f"Ring buffer: {LOG_BACKUP_COUNT + 1} files x {LOG_MAX_BYTES / (1024*1024):.0f}MB")
    
    return logger


def get_logger() -> logging.Logger:
    """
    Get the configured logger instance.
    
    If the logger hasn't been set up yet, this will set it up.
    
    Returns:
        logging.Logger: The logger instance
    """
    if _logger is None:
        return setup_logger()
    return _logger
